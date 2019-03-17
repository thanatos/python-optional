"""A class representing some value, or nothing.

A base class, Option[T], to represent either a value ``Some(...)``, or nothing
``Nothing()``. Use the subclasses ``Some`` and ``Nothing`` to instantiate.
"""

import abc
from typing import Callable, Generic, Type, TypeVar, Union


__all__ = ['Option', 'NoneError']


T = TypeVar('T')
U = TypeVar('U')


class Option(Generic[T], metaclass=abc.ABCMeta):
    """A type either containing a value, or nothing."""

    __slots__ = ()

    @abc.abstractmethod
    def is_none(self) -> bool:
        """Return ``True`` if there is no contained value."""
        raise NotImplementedError()

    @abc.abstractmethod
    def is_some(self) -> bool:
        """Return ``True`` if there is some contained value."""
        raise NotImplementedError()

    @abc.abstractmethod
    def unwrap(self) -> T:
        """
        If this is a Some(), return the contained value. Otherwise, raise.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def unwrap_or(self, default: T) -> T:
        """Return the contained value, or ``default`` if there is nothing."""
        raise NotImplementedError()

    @abc.abstractmethod
    def unwrap_or_else(self, fn: Callable[[], T]) -> T:
        """
        Return the contained value, or call the passed function to compute one.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def map(self, fn: Callable[[T], U]) -> 'Option[U]':
        """Apply the contained value to ``fn``, or return ``Nothing()``."""
        raise NotImplementedError()

    @abc.abstractmethod
    def map_or(self, default: U, fn: Callable[[T], U]) -> U:
        """Apply the contained value to ``fn``, or return ``default``."""
        raise NotImplementedError()

    @abc.abstractmethod
    def map_or_else(self, default: Callable[[], U], fn: Callable[[T], U]) -> U:
        """Apply the contained value to ``fn``, or compute a default."""
        raise NotImplementedError()


class Some(Option[T]):
    """A class holding a value."""

    __slots__ = ('_value',)

    def __init__(self, value: T) -> None:
        self._value = value

    def __eq__(self, other):
        if isinstance(other, Some):
            return self._value == other._value
        elif isinstance(other, Nothing):
            return False
        else:
            return NotImplemented

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self._value)

    def __repr__(self):
        return 'Some({!r})'.format(self._value)

    def is_none(self) -> bool:
        return False

    def is_some(self) -> bool:
        return True

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        _ = default
        return self._value

    def unwrap_or_else(self, fn: Callable[[], T]) -> T:
        _ = fn
        return self._value

    def map(self, fn: Callable[[T], U]) -> 'Option[U]':
        return Some(fn(self._value))

    def map_or(self, default: U, fn: Callable[[T], U]) -> U:
        _ = default
        return fn(self._value)

    def map_or_else(self, default: Callable[[], U], fn: Callable[[T], U]) -> U:
        return fn(self._value)


class Nothing(Option[T]):
    """A value representing nothing."""

    __slots__ = ()

    def __init__(self) -> None:
        pass

    def __eq__(self, other):
        if isinstance(other, Nothing):
            return True
        elif isinstance(other, Some):
            return False
        else:
            return NotImplemented

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __hash__(self):
        return 1

    def __repr__(self):
        return 'Nothing()'

    def is_none(self) -> bool:
        return True

    def is_some(self) -> bool:
        return False

    def unwrap(self) -> T:
        raise NoneError()

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, fn: Callable[[], T]) -> T:
        return fn()

    def map(self, fn: Callable[[T], U]) -> 'Option[U]':
        _ = fn
        return Nothing()

    def map_or(self, default: U, fn: Callable[[T], U]) -> U:
        _ = fn
        return default

    def map_or_else(self, default: Callable[[], U], fn: Callable[[T], U]) -> U:
        _ = fn
        return default()


class NoneError(ValueError):
    def __str__(self):
        return 'unwrap() called on an Option instance holding nothing.'
