from __future__ import annotations

import abc
import numbers
from abc import ABC
from dataclasses import dataclass, field, InitVar
from math import ceil, floor, inf, nan
from typing import (Callable, Container, Generic, Iterable, Protocol, TypeVar, Union,
                    runtime_checkable, Set)

from numpy import iterable as is_iterable

from qutil.itertools import next_closest, next_largest, next_smallest

_RealT = TypeVar("_RealT", bound=numbers.Real)
_IntegralT = TypeVar("_IntegralT", bound=numbers.Integral)
_BoundT = Union[Callable[[], _RealT], _RealT]
_BoundT = Union[Iterable[_BoundT], _BoundT]


class Bound(Generic[_RealT]):
    """A lazily evaluated bound."""

    def __init__(self, default: _RealT, integral: bool):
        self.default = default
        self.integral = integral

    def __set_name__(self, owner, name):
        self._name = f'_{name}'

    def __get__(self, instance, owner=None) -> _RealT:
        if instance is None:
            return self.default

        value = getattr(instance, self._name, {self.default})
        evaluated = set()
        for item in value:
            if callable(item):
                evaluated.add(item())
            else:
                evaluated.add(item)
        if self._name.startswith('_lower'):
            lower = max(evaluated)
            if self.integral:
                try:
                    return self.cast_lower(lower)
                except (OverflowError, ValueError):
                    # inf or nan
                    return lower
            return lower
        if self._name.startswith('_upper'):
            upper = min(evaluated)
            if self.integral:
                try:
                    return self.cast_upper(upper)
                except (OverflowError, ValueError):
                    # inf or nan
                    return upper
            return upper
        raise NameError('Bound descriptor instance name should start with lower or upper')

    def __set__(self, instance, value: _BoundT):
        if value is self:
            value = self.default
        if not is_iterable(value):
            value = {value}
        else:
            value = set(value)
        setattr(instance, self._name, value)

    def cast_lower(self, lower):
        return ceil(lower)

    def cast_upper(self, upper):
        return floor(upper)


class ReciprocalBound(Bound[_RealT]):

    def cast_lower(self, lower):
        # 1/floor is less inclusive than 1/ceil
        return floor(lower)

    def cast_upper(self, upper):
        # 1/ceil is less inclusive than 1/floor
        return ceil(upper)


class Bounded(Protocol[_RealT]):
    """An object with bounds."""
    lower: Bound[_RealT]
    upper: Bound[_RealT]


@runtime_checkable
class Reciprocal(Protocol[_RealT]):
    """A reciprocal quantity that's specified by a numerator."""
    numerator: _RealT

    def _to_denominator(self, it: Iterable[_RealT | Callable[[], _RealT]]) -> Set[_RealT]:
        """Converts rationals in it to denominators given numerator."""
        result = set()
        for item in it:
            if callable(item):
                result.add(lambda: self.numerator / item())
            else:
                result.add(self.numerator / item)
        return result


class Domain(Container[_RealT], Bounded[_RealT]):
    """A domain that constrains the allowed values a parameter can take."""
    lower: Bound[_RealT]
    upper: Bound[_RealT]
    precision: int

    def __lt__(self, value: _RealT) -> bool:
        return self.round(self.max() - value) < 0

    def __gt__(self, value: _RealT) -> bool:
        return self.round(self.min() - value) > 0

    @abc.abstractmethod
    def __and__(self, other: object) -> Domain:
        ...

    def __contains__(self, value: object) -> bool:
        return isinstance(value, numbers.Real) and not (value > self or value < self)

    @abc.abstractmethod
    def min(self) -> _RealT:
        ...

    @abc.abstractmethod
    def max(self) -> _RealT:
        ...

    @abc.abstractmethod
    def next_closest(self, value: _RealT) -> _RealT:
        ...

    @abc.abstractmethod
    def next_smallest(self, value: _RealT) -> _RealT:
        ...

    @abc.abstractmethod
    def next_largest(self, value: _RealT) -> _RealT:
        ...

    def round(self, value: _RealT):
        if self.precision is None:
            return value
        return round(value, self.precision)


