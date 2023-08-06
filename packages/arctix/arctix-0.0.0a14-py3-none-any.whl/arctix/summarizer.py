from __future__ import annotations

__all__ = [
    "BaseSummarizer",
    "Summarizer",
    "summarizer_options",
    "summary",
]


from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from contextlib import contextmanager
from typing import Any

from arctix.formatter import (
    BaseFormatter,
    DefaultFormatter,
    MappingFormatter,
    SequenceFormatter,
)
from arctix.utils.format import str_indent, str_mapping


def summary(value: Any, max_depth: int = 1, summarizer: BaseSummarizer | None = None) -> str:
    r"""Summarize the input value in a string.

    Args:
    ----
        value: Specifies the value to summarize.
        max_depth (int, optional): Specifies the maximum depth to
            summarize if the input is nested. Default: ``1``
        summarizer (``BaseSummarizer`` or ``None``): Specifies the
            summarization strategy. If ``None``, the default
            ``Summarizer`` is used. Default: ``None``

    Returns:
    -------
        str: The summary as a string.

    Example usage:

    .. code-block:: pycon

        >>> from arctix import summary
        >>> print(summary(1))
        <class 'int'> 1
        >>> print(summary(["abc", "def"]))
        <class 'list'> (length=2)
          (0): abc
          (1): def
        >>> print(summary([[0, 1, 2], {"key1": "abc", "key2": "def"}]))
        <class 'list'> (length=2)
          (0): [0, 1, 2]
          (1): {'key1': 'abc', 'key2': 'def'}
        >>> print(summary([[0, 1, 2], {"key1": "abc", "key2": "def"}], max_depth=2))
        <class 'list'> (length=2)
          (0): <class 'list'> (length=3)
              (0): 0
              (1): 1
              (2): 2
          (1): <class 'dict'> (length=2)
              (key1): abc
              (key2): def
    """
    summarizer = summarizer or Summarizer()
    return summarizer.summary(value=value, depth=0, max_depth=max_depth)


class BaseSummarizer(ABC):
    r"""Define the base class to implement a summarizer."""

    @abstractmethod
    def summary(
        self,
        value: Any,
        depth: int = 0,
        max_depth: int = 1,
    ) -> str:
        r"""Summarize the input value in a string.

        Args:
        ----
            value: Specifies the value to summarize.
            max_depth (int, optional): Specifies the maximum depth to
                summarize if the input is nested. Default: ``1``
            summarizer (``BaseSummarizer`` or ``None``): Specifies the
                summarization strategy. If ``None``, the default
                ``Summarizer`` is used. Default: ``None``

        Returns:
        -------
            str: The summary as a string.

        Example usage:

        .. code-block:: pycon

            >>> from arctix import Summarizer
            >>> print(Summarizer().summary(1))
            <class 'int'> 1
            >>> print(Summarizer().summary(["abc", "def"]))
            <class 'list'> (length=2)
              (0): abc
              (1): def
            >>> print(Summarizer().summary([[0, 1, 2], {"key1": "abc", "key2": "def"}]))
            <class 'list'> (length=2)
              (0): [0, 1, 2]
              (1): {'key1': 'abc', 'key2': 'def'}
            >>> print(Summarizer().summary([[0, 1, 2], {"key1": "abc", "key2": "def"}], max_depth=2))
            <class 'list'> (length=2)
              (0): <class 'list'> (length=3)
                  (0): 0
                  (1): 1
                  (2): 2
              (1): <class 'dict'> (length=2)
                  (key1): abc
                  (key2): def
        """


