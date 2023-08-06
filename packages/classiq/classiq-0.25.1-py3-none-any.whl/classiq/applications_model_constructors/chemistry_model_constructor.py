# flake8: noqa

from typing import Dict, List, Optional, Type

from classiq.interface.chemistry.fermionic_operator import (
    FermionicOperator,
    SummedFermionicOperator,
)
from classiq.interface.chemistry.ground_state_problem import (
    CHEMISTRY_PROBLEMS_TYPE,
    HamiltonianProblem,
    MoleculeProblem,
)
from classiq.interface.generator.expressions.chemistry import Element, FermionMapping
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.assignment_statement import (
    AssignmentStatement,
)
from classiq.interface.generator.functions.classical_function_definition import (
    ClassicalFunctionDefinition,
    ClassicalStatement,
)
from classiq.interface.generator.functions.classical_type import (
    ClassicalArray,
    ClassicalType,
    Real,
    Struct,
    VQEResult,
)
from classiq.interface.generator.functions.save_statement import SaveStatement
from classiq.interface.generator.functions.variable_declaration_statement import (
    VariableDeclaration,
)
from classiq.interface.generator.quantum_invoker_call import QuantumInvokerCall
from classiq.interface.model.model import Model
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.quantum_function_call import (
    IOType,
    QuantumFunctionCall,
    QuantumLambdaFunction,
)

from classiq.applications.chemistry.ansatz_parameters import (
    AnsatzParameters,
    HEAParameters,
    HVAParameters,
    UCCParameters,
)
from classiq.applications.chemistry.chemistry_execution_parameters import (
    ChemistryExecutionParameters,
)
from classiq.applications_model_constructors.constructors_utilities import get_model
from classiq.applications_model_constructors.libraries.hea_library import HEA_LIBRARY
from classiq.exceptions import ClassiqError
from classiq.synthesis import SerializedModel

_LADDER_OPERATOR_TYPE_INDICATOR_TO_QMOD_MAPPING: Dict[str, str] = {
    "+": "PLUS",
    "-": "MINUS",
}

_CHEMISTRY_PROBLEM_PREFIX_MAPPING: Dict[Type[CHEMISTRY_PROBLEMS_TYPE], str] = {
    MoleculeProblem: "molecule",
    HamiltonianProblem: "fock_hamiltonian",
}

_ANSATZ_PARAMETERS_FUNCTION_NAME_MAPPING: Dict[Type[AnsatzParameters], str] = {
    UCCParameters: "ucc",
    HVAParameters: "hva",
}

_EXECUTION_RESULT = "vqe_result"
_MOLECULE_PROBLEM_RESULT = "molecule_result"

