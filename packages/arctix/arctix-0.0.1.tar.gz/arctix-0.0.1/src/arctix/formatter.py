from __future__ import annotations

__all__ = [
    "BaseFormatter",
    "DefaultFormatter",
    "MappingFormatter",
    "SequenceFormatter",
    "SetFormatter",
]

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from itertools import islice
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from arctix.utils.format import str_indent, str_mapping, str_sequence

if TYPE_CHECKING:
    from arctix.summarizer import BaseSummarizer

T = TypeVar("T")


class BaseFormatter(ABC, Generic[T]):
    r"""Define the base class to implement a formatter."""

    @abstractmethod
    def clone(self) -> BaseFormatter:
        r"""Return a copy of the formatter.

        Returns:
        -------
            ``BaseFormatter``: A copy of the formatter.

        Example usage:

        .. code-block:: pycon

            >>> from arctix.formatter import DefaultFormatter
            >>> formatter = DefaultFormatter()
            >>> formatter2 = formatter.clone()
            >>> formatter.set_max_characters(10)
            >>> formatter
            DefaultFormatter(max_characters=10)
            >>> formatter2
            DefaultFormatter(max_characters=-1)
        """

    @abstractmethod
    def equal(self, other: Any) -> bool:
        r"""Indicate if the other object is equal to the self object.

        Args:
        ----
            other: Specifies the other object to compare.

        Returns:
        -------
            bool: ``True`` if the objects are equal,
                otherwise ``False``.

        Example usage:

        .. code-block:: pycon

            >>> from arctix.formatter import DefaultFormatter
            >>> formatter = DefaultFormatter()
            >>> formatter.equal(DefaultFormatter())
            True
            >>> formatter.equal(DefaultFormatter(max_characters=10))
            False
        """

    @abstractmethod
    def format(self, summarizer: BaseSummarizer, value: T, depth: int, max_depth: int) -> str:
        r"""Format a value.

        Args:
        ----
            summarizer (``BaseSummarizer``): Specifies the summarizer.
            value: Specifies the value to summarize.

        Returns:
        -------
            str: The formatted value.

        Example usage:

        .. code-block:: pycon

            >>> from arctix import Summarizer
            >>> from arctix.formatter import DefaultFormatter
            >>> formatter = DefaultFormatter()
            >>> formatter.format(Summarizer(), 1)
            <class 'int'> 1
        """

    @abstractmethod
    def load_state_dict(self, state_dict: dict) -> None:
        r"""Load the state values from a dict.

        Args:
        ----
            state_dict (dict): a dict with parameters

        Example usage:

        .. code-block:: pycon

            >>> from arctix.formatter import DefaultFormatter
            >>> formatter = DefaultFormatter()
            >>> # Please take a look to the implementation of the state_dict
            >>> # function to know the expected structure
            >>> formatter.load_state_dict({"max_characters": 10})
            >>> formatter
            DefaultFormatter(max_characters=10)
        """

    @abstractmethod
    def state_dict(self) -> dict:
        r"""Return a dictionary containing state values.

        Example usage:
            dict: the state values in a dict.

        Example usage:

        .. code-block:: pycon

            >>> from arctix.formatter import DefaultFormatter
            >>> formatter = DefaultFormatter()
            >>> formatter.state_dict()
            {'max_characters': -1}
        """


