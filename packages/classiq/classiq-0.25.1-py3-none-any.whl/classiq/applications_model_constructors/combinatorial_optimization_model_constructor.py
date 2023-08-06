import json
from typing import List, Optional

import sympy
from pyomo import environ as pyo
from pyomo.core import ConcreteModel, Constraint, Objective, Var, maximize
from pyomo.core.base.objective import ScalarObjective
from pyomo.core.expr.sympy_tools import Pyomo2SympyVisitor, PyomoSympyBimap

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.assignment_statement import (
    AssignmentStatement,
)
from classiq.interface.generator.functions.classical_function_definition import (
    ClassicalFunctionDefinition,
)
from classiq.interface.generator.functions.classical_type import (
    ClassicalArray,
    Real,
    Struct,
    VQEResult,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.functions.save_statement import SaveStatement
from classiq.interface.generator.functions.variable_declaration_statement import (
    VariableDeclaration,
)
from classiq.interface.generator.model.model import SerializedModel
from classiq.interface.generator.quantum_function_call import WirePair
from classiq.interface.generator.quantum_invoker_call import QuantumInvokerCall
from classiq.interface.generator.standard_gates.standard_angled_gates import RXGate
from classiq.interface.generator.types.builtin_struct_declarations import Hamiltonian
from classiq.interface.generator.types.combinatorial_problem import (
    CombinatorialOptimizationStructDeclaration,
)
from classiq.interface.generator.wiring.sliced_wire import InoutPortBinding
from classiq.interface.model.model import Model
from classiq.interface.model.native_function_definition import (
    NativeFunctionDefinition,
    PortDeclaration,
)
from classiq.interface.model.quantum_function_call import (
    LambdaListComprehension,
    QuantumFunctionCall,
    QuantumLambdaFunction,
)

from classiq import Bool, ClassicalList, Integer
from classiq.applications.combinatorial_optimization.combinatorial_optimization_config import (
    OptimizerConfig,
    QAOAConfig,
)
from classiq.applications_model_constructors.constructors_utilities import get_model

_OUTPUT_VARIABLE_NAME = "solution"

QAOA_LIBRARY = [
    NativeFunctionDefinition(
        name="qaoa_mixer_layer",
        param_decls={"num_qubits": Integer(), "b": Real()},
        port_declarations={
            "target": PortDeclaration(
                name="target",
                size=Expression(expr="num_qubits"),
                direction=PortDeclarationDirection.Inout,
            ),
        },
        body=[
            QuantumFunctionCall(
                function="repeat",
                params={
                    "count": Expression(expr="num_qubits"),
                    "port_size": Expression(expr="num_qubits"),
                },
                inouts={"qbv": WirePair(in_wire="target_in", out_wire="target_out")},
                operands={
                    "iteration": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="RXGate",
                                function_params=RXGate(theta="b"),
                                inouts={
                                    "TARGET": InoutPortBinding(
                                        input_name="qbv_in",
                                        output_name="qbv_out",
                                        start=Expression(expr="index"),
                                        end=Expression(expr="index"),
                                    ),
                                },
                            )
                        ],
                    ),
                },
            ),
        ],
    ),
    NativeFunctionDefinition(
        name="qaoa_cost_layer",
        param_decls={
            "num_qubits": Integer(),
            "g": Real(),
            "hamiltonian": Hamiltonian(),
            "is_st": Bool(),
        },
        port_declarations={
            "target": PortDeclaration(
                name="target",
                size=Expression(expr="num_qubits"),
                direction=PortDeclarationDirection.Inout,
            ),
        },
        body=[
            QuantumFunctionCall(
                function="if",
                params={
                    "port_size": Expression(expr="num_qubits"),
                    "condition": Expression(expr="is_st"),
                },
                inouts={"qbv": WirePair(in_wire="target_in", out_wire="target_out")},
                operands={
                    "then": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="suzuki_trotter",
                                params={
                                    "pauli_operator": Expression(expr="hamiltonian"),
                                    "evolution_coefficient": Expression(expr="g"),
                                    "order": Expression(expr="1"),
                                    "repetitions": Expression(expr="1"),
                                },
                                inouts={
                                    "qbv": WirePair(
                                        in_wire="qbv_in", out_wire="qbv_out"
                                    )
                                },
                            ),
                        ],
                    ),
                    "else": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="permute",
                                params={
                                    "port_size": Expression(
                                        expr="len(get_field(hamiltonian[0], pauli))"
                                    ),
                                },
                                inouts={
                                    "qbv": WirePair(
                                        in_wire="qbv_in", out_wire="qbv_out"
                                    )
                                },
                                operands={
                                    "functions": LambdaListComprehension(
                                        count=Expression(expr="len(hamiltonian)"),
                                        index_var="index",
                                        func=QuantumLambdaFunction(
                                            body=[
                                                QuantumFunctionCall(
                                                    function="single_pauli_exponent",
                                                    params={
                                                        "pauli_string": Expression(
                                                            expr="get_field(hamiltonian[index], pauli)"
                                                        ),
                                                        "coefficient": Expression(
                                                            expr="g*get_field(hamiltonian[index], coefficient)"
                                                        ),
                                                    },
                                                    inputs={"qbv": "qbv_in"},
                                                    outputs={"qbv": "qbv_out"},
                                                ),
                                            ],
                                        ),
                                    ),
                                },
                            ),
                        ]
                    ),
                },
            )
        ],
    ),
    NativeFunctionDefinition(
        name="qaoa_layer",
        param_decls={
            "num_qubits": Integer(),
            "g": Real(),
            "b": Real(),
            "hamiltonian": Hamiltonian(),
            "is_st": Bool(),
        },
        port_declarations={
            "target": PortDeclaration(
                name="target",
                size=Expression(expr="num_qubits"),
                direction=PortDeclarationDirection.Inout,
            ),
        },
        body=[
            QuantumFunctionCall(
                function="qaoa_cost_layer",
                params={
                    "num_qubits": Expression(expr="num_qubits"),
                    "g": Expression(expr="g"),
                    "hamiltonian": Expression(expr="hamiltonian"),
                    "is_st": Expression(expr="is_st"),
                },
                inputs={"target": "target_in"},
                outputs={"target": "target_mid"},
            ),
            QuantumFunctionCall(
                function="qaoa_mixer_layer",
                params={
                    "num_qubits": Expression(expr="num_qubits"),
                    "b": Expression(expr="b"),
                },
                inputs={"target": "target_mid"},
                outputs={"target": "target_out"},
            ),
        ],
    ),
    NativeFunctionDefinition(
        name="qaoa_init",
        param_decls={"num_qubits": Integer()},
        port_declarations={
            "target": PortDeclaration(
                name="target",
                size=Expression(expr="num_qubits"),
                direction=PortDeclarationDirection.Inout,
            ),
        },
        body=[
            QuantumFunctionCall(
                function="repeat",
                params={
                    "count": Expression(expr="num_qubits"),
                    "port_size": Expression(expr="num_qubits"),
                },
                inouts={"qbv": WirePair(in_wire="target_in", out_wire="target_out")},
                operands={
                    "iteration": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="H",
                                inouts={
                                    "target": InoutPortBinding(
                                        input_name="qbv_in",
                                        output_name="qbv_out",
                                        start=Expression(expr="index"),
                                        end=Expression(expr="index"),
                                    ),
                                },
                            )
                        ],
                    ),
                },
            ),
        ],
    ),
    NativeFunctionDefinition(
        name="qaoa_penalty",
        param_decls={
            "num_qubits": Integer(),
            "params_list": ClassicalList(element_type=Real()),
            "hamiltonian": Hamiltonian(),
            "is_st": Bool(),
        },
        port_declarations={
            "target": PortDeclaration(
                name="target",
                size=Expression(expr="num_qubits"),
                direction=PortDeclarationDirection.Inout,
            ),
        },
        body=[
            QuantumFunctionCall(
                function="qaoa_init",
                params={
                    "num_qubits": Expression(expr="num_qubits"),
                },
                inputs={"target": "target_in"},
                outputs={"target": "target_mid"},
            ),
            QuantumFunctionCall(
                function="repeat",
                params={
                    "count": Expression(expr="len(params_list)/2"),
                    "port_size": Expression(expr="num_qubits"),
                },
                inouts={"qbv": WirePair(in_wire="target_mid", out_wire="target_out")},
                operands={
                    "iteration": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="qaoa_layer",
                                params={
                                    "num_qubits": Expression(expr="num_qubits"),
                                    "g": Expression(expr="params_list[2*index]"),
                                    "b": Expression(expr="params_list[2*index+1]"),
                                    "hamiltonian": Expression(expr="hamiltonian"),
                                    "is_st": Expression(expr="is_st"),
                                },
                                inputs={"target": "qbv_in"},
                                outputs={"target": "qbv_out"},
                            ),
                        ],
                    ),
                },
            ),
        ],
    ),
]