_HAE_GATE_MAPPING: Dict[str, QuantumFunctionCall] = {
    "h": QuantumFunctionCall(
        function="H",
        inputs={"target": "q_in"},
        outputs={"target": "q_out"},
    ),
    "x": QuantumFunctionCall(
        function="X",
        inputs={"target": "q_in"},
        outputs={"target": "q_out"},
    ),
    "y": QuantumFunctionCall(
        function="Y",
        inputs={"target": "q_in"},
        outputs={"target": "q_out"},
    ),
    "z": QuantumFunctionCall(
        function="Z",
        inputs={"target": "q_in"},
        outputs={"target": "q_out"},
    ),
    "i": QuantumFunctionCall(
        function="I",
        inputs={"target": "q_in"},
        outputs={"target": "q_out"},
    ),
    "s": QuantumFunctionCall(
        function="S",
        inputs={"target": "q_in"},
        outputs={"target": "q_out"},
    ),
    "t": QuantumFunctionCall(
        function="T",
        inputs={"target": "q_in"},
        outputs={"target": "q_out"},
    ),
    "sdg": QuantumFunctionCall(
        function="SDG",
        inputs={"target": "q_in"},
        outputs={"target": "q_out"},
    ),
    "tdg": QuantumFunctionCall(
        function="TDG",
        inputs={"target": "q_in"},
        outputs={"target": "q_out"},
    ),
    "p": QuantumFunctionCall(
        function="PHASE",
        inputs={"target": "q_in"},
        outputs={"target": "q_out"},
    ),
    "rx": QuantumFunctionCall(
        function="RX",
        params={"theta": Expression(expr="angle")},
        inputs={"target": "q_in"},
        outputs={"target": "q_out"},
    ),
    "ry": QuantumFunctionCall(
        function="RY",
        params={"theta": Expression(expr="angle")},
        inputs={"target": "q_in"},
        outputs={"target": "q_out"},
    ),
    "rz": QuantumFunctionCall(
        function="RZ",
        params={"theta": Expression(expr="angle")},
        inputs={"target": "q_in"},
        outputs={"target": "q_out"},
    ),
    "rxx": QuantumFunctionCall(
        function="RXX",
        params={"theta": Expression(expr="angle")},
        inputs={"target": "q_in"},
        outputs={"target": "q_out"},
    ),
    "ryy": QuantumFunctionCall(
        function="RYY",
        params={"theta": Expression(expr="angle")},
        inputs={"target": "q_in"},
        outputs={"target": "q_out"},
    ),
    "rzz": QuantumFunctionCall(
        function="RZZ",
        params={"theta": Expression(expr="angle")},
        inputs={"target": "q_in"},
        outputs={"target": "q_out"},
    ),
    "ch": QuantumFunctionCall(
        function="CH",
        inputs={"target": "q1_in", "control": "q2_in"},
        outputs={"target": "q1_out", "control": "q2_out"},
    ),
    "cx": QuantumFunctionCall(
        function="CX",
        inputs={"target": "q1_in", "control": "q2_in"},
        outputs={"target": "q1_out", "control": "q2_out"},
    ),
    "cy": QuantumFunctionCall(
        function="CY",
        inputs={"target": "q1_in", "control": "q2_in"},
        outputs={"target": "q1_out", "control": "q2_out"},
    ),
    "cz": QuantumFunctionCall(
        function="CZ",
        inputs={"target": "q1_in", "control": "q2_in"},
        outputs={"target": "q1_out", "control": "q2_out"},
    ),
    "crx": QuantumFunctionCall(
        function="CRX",
        params={"theta": Expression(expr="angle")},
        inputs={"target": "q1_in", "control": "q2_in"},
        outputs={"target": "q1_out", "control": "q2_out"},
    ),
    "cry": QuantumFunctionCall(
        function="CRY",
        params={"theta": Expression(expr="angle")},
        inputs={"target": "q1_in", "control": "q2_in"},
        outputs={"target": "q1_out", "control": "q2_out"},
    ),
    "crz": QuantumFunctionCall(
        function="CRZ",
        params={"theta": Expression(expr="angle")},
        inputs={"target": "q1_in", "control": "q2_in"},
        outputs={"target": "q1_out", "control": "q2_out"},
    ),
    "cp": QuantumFunctionCall(
        function="CPHASE",
        params={"theta": Expression(expr="angle")},
        inputs={"target": "q1_in", "control": "q2_in"},
        outputs={"target": "q1_out", "control": "q2_out"},
    ),
    "swap": QuantumFunctionCall(
        function="SWAP",
        inputs={"qbit0": "q1_in", "qbit1": "q2_in"},
        outputs={"qbit0": "q1_out", "qbit1": "q2_out"},
    ),
}


def _atoms_to_qmod_atoms(atoms: List[list]) -> str:
    # fmt: off
    atom_struct_literals = [
        "struct_literal(ChemistryAtom, {"
            f"element: {Element[atom[0]].to_name()},"
            "position: struct_literal(Position, {"
                f"x: {atom[1][0]},"
                f"y: {atom[1][1]},"
                f"z: {atom[1][2]}"
            "})"
        "})"
        for atom in atoms
    ]
    # fmt: on
    return ",".join(atom_struct_literals)


