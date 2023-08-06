import abc
import functools

from torch import Tensor

from classiq.interface.generator.generated_circuit import GeneratedCircuit

from classiq.applications.qnn.circuit_utils import extract_parameters, validate_circuit
from classiq.applications.qnn.types import ExecuteFunction, PostProcessFunction
from classiq.synthesis import SerializedQuantumProgram


class QuantumGradient(abc.ABC):
    def __init__(
        self,
        quantum_program: SerializedQuantumProgram,
        execute: ExecuteFunction,
        post_process: PostProcessFunction,
        *args,
        **kwargs
    ):
        self._execute = execute
        self._post_process = post_process

        circuit = GeneratedCircuit.parse_raw(quantum_program)
        validate_circuit(circuit)
        self._quantum_program = quantum_program
        self._parameters_names = extract_parameters(circuit)

        self.execute = functools.partial(execute, quantum_program)

    @abc.abstractmethod
    def gradient_weights(
        self, inputs: Tensor, weights: Tensor, *args, **kwargs
    ) -> Tensor:
        pass

    @abc.abstractmethod
    def gradient_inputs(
        self, inputs: Tensor, weights: Tensor, *args, **kwargs
    ) -> Tensor:
        pass
