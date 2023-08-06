from __future__ import annotations

import typing as tp
from dataclasses import dataclass

import numpy as np
from jijbench.elements.base import Number
from jijbench.functions.math import Max, Mean, Min, Std
from jijbench.node.base import DataNode
from jijbench.typing import ArrayType


@dataclass
class Array(DataNode[ArrayType]):
    """A class representing numpy arrays.

    Attributes:
        data (numpy.ndarray): The numpy array.
        name (str): The name of the node.
    """

    def min(self) -> Number:
        """Get the minimum value of the numpy array.

        Returns:
            Number: The minimum value of the numpy array.
        """
        return self.apply(Min())

    def max(self) -> Number:
        """Get the maximum value of the numpy array.

        Returns:
            Number: The maximum value of the numpy array.
        """
        return self.apply(Max())

    def mean(self) -> Number:
        """Get the mean value of the numpy array.

        Returns:
            Number: The mean value of the numpy array.
        """
        return self.apply(Mean())

    def std(self) -> Number:
        """Get the standard deviation of the numpy array.

        Returns:
            Number: The standard deviation of the numpy array.
        """
        return self.apply(Std())

    @classmethod
    def validate_data(cls, data: ArrayType) -> ArrayType:
        """Validate the data to ensure it is a numpy array.

        Args:
            data (numpyp.ndarray): The numpy array to validate.

        Raises:
            TypeError: If the input data is not a numpy array.

        Returns:
            numpy.ndarray: The validated numpy array.
        """
        return cls._validate_dtype(data, (np.ndarray,))