def _molecule_problem_to_qmod_molecule_problem(
    molecule_problem: MoleculeProblem,
) -> str:
    # fmt: off
    return (
        "struct_literal("
        "MoleculeProblem, {"
        f"mapping: {FermionMapping[molecule_problem.mapping.value.upper()].to_name()},"
        f"z2_symmetries: {molecule_problem.z2_symmetries},"
        "molecule: struct_literal("
        "Molecule, {"
        f"atoms: [{_atoms_to_qmod_atoms(molecule_problem.molecule.atoms)}],"
        f"spin: {molecule_problem.molecule.spin},"
        f"charge: {molecule_problem.molecule.charge}"
        "}"
        "),"
        f"freeze_core: {molecule_problem.freeze_core},"
        f"remove_orbitals: {molecule_problem.remove_orbitals}"
        "})")
    # fmt: on


def _fermionic_operator_to_qmod_ladder_ops(
    fermionic_operator: FermionicOperator,
) -> str:
    return "\n\t\t\t\t\t".join(
        [
            f"struct_literal(LadderOp, {{op: LadderOperator_{_LADDER_OPERATOR_TYPE_INDICATOR_TO_QMOD_MAPPING[ladder_op[0]]}, index: {ladder_op[1]}}}),"
            for ladder_op in fermionic_operator.op_list
        ]
    )[:-1]


def _summed_fermionic_operator_to_qmod_lader_terms(
    hamiltonian: SummedFermionicOperator,
) -> str:
    return "\t\t".join(
        [
            # fmt: off
            f"""
            struct_literal(LadderTerm, {{
                coefficient: {fermionic_operator[1]},
                ops: [
                    {_fermionic_operator_to_qmod_ladder_ops(fermionic_operator[0])}
                ]
            }}),"""
            for fermionic_operator in hamiltonian.op_list
            # fmt: on
        ]
    )[:-1]


def _hamiltonian_problem_to_qmod_fock_hamiltonian_problem(
    hamiltonian_problem: HamiltonianProblem,
) -> str:
    return (
        # fmt: off
        "struct_literal("
        "FockHamiltonianProblem, {"
        f"mapping: {FermionMapping[hamiltonian_problem.mapping.value.upper()].to_name()},"
        f"z2_symmetries: {hamiltonian_problem.z2_symmetries},"
        f"terms: [{_summed_fermionic_operator_to_qmod_lader_terms(hamiltonian_problem.hamiltonian)}],"
        f"num_particles: {hamiltonian_problem.num_particles}"
        "}"
        ")"
        # fmt: on
    )


def _convert_library_problem_to_qmod_problem(problem: CHEMISTRY_PROBLEMS_TYPE) -> str:
    if isinstance(problem, MoleculeProblem):
        a = _molecule_problem_to_qmod_molecule_problem(problem)
        return a
    elif isinstance(problem, HamiltonianProblem):
        return _hamiltonian_problem_to_qmod_fock_hamiltonian_problem(problem)
    else:
        raise ClassiqError(f"Invalid problem type: {problem}")


def _get_chemistry_function(
    chemistry_problem: CHEMISTRY_PROBLEMS_TYPE,
    chemistry_function_name: str,
    ansatz_parameters_expressions: Optional[Dict[str, Expression]] = None,
    inputs: Optional[IOType] = None,
    outputs: Optional[IOType] = None,
) -> QuantumFunctionCall:
    problem_prefix = _CHEMISTRY_PROBLEM_PREFIX_MAPPING[type(chemistry_problem)]
    return QuantumFunctionCall(
        function=f"{problem_prefix}_{chemistry_function_name}",
        params={
            **(ansatz_parameters_expressions or dict()),
            f"{problem_prefix}_problem": Expression(
                expr=_convert_library_problem_to_qmod_problem(chemistry_problem)
            ),
        },
        inputs=inputs or dict(),
        outputs=outputs or dict(),
    )


def _get_hartree_fock(
    chemistry_problem: CHEMISTRY_PROBLEMS_TYPE,
) -> QuantumFunctionCall:
    return _get_chemistry_function(
        chemistry_problem,
        "hartree_fock",
        outputs={"qbv": "w_hf"},
    )