def pyomo2qmod(struct_name: str, pyo_model: ConcreteModel) -> str:
    symbols_map = PyomoSympyBimap()

    variables: List[sympy.Symbol] = []

    bounds_set = False
    lower_bound = None
    upper_bound = None

    for var_dict in pyo_model.component_objects(Var):
        for key in var_dict:
            var = Pyomo2SympyVisitor(symbols_map).walk_expression(var_dict[key])
            var.name = var.name.replace(",", "_")
            variables.append(var)
            if bounds_set:
                if lower_bound != var_dict[key].lb:
                    raise ValueError("All problem variables must agree on lower bound")
                if upper_bound != var_dict[key].ub:
                    raise ValueError("All problem variables must agree on upper bound")
            else:
                lower_bound = var_dict[key].lb
                upper_bound = var_dict[key].ub
                bounds_set = True

    constraint_exprs: List[sympy.Expr] = []

    for constraint_dict in pyo_model.component_objects(Constraint):
        for key in constraint_dict:
            constraint_exprs.append(
                Pyomo2SympyVisitor(symbols_map).walk_expression(
                    constraint_dict[key].expr
                )
            )

    pyo_objective: ScalarObjective = next(pyo_model.component_objects(Objective))
    objective_type_str = "Max" if pyo_objective.sense == maximize else "Min"
    objective_expr: sympy.Expr = Pyomo2SympyVisitor(symbols_map).walk_expression(
        pyo_objective
    )

    combi_struct_decl = {
        "name": struct_name,
        "variables": {str(variable): {"kind": "int"} for variable in variables},
        "variable_lower_bound": lower_bound,
        "variable_upper_bound": upper_bound,
        "constraints": [
            {"expr": str(constraint_expr)} for constraint_expr in constraint_exprs
        ],
        "objective_type": objective_type_str,
        "objective_function": {"expr": str(objective_expr)},
    }
    return json.dumps(combi_struct_decl, indent=2)


