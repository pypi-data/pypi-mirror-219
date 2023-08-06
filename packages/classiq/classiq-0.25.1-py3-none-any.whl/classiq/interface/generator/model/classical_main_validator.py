from typing import Dict, Tuple

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.assignment_statement import (
    AssignmentStatement,
)
from classiq.interface.generator.functions.classical_function_definition import (
    ClassicalFunctionDefinition,
)
from classiq.interface.generator.functions.classical_type import Histogram
from classiq.interface.generator.functions.save_statement import SaveStatement
from classiq.interface.generator.functions.variable_declaration_statement import (
    VariableDeclaration,
)
from classiq.interface.generator.model.model import (
    CLASSICAL_ENTRY_FUNCTION_NAME,
    MAIN_FUNCTION_NAME,
    SynthesisModel,
)
from classiq.interface.generator.quantum_invoker_call import QuantumInvokerCall

from classiq.model.model import DEFAULT_SAMPLE_RESULT_NAME

STANDARD_CMAIN_BODY_LENGTH = 3  # variable declaration, sample call, save statement


class NonStandardCmainError(Exception):
    pass


# `is_standard_cmain` and `extract_sample_params` could easily be merged to one function, as they
# are doing similar tasks, but we decided to separate them for the sake of a better interface
def is_standard_cmain(model: SynthesisModel) -> bool:
    try:
        classical_main = _get_classical_main(model)
        if len(classical_main.body) != STANDARD_CMAIN_BODY_LENGTH:
            return False

        _assert_variable_declaration(classical_main)
        _assert_sample_call(classical_main)
        _assert_save_statement(classical_main)

        return True
    except NonStandardCmainError:
        return False


def extract_sample_params(model: SynthesisModel) -> Tuple[int, Dict[str, float]]:
    classical_main = _get_classical_main(model)

    sample_call = _get_sample_call(classical_main)
    num_shots = _get_invoker_call_num_shots(sample_call)
    _assert_quantum_main_call(sample_call)
    qmain_params = _expression_dict_to_float_dict(sample_call.target_params)

    return num_shots, qmain_params


def _expression_dict_to_float_dict(d: Dict[str, Expression]) -> Dict[str, float]:
    return {name: value.to_float_value() for name, value in d.items()}


def _get_classical_main(model: SynthesisModel) -> ClassicalFunctionDefinition:
    if CLASSICAL_ENTRY_FUNCTION_NAME not in model.classical_function_dict:
        raise NonStandardCmainError
    return model.classical_function_dict[CLASSICAL_ENTRY_FUNCTION_NAME]


def _assert_variable_declaration(
    classical_main: ClassicalFunctionDefinition,
) -> None:
    variable_declaration = classical_main.body[0]
    if not isinstance(variable_declaration, VariableDeclaration):
        raise NonStandardCmainError

    if variable_declaration.name != DEFAULT_SAMPLE_RESULT_NAME:
        raise NonStandardCmainError
    if variable_declaration.var_type != Histogram():
        raise NonStandardCmainError


def _assert_sample_call(classical_main: ClassicalFunctionDefinition) -> None:
    sample_call = _get_sample_call(classical_main)
    _assert_quantum_main_call(sample_call)


def _get_sample_call(
    classical_main: ClassicalFunctionDefinition,
) -> QuantumInvokerCall:
    classical_call = classical_main.body[1]
    if not isinstance(classical_call, AssignmentStatement):
        raise NonStandardCmainError

    if classical_call.assigned_variable != DEFAULT_SAMPLE_RESULT_NAME:
        raise NonStandardCmainError

    invoked_expression = classical_call.invoked_expression
    if not isinstance(invoked_expression, QuantumInvokerCall):
        raise NonStandardCmainError
    if invoked_expression.function != "sample":
        raise NonStandardCmainError

    return invoked_expression


def _get_invoker_call_num_shots(invoker_call: QuantumInvokerCall) -> int:
    params = _expression_dict_to_float_dict(invoker_call.params)
    if "num_shots" not in params:
        raise NonStandardCmainError
    return int(params["num_shots"])


def _assert_quantum_main_call(sample_call: QuantumInvokerCall) -> None:
    if sample_call.target_function != MAIN_FUNCTION_NAME:
        raise NonStandardCmainError


def _assert_save_statement(
    classical_main: ClassicalFunctionDefinition,
) -> None:
    save_statement = classical_main.body[2]
    if not isinstance(save_statement, SaveStatement):
        raise NonStandardCmainError

    if save_statement.saved_variable != DEFAULT_SAMPLE_RESULT_NAME:
        raise NonStandardCmainError
