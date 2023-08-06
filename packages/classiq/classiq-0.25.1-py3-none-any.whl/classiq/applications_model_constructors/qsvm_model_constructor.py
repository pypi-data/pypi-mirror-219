from typing import Dict, List

from classiq.interface.applications.qsvm import DataList, LabelsInt
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.expressions.pauli import Pauli
from classiq.interface.generator.expressions.qsvm_feature_map_entanglement import (
    QSVMFeatureMapEntanglement,
)
from classiq.interface.generator.functions import SynthesisNativeFunctionDefinition
from classiq.interface.generator.functions.assignment_statement import (
    AssignmentStatement,
)
from classiq.interface.generator.functions.classical_function_definition import (
    ClassicalFunctionDefinition,
)
from classiq.interface.generator.functions.classical_type import Struct
from classiq.interface.generator.functions.save_statement import SaveStatement
from classiq.interface.generator.functions.statement import Statement
from classiq.interface.generator.functions.variable_declaration_statement import (
    VariableDeclaration,
)
from classiq.interface.generator.model.model import SerializedModel
from classiq.interface.generator.quantum_invoker_call import QuantumInvokerCall
from classiq.interface.model.model import Model
from classiq.interface.model.quantum_function_call import QuantumFunctionCall

from classiq.applications_model_constructors.constructors_utilities import get_model
from classiq.exceptions import ClassiqValueError

INVALID_FEATURE_MAP_FUNC_NAME_MSG = "Invalid feature_map_function_name, it can be bloch_sphere_feature_map or pauli_feature_map"

_OUTPUT_VARIABLE_NAME = "qsvm_results"


def _bloch_sphere_feature_map_function_params(
    bloch_feature_dimension: int,
) -> Dict[str, Expression]:
    return {"feature_dimension": Expression(expr=f"{bloch_feature_dimension}")}


def _pauli_feature_map_function_params(
    paulis: List[List[Pauli]],
    entanglement: QSVMFeatureMapEntanglement,
    alpha: int,
    reps: int,
    feature_dimension: int,
) -> Dict[str, Expression]:
    paulis_str = (
        "["
        + ",".join(
            ["[" + ",".join([p.to_name() for p in p_list]) + "]" for p_list in paulis]
        )
        + "]"
    )
    pauli_feature_map_params = (
        f"{{"
        f"paulis: {paulis_str}, "
        f"entanglement: {entanglement.to_name()}, "
        f"alpha: {alpha}, "
        f"reps: {reps}, "
        f"feature_dimension: {feature_dimension}"
        f"}}"
    )
    return {
        "feature_map": Expression(
            expr=f"struct_literal(QSVMFeatureMapPauli, {pauli_feature_map_params})"
        )
    }


def get_qsvm_qmain_body(
    feature_map_function_name: str, **kwargs
) -> List[QuantumFunctionCall]:
    if feature_map_function_name == "bloch_sphere_feature_map":
        params = _bloch_sphere_feature_map_function_params(**kwargs)
    elif feature_map_function_name == "pauli_feature_map":
        params = _pauli_feature_map_function_params(**kwargs)
    else:
        raise ClassiqValueError(INVALID_FEATURE_MAP_FUNC_NAME_MSG)

    return [
        QuantumFunctionCall(
            function=feature_map_function_name,
            params=params,
        ),
    ]


def get_qsvm_cmain_body(
    train_data: DataList,
    train_labels: LabelsInt,
    test_data: DataList,
    test_labels: LabelsInt,
    predict_data: DataList,
) -> List[Statement]:
    return [
        VariableDeclaration(
            name=_OUTPUT_VARIABLE_NAME,
            var_type=Struct(name="QsvmResult"),
        ),
        AssignmentStatement(
            assigned_variable=_OUTPUT_VARIABLE_NAME,
            invoked_expression=QuantumInvokerCall(
                function="qsvm_full_run",
                params={
                    "train_data": Expression(expr=str(train_data)),
                    "train_labels": Expression(expr=str(train_labels)),
                    "test_data": Expression(expr=str(test_data)),
                    "test_labels": Expression(expr=str(test_labels)),
                    "predict_data": Expression(expr=str(predict_data)),
                },
                target_function="main",
            ),
        ),
        SaveStatement(saved_variable=_OUTPUT_VARIABLE_NAME),
    ]


def construct_qsvm_model(
    train_data: DataList,
    train_labels: LabelsInt,
    test_data: DataList,
    test_labels: LabelsInt,
    predict_data: DataList,
    feature_map_function_name: str,
    **kwargs,
) -> SerializedModel:
    qsvm_qmod = Model(
        functions=[
            SynthesisNativeFunctionDefinition(
                name="main",
                body=get_qsvm_qmain_body(
                    feature_map_function_name=feature_map_function_name, **kwargs
                ),
            ),
        ],
        classical_functions=[
            ClassicalFunctionDefinition(
                name="cmain",
                body=get_qsvm_cmain_body(
                    train_data=train_data,
                    train_labels=train_labels,
                    test_data=test_data,
                    test_labels=test_labels,
                    predict_data=predict_data,
                ),
            ),
        ],
    )

    return get_model(qsvm_qmod)