@dataclass
class Interval(Domain[_RealT], Bounded[_RealT], ABC):
    """An interval with lower and upper bounds."""
    lower: _BoundT[_RealT] = Bound[_RealT](default=-inf, integral=False)
    upper: _BoundT[_RealT] = Bound[_RealT](default=+inf, integral=False)
    precision: int = field(default=16, repr=False)

    def __and__(self, other: object) -> Domain:
        if isinstance(other, Reciprocal):
            # let reciprocal class handle it
            return other & self
        if isinstance(other, Interval):
            cls = type(self)
            return cls(lower=self._lower | other._lower,
                       upper=self._upper | other._upper,
                       precision=min(self.precision, other.precision))
        if isinstance(other, Iterable):
            if not isinstance(other, BoundedSet):
                other = BoundedSet(other)
            return other & self
        return NotImplemented

    def min(self) -> _RealT:
        return self.lower

    def max(self) -> _RealT:
        return self.upper


@dataclass
class DiscreteInterval(Interval[_IntegralT], Bounded[_IntegralT]):
    """A discrete interval that only allows integral values.

    Examples
    --------
    >>> x = 7
    >>> domain = DiscreteInterval(lower=-4.3, upper={5, lambda: x})
    >>> domain
    DiscreteInterval(lower=-4, upper=5)
    >>> 4 in domain
    True
    >>> 4.0 in domain  # only ints
    False
    >>> domain.next_closest(1.7)
    2
    >>> domain.next_smallest(1.7)
    1

    Bounds can be dynamic and are lazily evaluated:

    >>> x = 2
    >>> 4 in domain
    False
    >>> domain
    DiscreteInterval(lower=-4, upper=2)
    """
    lower: _BoundT[_IntegralT] = Bound[_IntegralT](default=-inf, integral=True)
    upper: _BoundT[_IntegralT] = Bound[_IntegralT](default=+inf, integral=True)

    def __contains__(self, value: object) -> bool:
        return isinstance(value, numbers.Integral) and super().__contains__(value)

    def to_bounded_set(self) -> BoundedSet:
        return BoundedSet(range(self.min(), self.max() + 1),
                          lower=self.min(),
                          upper=self.max(),
                          precision=self.precision)

    def next_closest(self, value: _RealT) -> int:
        if value < self:
            return ceil(self.min())
        if value > self:
            return floor(self.max())
        return round(value)

    def next_smallest(self, value: _RealT) -> int:
        if value < self:
            return ceil(self.min())
        if value > self:
            return floor(self.max())
        return floor(value)

    def next_largest(self, value: _RealT) -> int:
        if value < self:
            return ceil(self.min())
        if value > self:
            return floor(self.max())
        return ceil(value)


class ContinuousInterval(Interval[_RealT]):
    """A continuous interval that allows any value within its bounds.

    Examples
    --------
    >>> domain = ContinuousInterval(-3.1, 1.7)
    >>> 0 in domain
    True
    >>> 1.7 in domain
    True
    >>> 10 in domain
    False
    >>> -10 < domain
    True
    >>> domain.next_smallest(0.91)
    0.91
    >>> domain.next_largest(6)
    1.7

    """

    def next_closest(self, value: _RealT) -> _RealT:
        if value < self:
            return self.min()
        if value > self:
            return self.max()
        return value

    def next_smallest(self, value: _RealT) -> _RealT:
        return self.next_closest(value)

    def next_largest(self, value: _RealT) -> _RealT:
        return self.next_closest(value)