def _get_hea_function(
    hea_parameters: HEAParameters, use_hartree_fock: bool
) -> QuantumFunctionCall:
    return QuantumFunctionCall(
        function="full_hea",
        params={
            "num_qubits": Expression(expr=f"{hea_parameters.num_qubits}"),
            "is_parametrized": Expression(
                expr=f"{[int(_is_parametric_gate(_HAE_GATE_MAPPING[gate])) for gate in hea_parameters.one_qubit_gates+hea_parameters.two_qubit_gates]}"
            ),
            "connectivity_map": Expression(
                expr=f"{[list(connectivity_pair) for connectivity_pair in hea_parameters.connectivity_map]}"
            ),
            "reps": Expression(expr=f"{hea_parameters.reps}"),
            "angle_params": Expression(expr="t"),
        },
        operands={
            "operands_1qubit": [
                QuantumLambdaFunction(body=[_HAE_GATE_MAPPING[gate]])
                for gate in hea_parameters.one_qubit_gates
            ],
            "operands_2qubit": [
                QuantumLambdaFunction(body=[_HAE_GATE_MAPPING[gate]])
                for gate in hea_parameters.two_qubit_gates
            ],
        },
        inputs={"x": "w_hf"} if use_hartree_fock else dict(),
    )


def _get_ansatz(
    chemistry_problem: CHEMISTRY_PROBLEMS_TYPE,
    use_hartree_fock: bool,
    ansatz_parameters: AnsatzParameters,
) -> QuantumFunctionCall:
    if isinstance(ansatz_parameters, HEAParameters):
        return _get_hea_function(ansatz_parameters, use_hartree_fock)
    return _get_chemistry_function(
        chemistry_problem,
        _ANSATZ_PARAMETERS_FUNCTION_NAME_MAPPING[type(ansatz_parameters)],
        {
            param_name: Expression(expr=str(param_value))
            for param_name, param_value in ansatz_parameters.__dict__.items()
        },
        inputs={"qbv": "w_hf"} if use_hartree_fock else None,
    )


def _get_chemistry_vqe_additional_params(
    execution_parameters: ChemistryExecutionParameters,
) -> Dict["str", Expression]:
    return {
        "num_shots": Expression(expr=f"{execution_parameters.num_shots}"),
        "maximize": Expression(expr="false"),
        "initial_point": Expression(
            expr=f"{execution_parameters.initial_point or list()}"
        ),
        "optimizer_name": Expression(
            expr=f"Optimizer_{execution_parameters.optimizer}"
        ),
        "max_iteration": Expression(expr=f"{execution_parameters.max_iteration}"),
        "tolerance": Expression(expr=f"{execution_parameters.tolerance}"),
        "step_size": Expression(expr=f"{execution_parameters.step_size}"),
        "skip_compute_variance": Expression(
            expr=f"{(str(execution_parameters.skip_compute_variance)).lower()}"
        ),
        "alpha_cvar": Expression(expr="1.0"),
    }


def _get_molecule_problem_execution_post_processing(
    molecule_problem: MoleculeProblem,
) -> List[ClassicalStatement]:
    return [
        VariableDeclaration(
            name=_MOLECULE_PROBLEM_RESULT, var_type=Struct(name="MoleculeResult")
        ),
        AssignmentStatement(
            assigned_variable=_MOLECULE_PROBLEM_RESULT,
            invoked_expression=Expression(
                expr=f"molecule_ground_state_solution_post_process({_molecule_problem_to_qmod_molecule_problem(molecule_problem)},{_EXECUTION_RESULT})"
            ),
        ),
        SaveStatement(saved_variable=_MOLECULE_PROBLEM_RESULT),
    ]


def _get_fock_hamiltonian_problem_execution_post_processing(
    hamiltonian_problem: HamiltonianProblem,
) -> List[ClassicalStatement]:
    return [
        SaveStatement(saved_variable=_EXECUTION_RESULT),
    ]


