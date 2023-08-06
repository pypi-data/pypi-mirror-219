from __future__ import annotations

import inspect
import typing as tp
from dataclasses import dataclass

import jijmodeling as jm
from jijbench.containers.containers import Record
from jijbench.exceptions.exceptions import SolverFailedError
from jijbench.functions.factory import RecordFactory
from jijbench.node.base import DataNode, FunctionNode
from jijbench.typing import T


@dataclass
class Parameter(DataNode[T]):
    """A parameter for a solver function.

    Attributes:
        data (Any): The data in the node.
        name (str): The name of the parameter.
    """

    name: str

    @classmethod
    def validate_data(cls, data: tp.Any) -> tp.Any:
        """A class method to validate the data before setting it.

        Args:
            data (Any): The data to be validated.

        Returns:
            Any: The validated data.
        """
        return data


@dataclass
class Response(DataNode[T]):
    """A return value of a solver function.

    Attributes:
        data (Any): The data in the node.
        name (str): The name of the return value.
    """

    name: str

    @classmethod
    def validate_data(cls, data: tp.Any) -> tp.Any:
        """A class method to validate the data before setting it.

        Args:
            data (Any): The data to be validated.

        Returns:
            Any: The validated data.
        """
        return data


class Solver(FunctionNode[Parameter[tp.Any], Record]):
    """A solver function that takes a list of Parameter and returns a Record.

    Attributes:
        name (str): The name of the solver function.
        function (Callable): The actual function to be executed.
    """

    def __init__(
        self, function: tp.Callable[..., tp.Any], name: str | None = None
    ) -> None:
        """The constructor of the `Solver` class.

        Args:
            function (Callable): The actual function to be executed.
            name (str, optional): The name of the solver function. Defaults to None.
        """
        if name is None:
            name = "solver"
        super().__init__(name)
        self.function = function

    def operate(
        self,
        inputs: list[Parameter[tp.Any]],
    ) -> Record:
        """The main operation of the solver function.

        Args:
            inputs (list[Parameter]): The list of input `Parameter` for the solver function.

        Raises:
            SolverFailedError: If an error occurs inside the solver function.

        Returns:
            Record: The result of the solver function as a `Record`.
        """
        from jijbench.solver.jijzept import SampleSet

        parameters = inspect.signature(self.function).parameters
        has_kwargs = any([p.kind == 4 for p in parameters.values()])
        if has_kwargs:
            solver_args = {node.name: node.data for node in inputs}
        else:
            solver_args = {
                node.name: node.data for node in inputs if node.name in parameters
            }
        try:
            rets = self.function(**solver_args)
            if not isinstance(rets, tuple):
                rets = (rets,)
        except Exception as e:
            msg = f'An error occurred inside your solver. Please check implementation of "{self.name}". -> {e}'
            raise SolverFailedError(msg)

        solver_return_names = [f"{self.name}_output[{i}]" for i in range(len(rets))]

        rets = [
            SampleSet(data, name)
            if isinstance(data, jm.SampleSet)
            else Response(data, name)
            for data, name in zip(rets, solver_return_names)
        ]
        factory = RecordFactory()
        return factory(rets)
