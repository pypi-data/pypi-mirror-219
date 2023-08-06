from classiq.interface.generator.functions import SynthesisNativeFunctionDefinition
from classiq.interface.generator.model import SynthesisModel as SynthesisModel
from classiq.interface.generator.quantum_function_call import (
    LambdaListComprehension as SynthesisLambdaListComprehension,
    QuantumLambdaFunction as SynthesisQuantumLambdaFunction,
    SynthesisQuantumFunctionCall,
)
from classiq.interface.generator.visitor import Transformer
from classiq.interface.model.foreign_function_definition import (
    ForeignFunctionDefinition,
)
from classiq.interface.model.model import Model
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.quantum_function_call import (
    LambdaListComprehension,
    QuantumFunctionCall,
    QuantumLambdaFunction,
)

from classiq import ForeignFunctionDefinition as SynthesisForeignFunctionDefinition

# FIXME: This class is temporary, it is a stepping stone before resolving CAD-8509
# Part of resolving that issue is merging this class and SynthesisReducer


class Converter(Transformer):
    def visit_Model(self, model: Model) -> SynthesisModel:
        return SynthesisModel(
            functions=self.visit(model.functions),
            types=self.visit(model.types),
            constants=self.visit(model.constants),
            classical_functions=self.visit(model.classical_functions),
            constraints=self.visit(model.constraints),
            execution_preferences=self.visit(model.execution_preferences),
            preferences=self.visit(model.preferences),
        )

    def visit_QuantumFunctionCall(
        self, call: QuantumFunctionCall
    ) -> SynthesisQuantumFunctionCall:
        return SynthesisQuantumFunctionCall(
            params=self.visit(call.params),
            operands=self.visit(call.operands),
            function=self.visit(call.function),
            function_params=self.visit(call.function_params),
            is_inverse=self.visit(call.is_inverse),
            assign_zero_ios=self.visit(call.assign_zero_ios),
            release_by_inverse=self.visit(call.release_by_inverse),
            control_states=self.visit(call.control_states),
            should_control=self.visit(call.should_control),
            inputs=self.visit(call.inputs),
            inouts=self.visit(call.inouts),
            outputs=self.visit(call.outputs),
            power=self.visit(call.power),
            name=self.visit(call.name),
        )

    def visit_ForeignFunctionDefinition(
        self, function: ForeignFunctionDefinition
    ) -> SynthesisForeignFunctionDefinition:
        return SynthesisForeignFunctionDefinition(
            name=self.visit(function.name),
            port_declarations=self.visit(function.port_declarations),
            register_mapping=self.visit(function.register_mapping),
            implementations=self.visit(function.implementations),
        )

    def visit_NativeFunctionDefinition(
        self, function: NativeFunctionDefinition
    ) -> SynthesisNativeFunctionDefinition:
        return SynthesisNativeFunctionDefinition(
            name=self.visit(function.name),
            param_decls=self.visit(function.param_decls),
            operand_declarations=self.visit(function.operand_declarations),
            port_declarations=self.visit(function.port_declarations),
            parameters=self.visit(function.parameters),
            input_ports_wiring=self.visit(function.input_ports_wiring),
            output_ports_wiring=self.visit(function.output_ports_wiring),
            body=self.visit(function.body),
        )

    def visit_QuantumLambdaFunction(
        self, function: QuantumLambdaFunction
    ) -> SynthesisQuantumLambdaFunction:
        return SynthesisQuantumLambdaFunction(
            rename_params=self.visit(function.rename_params),
            body=self.visit(function.body),
        )

    def visit_LambdaListComprehension(
        self, function: LambdaListComprehension
    ) -> SynthesisLambdaListComprehension:
        return SynthesisLambdaListComprehension(
            count=self.visit(function.count),
            index_var=self.visit(function.index_var),
            func=self.visit(function.func),
        )
