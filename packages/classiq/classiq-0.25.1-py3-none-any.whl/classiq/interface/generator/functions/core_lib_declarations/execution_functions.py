from classiq.interface.generator.functions.classical_function_declaration import (
    ClassicalFunctionDeclaration,
)
from classiq.interface.generator.functions.classical_type import (
    Bool,
    ClassicalList,
    Estimation,
    Histogram,
    Integer,
    Real,
    Struct,
    VQEResult,
)
from classiq.interface.generator.functions.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)
from classiq.interface.generator.functions.quantum_invoker_declaration import (
    QuantumInvokerDeclaration,
)
from classiq.interface.generator.types.builtin_struct_declarations.pauli_struct_declarations import (
    Hamiltonian,
)

SAMPLE_OPERATOR = QuantumInvokerDeclaration(
    name="sample",
    param_decls={"num_shots": Integer()},
    return_type=Histogram(),
    target_function_declaration=QuantumFunctionDeclaration(
        name="qfunc_call",
    ),
)

ESTIMATE_OPERATOR = QuantumInvokerDeclaration(
    name="estimate",
    param_decls={
        "num_shots": Integer(),
        "hamiltonian": Hamiltonian(),
    },
    return_type=Estimation(),
    target_function_declaration=QuantumFunctionDeclaration(
        name="qfunc_call",
    ),
)

QAE_WITH_QPE_POST_PROCESS_OPERATOR = ClassicalFunctionDeclaration(
    name="qae_with_qpe_result_post_processing",
    param_decls={
        "estimation_register_size": Integer(),
        "estimation_method": Integer(),
        "result": Histogram(),
    },
    return_type=Real(),
)

QSVM_FULL_RUN = QuantumInvokerDeclaration(
    name="qsvm_full_run",
    param_decls={
        "train_data": ClassicalList(element_type=ClassicalList(element_type=Real())),
        "train_labels": ClassicalList(element_type=ClassicalList(element_type=Real())),
        "test_data": ClassicalList(element_type=ClassicalList(element_type=Real())),
        "test_labels": ClassicalList(element_type=ClassicalList(element_type=Real())),
        "predict_data": ClassicalList(element_type=ClassicalList(element_type=Real())),
    },
    return_type=Struct(name="QsvmResult"),
    target_function_declaration=QuantumFunctionDeclaration(
        name="qfunc_call",
    ),
)


VQE_OPERATOR = QuantumInvokerDeclaration(
    name="vqe",
    param_decls={
        "hamiltonian": Hamiltonian(),
        "num_shots": Integer(),
        "maximize": Bool(),
        "initial_point": ClassicalList(element_type=Integer()),
        "optimizer_name": Integer(),
        "max_iteration": Integer(),
        "tolerance": Real(),
        "step_size": Real(),
        "skip_compute_variance": Bool(),
        "alpha_cvar": Real(),
    },
    return_type=VQEResult(),
    target_function_declaration=QuantumFunctionDeclaration(
        name="qfunc_call",
        param_decls={
            "runtime_params": ClassicalList(element_type=Integer()),
        },
    ),
)


ClassicalFunctionDeclaration.BUILTIN_FUNCTION_DECLARATIONS.update(
    {
        "sample": SAMPLE_OPERATOR,
        "estimate": ESTIMATE_OPERATOR,
        "qae_with_qpe_result_post_processing": QAE_WITH_QPE_POST_PROCESS_OPERATOR,
        "qsvm_full_run": QSVM_FULL_RUN,
        "vqe": VQE_OPERATOR,
    }
)