def construct_combi_opt_py_model(
    pyo_model: pyo.ConcreteModel,
    qaoa_config: Optional[QAOAConfig] = None,
    optimizer_config: Optional[OptimizerConfig] = None,
) -> Model:
    if qaoa_config is None:
        qaoa_config = QAOAConfig()

    if optimizer_config is None:
        optimizer_config = OptimizerConfig()

    max_iteration = 0
    if optimizer_config.max_iteration is not None:
        max_iteration = optimizer_config.max_iteration

    return Model(
        types=[
            CombinatorialOptimizationStructDeclaration.parse_raw(
                pyomo2qmod("MyCombiProblem", pyo_model)
            )
        ],
        functions=[
            *QAOA_LIBRARY,
            NativeFunctionDefinition(
                name="main",
                param_decls={
                    "params_list": ClassicalArray(
                        element_type=Real(), size=qaoa_config.num_layers * 2
                    )
                },
                body=[
                    QuantumFunctionCall(
                        function="qaoa_penalty",
                        params={
                            "hamiltonian": Expression(
                                expr=f"optimization_problem_to_hamiltonian(get_type(MyCombiProblem), {qaoa_config.penalty_energy})"
                            ),
                            "params_list": Expression(expr="params_list"),
                            "num_qubits": Expression(
                                expr=f"len(get_field(optimization_problem_to_hamiltonian(get_type(MyCombiProblem), {qaoa_config.penalty_energy})[0], pauli))"
                            ),
                            "is_st": Expression(expr="True"),
                        },
                    ),
                ],
            ),
        ],
        classical_functions=[
            ClassicalFunctionDefinition(
                name="cmain",
                body=[
                    VariableDeclaration(name="vqe_result", var_type=VQEResult()),
                    AssignmentStatement(
                        assigned_variable="vqe_result",
                        invoked_expression=QuantumInvokerCall(
                            function="vqe",
                            params={
                                "hamiltonian": Expression(
                                    expr=f"optimization_problem_to_hamiltonian(get_type(MyCombiProblem), {qaoa_config.penalty_energy})"
                                ),
                                "num_shots": Expression(
                                    expr=str(optimizer_config.num_shots)
                                ),
                                "maximize": Expression(
                                    expr=f"{next(pyo_model.component_objects(Objective)).sense==maximize}"
                                ),
                                "initial_point": Expression(
                                    expr=f"compute_qaoa_initial_point(optimization_problem_to_hamiltonian(get_type(MyCombiProblem), {qaoa_config.penalty_energy}),{qaoa_config.num_layers})"
                                ),
                                "optimizer_name": Expression(
                                    expr=f"Optimizer_{optimizer_config.opt_type}"
                                ),
                                "max_iteration": Expression(
                                    expr=str(max_iteration)
                                ),  # You must pass it, but 0 means use default
                                "tolerance": Expression(
                                    expr=str(optimizer_config.tolerance)
                                ),  # You must pass it, but 0 means use default
                                "step_size": Expression(
                                    expr=str(optimizer_config.step_size)
                                ),  # You must pass it, but 0 means use default
                                "skip_compute_variance": Expression(
                                    expr=str(optimizer_config.skip_compute_variance)
                                ),
                                "alpha_cvar": Expression(
                                    expr=str(optimizer_config.alpha_cvar)
                                ),  # You must pass it, but 0 means use default
                            },
                            target_function="main",
                            target_params={
                                "params_list": Expression(expr="runtime_params")
                            },
                        ),
                    ),
                    VariableDeclaration(
                        name=_OUTPUT_VARIABLE_NAME,
                        var_type=Struct(name="MyCombiProblem"),
                    ),
                    AssignmentStatement(
                        assigned_variable=_OUTPUT_VARIABLE_NAME,
                        invoked_expression=Expression(
                            expr=f"get_optimization_solution(get_type(MyCombiProblem), vqe_result, {qaoa_config.penalty_energy})"
                        ),
                    ),
                    VariableDeclaration(
                        name="hamiltonian",
                        var_type=ClassicalList(element_type=Struct(name="PauliTerm")),
                    ),
                    AssignmentStatement(
                        assigned_variable="hamiltonian",
                        invoked_expression=Expression(
                            expr=f"optimization_problem_to_hamiltonian(get_type(MyCombiProblem), {qaoa_config.penalty_energy})",
                        ),
                    ),
                    SaveStatement(saved_variable=_OUTPUT_VARIABLE_NAME),
                    SaveStatement(saved_variable="vqe_result"),
                    SaveStatement(saved_variable="hamiltonian"),
                ],
            ),
        ],
    )


def construct_combinatorial_optimization_model(
    pyo_model: pyo.ConcreteModel,
    qaoa_config: Optional[QAOAConfig] = None,
    optimizer_config: Optional[OptimizerConfig] = None,
) -> SerializedModel:
    model = construct_combi_opt_py_model(pyo_model, qaoa_config, optimizer_config)
    return get_model(model)
