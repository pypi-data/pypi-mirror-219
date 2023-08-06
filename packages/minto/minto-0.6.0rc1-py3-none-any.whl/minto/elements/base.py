from __future__ import annotations

import typing as tp
from dataclasses import dataclass

from jijbench.node.base import DataNode
from jijbench.typing import NumberTypes


@dataclass
class Number(DataNode[NumberTypes]):
    """A class representing a numerical element.

    Attributes:
        data (NumberTypes): The int or float object.
        name (Hashable): The name of the element.
    """

    @classmethod
    def validate_data(cls, data: NumberTypes) -> NumberTypes:
        """Validate the data to be a number.

        Args:
            data (NumberTypes): The data to be validated.

        Raises:
            TypeError: If the data is not a number.

        Returns:
            NumberTypes: The validated data.
        """
        return cls._validate_dtype(data, (int, float))


@dataclass
class String(DataNode[str]):
    """A class representing a string element.

    Attributes:
        data (str): The string object.
        name (Hashable): The name of the element.
    """

    @classmethod
    def validate_data(cls, data: str) -> str:
        """Validate the data to be a string.

        Args:
            data (str): The data to be validated.

        Raises:
            TypeError: If the data is not a string.

        Returns:
            str: The validated data.
        """
        return cls._validate_dtype(data, (str,))


@dataclass
class Callable(DataNode[tp.Callable[..., tp.Any]]):
    """A class representing a callable element.

    Attributes:
        data (Callable): The callable object.
        name (Hashable): The name of the element.
    """

    @classmethod
    def validate_data(cls, data: tp.Callable[..., tp.Any]) -> tp.Callable[..., tp.Any]:
        """Validate the data to be a callable.

        Args:
            data (Callable): The data to be validated.

        Raises:
            TypeError: If the data is not a callable.

        Returns:
            Callable: The validated data.

        """
        return cls._validate_dtype(data, (tp.Callable,))


@dataclass
class Any(DataNode[tp.Any]):
    """A class representing a any element.

    Attributes:
        data (Any): The any object.
        name (Hashable): The name of the element.
    """

    @classmethod
    def validate_data(cls, data: tp.Any) -> tp.Any:
        """Validate the data to be any.

        Args:
            data (Any): The data to be validated.

        Returns:
            Any: The validated data.
        """
        return data