class DefaultFormatter(BaseFormatter[Any]):
    r"""Implements the default formatter.

    Args:
    ----
        max_characters (int, optional): Specifies the maximum number
            of characters to show. If a negative value is provided,
            all the characters are shown. Default: ``-1``
    """

    def __init__(self, max_characters: int = -1) -> None:
        self.set_max_characters(max_characters)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(max_characters={self._max_characters:,})"

    def clone(self) -> DefaultFormatter:
        return self.__class__(max_characters=self._max_characters)

    def equal(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._max_characters == other._max_characters

    def format(
        self, summarizer: BaseSummarizer, value: Any, depth: int = 0, max_depth: int = 1
    ) -> str:
        if depth >= max_depth:
            return self._format(str(value))
        return f"{type(value)} {self._format(str(value))}"

    def _format(self, value: str) -> str:
        if self._max_characters >= 0 and len(value) > self._max_characters:
            value = value[: self._max_characters] + "..."
        return value

    def load_state_dict(self, state: dict) -> None:
        self._max_characters = state["max_characters"]

    def state_dict(self) -> dict:
        return {"max_characters": self._max_characters}

    def get_max_characters(self) -> int:
        r"""Gets the maximum number of characters to show.

        Returns:
        -------
            int: The maximum number of characters to show.

        Example usage:

        .. code-block:: pycon

            >>> from arctix.formatter import DefaultFormatter
            >>> formatter = DefaultFormatter()
            >>> formatter.get_max_characters()
            -1
        """
        return self._max_characters

    def set_max_characters(self, max_characters: int) -> None:
        r"""Set the maximum number of characters to show.

        Args:
        ----
            max_characters (int): Specifies the maximum number of
                characters to show.

        Raises:
        ------
            TypeError if ``max_characters`` is not an integer.

        Example usage:

        .. code-block:: pycon

            >>> from arctix.formatter import DefaultFormatter
            >>> formatter = DefaultFormatter()
            >>> formatter.set_max_characters(10)
            >>> formatter.get_max_characters()
            10
        """
        if not isinstance(max_characters, int):
            raise TypeError(
                "Incorrect type for max_characters. Expected int value but "
                f"received {max_characters}"
            )
        self._max_characters = max_characters


class BaseCollectionFormatter(BaseFormatter[T]):
    r"""Implement a base class to implement a formatter for
    ``Collection``.

    Args:
    ----
        max_items (int, optional): Specifies the maximum number
            of items to show. If a negative value is provided,
            all the items are shown. Default: ``5``
        num_spaces (int, optional): Specifies the number of spaces
            used for the indentation. Default: ``2``.
    """

    def __init__(self, max_items: int = 5, num_spaces: int = 2) -> None:
        self.set_max_items(max_items)
        self.set_num_spaces(num_spaces)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(max_items={self._max_items:,}, "
            f"num_spaces={self._num_spaces})"
        )

    def clone(self) -> BaseCollectionFormatter:
        return self.__class__(max_items=self._max_items, num_spaces=self._num_spaces)

    def equal(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._max_items == other._max_items and self._num_spaces == other._num_spaces

    def load_state_dict(self, state: dict) -> None:
        self._max_items = state["max_items"]
        self._num_spaces = state["num_spaces"]

    def state_dict(self) -> dict:
        return {"max_items": self._max_items, "num_spaces": self._num_spaces}

    def get_max_items(self) -> int:
        r"""Gets the maximum number of items to show.

        Returns:
        -------
            int: The maximum number of items to show.

        Example usage:

        .. code-block:: pycon

            >>> from arctix.formatter import MappingFormatter
            >>> formatter = MappingFormatter()
            >>> formatter.get_max_items()
            5
        """
        return self._max_items

    def set_max_items(self, max_items: int) -> None:
        r"""Set the maximum number of items to show.

        Args:
        ----
            max_characters (int): Specifies the maximum number of
                items to show.

        Raises:
        ------
            TypeError if ``max_items`` is not an integer.

        Example usage:

        .. code-block:: pycon

            >>> from arctix.formatter import MappingFormatter
            >>> formatter = MappingFormatter()
            >>> formatter.set_max_items(10)
            >>> formatter.get_max_items()
            10
        """
        if not isinstance(max_items, int):
            raise TypeError(
                "Incorrect type for max_items. Expected int value but " f"received {max_items}"
            )
        self._max_items = max_items

    def get_num_spaces(self) -> int:
        r"""Gets the number of spaces for indentation.

        Returns:
        -------
            int: The number of spaces for indentation.

        Example usage:

        .. code-block:: pycon

            >>> from arctix.formatter import MappingFormatter
            >>> formatter = MappingFormatter()
            >>> formatter.get_num_spaces()
            2
        """
        return self._num_spaces

    def set_num_spaces(self, num_spaces: int) -> None:
        r"""Set the number of spaces for indentation.

        Args:
        ----
            max_characters (int): Specifies the number of spaces for
                indentation.

        Raises:
        ------
            TypeError if ``num_spaces`` is not an integer.
            TValueError if ``num_spaces`` is not a positive integer.

        Example usage:

        .. code-block:: pycon

            >>> from arctix.formatter import MappingFormatter
            >>> formatter = MappingFormatter()
            >>> formatter.set_num_spaces(4)
            >>> formatter.get_num_spaces()
            4
        """
        if not isinstance(num_spaces, int):
            raise TypeError(
                f"Incorrect type for num_spaces. Expected int value but received {num_spaces}"
            )
        if num_spaces < 0:
            raise ValueError(
                "Incorrect value for num_spaces. Expected a positive integer value but "
                f"received {num_spaces}"
            )
        self._num_spaces = num_spaces


class MappingFormatter(BaseCollectionFormatter[Mapping]):
    r"""Implements a formatter for ``Mapping``."""

    def format(
        self, summarizer: BaseSummarizer, value: Mapping, depth: int = 0, max_depth: int = 1
    ) -> str:
        if depth >= max_depth:
            return summarizer.summary(str(value), depth=depth + 1, max_depth=max_depth)
        typ = type(value)
        length = len(value)
        if length > 0:
            items = value.items()
            if self._max_items >= 0:
                items = islice(value.items(), self._max_items)
            value = str_mapping(
                {
                    key: summarizer.summary(val, depth=depth + 1, max_depth=max_depth)
                    for key, val in items
                },
                num_spaces=self._num_spaces,
            )
            if length > self._max_items and self._max_items >= 0:
                value = f"{value}\n..."
            value = f"(length={length:,})\n{value}"
        return str_indent(f"{typ} {value}", num_spaces=self._num_spaces)


class SequenceFormatter(BaseCollectionFormatter[Sequence]):
    r"""Implements a formatter for ``Sequence``."""

    def format(
        self, summarizer: BaseSummarizer, value: Sequence, depth: int = 0, max_depth: int = 1
    ) -> str:
        if depth >= max_depth:
            return summarizer.summary(str(value), depth=depth + 1, max_depth=max_depth)
        typ = type(value)
        length = len(value)
        if length > 0:
            if self._max_items >= 0:
                value = value[: self._max_items]
            value = str_sequence(
                [summarizer.summary(val, depth=depth + 1, max_depth=max_depth) for val in value],
                num_spaces=self._num_spaces,
            )
            if length > self._max_items and self._max_items > 0:
                value = f"{value}\n..."
            value = f"(length={length:,})\n{value}"
        return str_indent(f"{typ} {value}", num_spaces=self._num_spaces)


class SetFormatter(BaseCollectionFormatter[set]):
    r"""Implements a formatter for ``set``."""

    def format(
        self, summarizer: BaseSummarizer, value: set, depth: int = 0, max_depth: int = 1
    ) -> str:
        if depth >= max_depth:
            return summarizer.summary(str(value), depth=depth + 1, max_depth=max_depth)
        typ = type(value)
        length = len(value)
        if length > 0:
            if self._max_items >= 0:
                value = islice(value, self._max_items)
            value = str_sequence(
                [summarizer.summary(val, depth=depth + 1, max_depth=max_depth) for val in value],
                num_spaces=self._num_spaces,
            )
            if length > self._max_items and self._max_items > 0:
                value = f"{value}\n..."
            value = f"(length={length:,})\n{value}"
        return str_indent(f"{typ} {value}", num_spaces=self._num_spaces)