def _is_parametric_gate(call: QuantumFunctionCall) -> bool:
    return len(call.params) > 0


def _get_execution_result_post_processing_statements(
    problem: CHEMISTRY_PROBLEMS_TYPE,
) -> List[ClassicalStatement]:
    if isinstance(problem, MoleculeProblem):
        return _get_molecule_problem_execution_post_processing(problem)
    elif isinstance(problem, HamiltonianProblem):
        return _get_fock_hamiltonian_problem_execution_post_processing(problem)
    else:
        raise ClassiqError(f"Invalid problem type: {problem}")


def _count_parametric_gates(gates: List[str]) -> int:
    return sum(_is_parametric_gate(_HAE_GATE_MAPPING[gate]) for gate in gates)


def _get_hea_port_size(hea_parameters: HEAParameters) -> int:
    return hea_parameters.reps * (
        hea_parameters.num_qubits
        * _count_parametric_gates(hea_parameters.one_qubit_gates)
        + len(hea_parameters.connectivity_map)
        * _count_parametric_gates(hea_parameters.two_qubit_gates)
    )


def _get_chemistry_quantum_main_params(
    ansatz_parameters: AnsatzParameters,
) -> Dict[str, ClassicalType]:
    if not isinstance(ansatz_parameters, HEAParameters):
        return dict()
    return {
        "t": ClassicalArray(
            element_type=Real(), size=_get_hea_port_size(ansatz_parameters)
        )
    }


def _get_chemistry_quantum_main(
    chemistry_problem: CHEMISTRY_PROBLEMS_TYPE,
    use_hartree_fock: bool,
    ansatz_parameters: AnsatzParameters,
) -> NativeFunctionDefinition:
    return NativeFunctionDefinition(
        name="main",
        param_decls=_get_chemistry_quantum_main_params(ansatz_parameters),
        body=(
            [
                _get_hartree_fock(chemistry_problem),
            ]
            if use_hartree_fock
            else []
        )
        + [_get_ansatz(chemistry_problem, use_hartree_fock, ansatz_parameters)],
    )


def _get_chemistry_classical_main(
    chemistry_problem: CHEMISTRY_PROBLEMS_TYPE,
    execution_parameters: ChemistryExecutionParameters,
    is_hea: bool,
) -> ClassicalFunctionDefinition:
    qmod_problem = _convert_library_problem_to_qmod_problem(chemistry_problem)
    problem_prefix = _CHEMISTRY_PROBLEM_PREFIX_MAPPING[type(chemistry_problem)]
    return ClassicalFunctionDefinition(
        name="cmain",
        body=[
            VariableDeclaration(name=_EXECUTION_RESULT, var_type=VQEResult()),
            AssignmentStatement(
                assigned_variable=_EXECUTION_RESULT,
                invoked_expression=QuantumInvokerCall(
                    function="vqe",
                    params={
                        "hamiltonian": Expression(
                            expr=f"{problem_prefix}_problem_to_hamiltonian({qmod_problem})"
                        ),
                        **_get_chemistry_vqe_additional_params(execution_parameters),
                    },
                    target_function="main",
                    target_params={"t": Expression(expr="runtime_params")}
                    if is_hea
                    else dict(),
                ),
            ),
        ]
        + _get_execution_result_post_processing_statements(chemistry_problem),
    )


def construct_chemistry_model(
    chemistry_problem: CHEMISTRY_PROBLEMS_TYPE,
    use_hartree_fock: bool,
    ansatz_parameters: AnsatzParameters,
    execution_parameters: ChemistryExecutionParameters,
) -> SerializedModel:
    model = Model(
        functions=(HEA_LIBRARY if isinstance(ansatz_parameters, HEAParameters) else [])
        + [
            _get_chemistry_quantum_main(
                chemistry_problem, use_hartree_fock, ansatz_parameters
            ),
        ],
        classical_functions=[
            _get_chemistry_classical_main(
                chemistry_problem,
                execution_parameters,
                isinstance(ansatz_parameters, HEAParameters),
            )
        ],
    )
    return get_model(model)