class Summarizer(BaseSummarizer):
    """Implement the default summarizer.

    The registry is a class variable, so it is shared with all the
    instances of this class.
    """

    registry: dict[type[object], BaseFormatter] = {
        Mapping: MappingFormatter(),
        Sequence: SequenceFormatter(),
        dict: MappingFormatter(),
        list: SequenceFormatter(),
        object: DefaultFormatter(),
        tuple: SequenceFormatter(),
    }

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {str_indent(str_mapping(self.registry))}\n)"

    def summary(
        self,
        value: Any,
        depth: int = 0,
        max_depth: int = 1,
    ) -> str:
        return self.find_formatter(type(value)).format(
            summarizer=self,
            value=value,
            depth=depth,
            max_depth=max_depth,
        )

    @classmethod
    def add_formatter(
        cls, data_type: type[object], formatter: BaseFormatter, exist_ok: bool = False
    ) -> None:
        r"""Add a formatter for a given data type.

        Args:
        ----
            data_type: Specifies the data type for this test.
            formatter (``BaseFormatter``): Specifies the formatter
                to use for the specified type.
            exist_ok (bool, optional): If ``False``, ``RuntimeError``
                is raised if the data type already exists. This
                parameter should be set to ``True`` to overwrite the
                formatter for a type. Default: ``False``.

        Raises:
        ------
            RuntimeError if a formatter is already registered for the
                data type and ``exist_ok=False``.

        Example usage:

        .. code-block:: pycon

            >>> from arctix import Summarizer
            >>> from arctix.formatter import MappingFormatter
            >>> from collections import defaultdict
            >>> Summarizer.add_formatter(defaultdict, MappingFormatter())
            >>> # To overwrite an existing formatter
            >>> Summarizer.add_formatter(defaultdict, MappingFormatter(), exist_ok=True)
        """
        if data_type in cls.registry and not exist_ok:
            raise RuntimeError(
                f"A formatter ({cls.registry[data_type]}) is already registered for the data "
                f"type {data_type}. Please use `exist_ok=True` if you want to overwrite the "
                "formatter for this type"
            )
        cls.registry[data_type] = formatter

    @classmethod
    def has_formatter(cls, data_type: type[object]) -> bool:
        r"""Indicate if a formatter is registered for the given data
        type.

        Args:
        ----
            data_type: Specifies the data type to check.

        Returns:
        -------
            bool: ``True`` if a formatter is registered,
                otherwise ``False``.

        Example usage:

        .. code-block:: pycon

            >>> from arctix import Summarizer
            >>> Summarizer.has_formatter(list)
            True
            >>> Summarizer.has_formatter(str)
            False
        """
        return data_type in cls.registry

    @classmethod
    def find_formatter(cls, data_type: Any) -> BaseFormatter:
        r"""Find the formatter associated to an object.

        Args:
        ----
            data_type: Specifies the data type to get.

        Returns:
        -------
            ``BaseFormatter``: The formatter associated to the data
                type.

        Raises:
        ------
            TypeError if a formatter cannot be found for this data
                type.

        Example usage:

        .. code-block:: pycon

            >>> from arctix import Summarizer
            >>> Summarizer.find_formatter(list)
            SequenceFormatter(max_items=5, num_spaces=2)
            >>> Summarizer.find_formatter(str)
            DefaultFormatter(max_characters=-1)
        """
        for object_type in data_type.__mro__:
            formatter = cls.registry.get(object_type, None)
            if formatter is not None:
                return formatter
        raise TypeError(f"Incorrect data type: {data_type}")

    @classmethod
    def load_state_dict(cls, state: dict) -> None:
        r"""Load the state values from a dict.

        Args:
        ----
            state_dict (dict): a dict with parameters

        Example usage:

        .. code-block:: pycon

            >>> from arctix import Summarizer
            >>> Summarizer.load_state_dict({object: {"max_characters": 10}})
            >>> summarizer = Summarizer()
            >>> summarizer
            Summarizer(
              (<class 'collections.abc.Mapping'>): MappingFormatter(max_items=5, num_spaces=2)
              (<class 'collections.abc.Sequence'>): SequenceFormatter(max_items=5, num_spaces=2)
              (<class 'dict'>): MappingFormatter(max_items=5, num_spaces=2)
              (<class 'list'>): SequenceFormatter(max_items=5, num_spaces=2)
              (<class 'object'>): DefaultFormatter(max_characters=10)
              (<class 'tuple'>): SequenceFormatter(max_items=5, num_spaces=2)
              (<class 'collections.defaultdict'>): MappingFormatter(max_items=5, num_spaces=2)
            )
            >>> Summarizer.load_state_dict({object: {"max_characters": -1}})
            >>> summarizer
            Summarizer(
              (<class 'collections.abc.Mapping'>): MappingFormatter(max_items=5, num_spaces=2)
              (<class 'collections.abc.Sequence'>): SequenceFormatter(max_items=5, num_spaces=2)
              (<class 'dict'>): MappingFormatter(max_items=5, num_spaces=2)
              (<class 'list'>): SequenceFormatter(max_items=5, num_spaces=2)
              (<class 'object'>): DefaultFormatter(max_characters=-1)
              (<class 'tuple'>): SequenceFormatter(max_items=5, num_spaces=2)
              (<class 'collections.defaultdict'>): MappingFormatter(max_items=5, num_spaces=2)
            )
        """
        for data_type, formatter in cls.registry.items():
            if (s := state.get(data_type)) is not None:
                formatter.load_state_dict(s)

    @classmethod
    def state_dict(cls) -> dict:
        r"""Return a dictionary containing state values.

        Returns:
        -------
            dict: the state values in a dict.

        Example usage:

        .. code-block:: pycon

            >>> from arctix import Summarizer
            >>> Summarizer.state_dict()  # doctest: +ELLIPSIS
            {<class 'collections.abc.Mapping'>: {'max_items': 5},...
        """
        return {data_type: formatter.state_dict() for data_type, formatter in cls.registry.items()}

    @classmethod
    def set_max_characters(cls, max_characters: int) -> None:
        r"""Set the maximum of characters for the compatible formatter to
        the specified value.

        To be updated, the formatters need to implement the method
        ``set_max_characters``.

        Args:
        ----
            max_characters (int): Specifies the maximum of characters.

        Example usage:

        .. code-block:: pycon

            >>> from arctix import Summarizer
            >>> Summarizer.set_max_characters(10)
            >>> summarizer = Summarizer()
            >>> summarizer
            Summarizer(
              (<class 'collections.abc.Mapping'>): MappingFormatter(max_items=5, num_spaces=2)
              (<class 'collections.abc.Sequence'>): SequenceFormatter(max_items=5, num_spaces=2)
              (<class 'dict'>): MappingFormatter(max_items=5, num_spaces=2)
              (<class 'list'>): SequenceFormatter(max_items=5, num_spaces=2)
              (<class 'object'>): DefaultFormatter(max_characters=10)
              (<class 'tuple'>): SequenceFormatter(max_items=5, num_spaces=2)
              (<class 'collections.defaultdict'>): MappingFormatter(max_items=5, num_spaces=2)
            )
            >>> Summarizer.set_max_characters(-1)
            >>> summarizer
            Summarizer(
              (<class 'collections.abc.Mapping'>): MappingFormatter(max_items=5, num_spaces=2)
              (<class 'collections.abc.Sequence'>): SequenceFormatter(max_items=5, num_spaces=2)
              (<class 'dict'>): MappingFormatter(max_items=5, num_spaces=2)
              (<class 'list'>): SequenceFormatter(max_items=5, num_spaces=2)
              (<class 'object'>): DefaultFormatter(max_characters=-1)
              (<class 'tuple'>): SequenceFormatter(max_items=5, num_spaces=2)
              (<class 'collections.defaultdict'>): MappingFormatter(max_items=5, num_spaces=2)
            )
        """
        for formatter in cls.registry.values():
            if hasattr(formatter, "set_max_characters"):
                formatter.set_max_characters(max_characters)


