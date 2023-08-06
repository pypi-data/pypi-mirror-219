from classiq.interface.generator.model.model import SerializedModel
from classiq.interface.model.converter import Converter
from classiq.interface.model.model import Model

# This is a utility function which will be removed after the PR fixing CAD-8509
# The reason it exists is that making this function a method of `UserModel`
# causes a circular dependency between Converter and UserModel
# After that issue is fixed, Converter will be removed and joined with SynthesisReducer


def get_model(model: Model) -> SerializedModel:
    synthesis_model = Converter().visit(model)
    return synthesis_model.get_model()
