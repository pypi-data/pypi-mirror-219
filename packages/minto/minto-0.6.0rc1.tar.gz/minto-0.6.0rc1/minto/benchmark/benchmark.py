from __future__ import annotations

import inspect
import itertools
import pathlib
import typing as tp

import jijmodeling as jm
from jijbench.consts.default import DEFAULT_RESULT_DIR
from jijbench.elements.date import Date
from jijbench.elements.id import ID
from jijbench.experiment.experiment import Experiment
from jijbench.functions.concat import Concat
from jijbench.functions.factory import RecordFactory
from jijbench.node.base import FunctionNode
from jijbench.solver.base import Parameter, Solver
from jijbench.solver.jijzept import InstanceData, Model
from typing_extensions import TypeGuard

if tp.TYPE_CHECKING:
    from jijzept.sampler.base_sampler import JijZeptBaseSampler


class Benchmark(FunctionNode[Experiment, Experiment]):
    """A class representing a benchmark.

    This class allows to define a benchmark as a collection of experiments
    over a set of parameters and solvers. The benchmark will be run sequentially
    or concurrently and the results of each experiment will be concatenated and
    returned as a single experiment.

    Attributes:
        params (dict[str, Iterable[Any]]): List of lists of parameters for the benchmark.
        solver (Callable | list[Callable]): List of solvers to be used in the benchmark.
        name (str | None, optional): Name of the benchmark.
    """

    def __init__(
        self,
        solver: tp.Callable[..., tp.Any] | list[tp.Callable[..., tp.Any]],
        params: dict[str, tp.Iterable[tp.Any]],
        name: str | None = None,
    ) -> None:
        """Initializes the benchmark with the given parameters and solvers.

        Args:
            solver (Callable | list[Callable]): A single solver or a list of solvers to be used in the benchmark.
                The solvers should be callable objects taking in a list of parameters.
            params (dict[str, Iterable[Any]]): Dictionary of parameters for the benchmark.
                The keys should be the names of the parameters and the values should
                be iterables of the respective parameter values.
            name (str | None, optional): Name of the benchmark. Defaults to None.

        Raises:
            TypeError: If the name is not a string.
        """

        def is_any_parameter(param: tp.Any) -> TypeGuard[Parameter[tp.Any]]:
            return isinstance(param, Parameter)

        if name is None:
            name = ID().data
        super().__init__(name)

        self.params = [
            [
                v if is_any_parameter(v) else Parameter(v, k)
                for k, v in zip(params.keys(), r)
            ]
            for r in itertools.product(*params.values())
        ]

        if isinstance(solver, tp.Callable):
            self.solver = [Solver(solver, "solver")]
        else:
            self.solver = [Solver(f, "solver") for f in solver]

    def __call__(
        self,
        inputs: list[Experiment] | None = None,
        solver_output_names: list[str] | None = None,
        concurrent: bool = False,
        autosave: bool = True,
        savedir: str | pathlib.Path = DEFAULT_RESULT_DIR,
    ) -> Experiment:
        """Executes the benchmark with the given parameters and solvers.

        Args:
            inputs (list[Experiment] | None, optional): A list of input experiments to be used by the benchmark. Defaults to None.
            concurrent (bool, optional): Whether to run the experiments concurrently or not. Defaults to False.
            autosave (bool, optional): Whether to automatically save the Experiment object after each run. Defaults to True.
            savedir (str | pathlib.Path, optional): The directory to save the Experiment object. Defaults to DEFAULT_RESULT_DIR.

        Returns:
            Experiment: The result of the benchmark as an Experiment object.
        """
        if inputs is None:
            inputs = [Experiment(autosave=autosave, savedir=savedir)]

        return super().__call__(
            inputs,
            solver_output_names=solver_output_names,
            concurrent=concurrent,
            autosave=autosave,
            savedir=savedir,
        )

    @property
    def name(self) -> str:
        """The name of the benchmark."""
        return str(self._name)

    @name.setter
    def name(self, name: str) -> None:
        """Sets the name of the benchmark.

        Args:
            name (str): The name to be set.

        Raises:
            TypeError: If the name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Becnhmark name must be string.")
        self._name = name

    def operate(
        self,
        inputs: list[Experiment],
        solver_output_names: list[str] | None = None,
        concurrent: bool = False,
        autosave: bool = True,
        savedir: str | pathlib.Path = DEFAULT_RESULT_DIR,
    ) -> Experiment:
        """Performs the operations specified in the benchmark on the input experiments and returns the Experiment object.

        Args:
            inputs (list[Experiment]): A list of input experiments.
            concurrent (bool, optional): Whether to run the operations concurrently or not. Defaults to False.
            autosave (bool, optional): Whether to automatically save the Experiment object after each run. Defaults to True.
            savedir (str | pathlib.Path, optional): The directory to save the Experiment object. Defaults to DEFAULT_RESULT_DIR.

        Returns:
            Experiment: An Experiment object representing the results of the operations performed by the benchmark.
        """
        savedir = pathlib.Path(savedir)
        savedir.mkdir(exist_ok=True, parents=True)
        (savedir / "star.csv").touch(exist_ok=True)
        savedir /= self.name

        concat: Concat[Experiment] = Concat()
        name = inputs[0].name

        experiment = concat(inputs, name=name, autosave=autosave, savedir=savedir)
        if concurrent:
            experiment = self._co()
        else:
            experiment = self._seq(experiment)

        if solver_output_names is not None:
            a, t = experiment.data
            outputs = t.data.filter(regex="solver_output")
            for record in a.values():
                record.update(
                    {
                        name: record.pop(k)
                        for k, name in zip(outputs, solver_output_names)
                    }
                )

            t.data.rename(
                columns={
                    c: name
                    for c, name in zip(outputs, solver_output_names)
                    if "solver_output" in str(c)
                },
                inplace=True,
            )
        return experiment

    def _co(self) -> Experiment:
        raise NotImplementedError

    def _seq(
        self,
        experiment: Experiment,
    ) -> Experiment:
        for solver in self.solver:
            for params in self.params:
                with experiment:
                    info = RecordFactory()(
                        [
                            Date(),
                            Parameter(solver.function.__qualname__, "solver_name"),
                            *params,
                        ]
                    )
                    ret = solver(params)
                    record = Concat()([info, ret])

                    state = getattr(experiment, "state")
                    state.index = (self.name, experiment.name)
                    experiment.append(record)
                    experiment.data[1].index.names = [
                        "benchmark_id",
                        "experiment_id",
                        "run_id",
                    ]
        return experiment


def benchmark_for(
    sampler: JijZeptBaseSampler,
    models: list[tuple[jm.Problem, jm.PH_VALUES_INTERFACE]],
    params: dict[str, tp.Iterable[tp.Any]],
    name: str | None = None,
) -> Benchmark:
    """Create a Benchmark object.

    Args:
        sampler (JijZeptBaseSampler): The sampler to use for creating the benchmark.
        models (list[tuple[jijmodeling.Problem, jijmodeling.PH_VALUES_INTERFACE]]): A list of tuples containing jijmodeling.Problem and jijmodeling.PH_VALUES_INTERFACE.
        params (dict[str, Iterable]): The parameters to use for creating the benchmark.
        name (str | None, optional): The name of the benchmark. Defaults to None.

    Raises:
        KeyError: If the argument corresponding to jijmodeling.Prolblem is missing in sample_model.
        KeyError: If the argument corresponding to instance data is missing in sample_model.

    Returns:
        Benchmark: The constructed benchmark.
    """
    sample_model = getattr(sampler, "sample_model")
    sampler_parameters = inspect.signature(sample_model).parameters
    if "problem" in sampler_parameters:
        argname_problem = "problem"
    elif "model" in sampler_parameters:
        argname_problem = "model"
    else:
        raise KeyError(
            f"The argument corresponding to jijmodeling.Prolblem is missing in sample_model of {sampler.__class__.__name__}."
        )

    if "instance_data" in sampler_parameters:
        argname_instance_data = "instance_data"
    elif "feed_dict" in sampler_parameters:
        argname_instance_data = "feed_dict"
    else:
        raise KeyError(
            f"The argument corresponding to instance data is missing in sample_model of {sampler.__class__.__name__}."
        )

    bench = Benchmark(sample_model, params, name)

    additional_params: list[list[Parameter[tp.Any]]] = []
    for problem, instance_data in models:
        data = (problem, instance_data)
        data = Model.validate_data(data)
        additional_params.append(
            [
                Parameter(data[0], argname_problem),
                InstanceData(data[1], argname_instance_data),
            ]
        )
    bench.params = [p + ap for p in bench.params for ap in additional_params]

    return bench
