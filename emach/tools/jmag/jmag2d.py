from .jmag import JmagDesigner
from ...model_obj.dimensions import *

__all__ = []
__all__ += ["JmagDesigner2D"]


class JmagDesigner2D(JmagDesigner):

    def extrude(self, name, material: str, depth: float, token=None) -> any:
        """ Extrudes a cross-section by extending the model

        Args:
            name: name of the newly extruded component.
            depth: Depth of extrusion. Should be defined with eMach Dimensions.
            material : Material applied to the extruded component.

        Returns:
            Function will return the handle to the new extruded part
        """

        depth = eval(self.default_length)(depth)

        self.sketch.SetProperty('Name', name)
        self.sketch = None
        self.doc.SaveModel(True)
        model_name = name + '_model'
        self.model = self.create_model(model_name)

        study_name = name + '_study'
        self.study = self.create_study(study_name, self.study_type, self.model)
        self.study.GetStudyProperties().SetValue("ModelThickness", depth)

        self.set_default_length_unit(self.default_length)
        self.set_default_angle_unit(self.default_angle)
        self.study.SetMaterialByName(name, material)

        extrude_part = self.study.GetMaterial(name)
        return extrude_part