@dataclass
class ReciprocalDiscreteInterval(DiscreteInterval[_IntegralT], Reciprocal[_RealT]):
    """A rational interval that only allows integral denominators.

    Examples
    --------
    The interval [2.3/10, 2.3/9, ..., 2.3/1]:
    >>> domain = ReciprocalDiscreteInterval(lower=1, upper=10, numerator=2.3)
    >>> 2.3/8 in domain
    True
    >>> 2.4/8 in domain
    False
    >>> 2.3/11 < domain
    True
    >>> domain.next_smallest(0.3)  # 2.3/8
    0.2875
    >>> domain.next_largest(0.3)  # 2.3/7
    0.32857142857142857
    >>> domain.next_closest(0.3)  # 2.3/8
    0.2875

    """
    lower: _BoundT[_IntegralT] = ReciprocalBound[_IntegralT](default=1, integral=True)
    upper: _BoundT[_IntegralT] = ReciprocalBound[_IntegralT](default=inf, integral=True)
    numerator: _RealT = 1.0

    def __post_init__(self):
        self._denominator_interval = DiscreteInterval(self.lower, self.upper, self.precision)

    def __contains__(self, value: object) -> bool:
        # Works only without floating point imprecision
        denominator = self.numerator / value
        return not self.round(denominator % 1) and int(denominator) in self._denominator_interval

    def __and__(self, other: object) -> Domain:
        cls = type(self)
        if isinstance(other, DiscreteInterval):
            if isinstance(other, cls) and other.numerator == self.numerator:
                return cls(numerator=self.numerator,
                           lower=self._lower | other._lower,
                           upper=self._upper | other._upper,
                           precision=min(self.precision, other.precision))
            try:
                return self.to_bounded_set() & other.to_bounded_set()
            except TypeError:
                raise NotImplementedError(f'Intersection not implemented for {self} & {other}')
        if isinstance(other, Interval):
            return cls(numerator=self.numerator,
                       lower=self._lower | self._to_denominator(other._upper),
                       upper=self._upper | self._to_denominator(other._lower),
                       precision=min(self.precision, other.precision))
        if isinstance(other, Iterable):
            if not isinstance(other, BoundedSet):
                other = BoundedSet(other)
            return BoundedSet(other,
                              lower={self.min()} | other._lower,
                              upper={self.max()} | other._upper,
                              precision=min(self.precision, other.precision))
        return NotImplemented

    def to_bounded_set(self) -> BoundedSet:
        return BoundedSet((self.numerator / i for i in range(self.lower, self.upper + 1)),
                          lower=self.min(),
                          upper=self.max(),
                          precision=self.precision)

    def next_closest(self, value: _RealT) -> _RealT:
        return self.numerator / self._denominator_interval.next_closest(self.numerator / value)

    def next_smallest(self, value: _RealT) -> _RealT:
        return self.numerator / self._denominator_interval.next_largest(self.numerator / value)

    def next_largest(self, value: _RealT) -> _RealT:
        return self.numerator / self._denominator_interval.next_smallest(self.numerator / value)

    def min(self) -> _RealT:
        return self.numerator / self.upper

    def max(self) -> _RealT:
        return self.numerator / self.lower


@dataclass
class BoundedSet(frozenset, Domain[_RealT], Bounded[_RealT]):
    """A finite set of numbers with lower and upper bounds.

    Examples
    --------
    >>> domain = BoundedSet([1, 1.0, 3, -2.3, 7], lower=-4, upper=5)
    >>> domain  # behaves like frozenset
    BoundedSet({1, 3, -2.3, 7}, lower=-4, upper=5)
    >>> 3 in domain
    True
    >>> -1.7 in domain
    False
    >>> 7 in domain  # out of bounds
    False
    >>> domain.next_largest(2.7)
    3

    """
    iterable: InitVar[Iterable[_RealT]] = ...
    lower: _BoundT[_RealT] = Bound[_RealT](default=-inf, integral=False)
    upper: _BoundT[_RealT] = Bound[_RealT](default=+inf, integral=False)
    precision: int = field(default=16, repr=False)

    def __post_init__(self, iterable):
        super().__init__(iterable)
        self._rounded = [self.round(item) for item in self]

    def __repr__(self) -> str:
        r = super().__repr__()
        r = r.replace(')', f', lower={self.lower}, upper={self.upper})', 1)
        return r

    def __and__(self, other: object) -> Domain:
        cls = type(self)
        if isinstance(other, Domain) and not self:
            return other
        if isinstance(other, Interval):
            return cls(self,
                       lower=self._lower | other._lower,
                       upper=self._upper | other._upper,
                       precision=min(self.precision, other.precision))
        if isinstance(other, BoundedSet):
            return cls(frozenset.intersection(self, other),
                       lower=self._lower | other._lower,
                       upper=self._upper | other._upper,
                       precision=min(self.precision, other.precision))
        if isinstance(other, Iterable):
            return cls(frozenset.intersection(self, other),
                       lower=self._lower,
                       upper=self._upper,
                       precision=min(self.precision, other.precision))
        return NotImplemented

    def __contains__(self, value: object) -> bool:
        return (isinstance(value, numbers.Real)
                and self.round(self.lower - value) <= 0 <= self.round(self.upper - value)
                and self.round(value) in self._rounded)

    def min(self) -> _RealT:
        return min((item for item in self if item in self), default=nan)

    def max(self) -> _RealT:
        return max((item for item in self if item in self), default=nan)

    def next_closest(self, value: _RealT) -> _RealT:
        return next_closest(self, value, self.precision)

    def next_smallest(self, value: _RealT) -> _RealT:
        return next_smallest(self, value, self.precision)

    def next_largest(self, value: _RealT) -> _RealT:
        return next_largest(self, value, self.precision)