def set_summarizer_options(max_characters: int | None = None) -> None:
    r"""Set the ``Summarizer`` options.

    Note: It is recommended to use ``summarizer_options`` rather than
    this function.

    Args:
    ----
        max_characters (int or None, optional): Specifies the maximum
            number of characters to show. If ``None``, all the
            characters are shown. Default: ``None``

    Example usage:

    .. code-block:: pycon

        >>> from arctix import set_summarizer_options, summary
        >>> print(summary("abcdefghijklmnopqrstuvwxyz"))
        <class 'str'> abcdefghijklmnopqrstuvwxyz
        >>> set_summarizer_options(max_characters=10)
        >>> print(summary("abcdefghijklmnopqrstuvwxyz"))
        <class 'str'> abcdefghij...
        >>> set_summarizer_options(max_characters=-1)
        >>> print(summary("abcdefghijklmnopqrstuvwxyz"))
        <class 'str'> abcdefghijklmnopqrstuvwxyz
    """
    if max_characters is not None:
        Summarizer.set_max_characters(max_characters)


@contextmanager
def summarizer_options(**kwargs) -> None:
    r"""Context manager that temporarily changes the summarizer options.

    Accepted arguments are same as ``set_summarizer_options``.
    The context manager temporary change the configuration of
    ``Summarizer``. This context manager has no effect if
    ``Summarizer`` is not used.

    Args:
    ----
        **kwargs: Accepted arguments are same as
            ``set_summarizer_options``.

    Example usage:

    .. code-block:: pycon

        >>> from arctix import summarizer_options, summary
        >>> print(summary("abcdefghijklmnopqrstuvwxyz"))
        <class 'str'> abcdefghijklmnopqrstuvwxyz
        >>> with summarizer_options(max_characters=10):
        ...     print(summary("abcdefghijklmnopqrstuvwxyz"))
        ...
        <class 'str'> abcdefghij...
        >>> print(summary("abcdefghijklmnopqrstuvwxyz"))
        <class 'str'> abcdefghijklmnopqrstuvwxyz
    """
    state = Summarizer.state_dict()
    set_summarizer_options(**kwargs)
    try:
        yield
    finally:
        Summarizer.load_state_dict(state)
