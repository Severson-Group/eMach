from win32com.client import DispatchEx
import os

from ..tool_abc import toolabc as abc
from ..token_draw import TokenDraw


class JmagDesigner(abc.ToolBase, abc.DrawerBase, abc.MakerExtrudeBase, abc.MakerRevolveBase):
    def __init__(self):
        self.jd = None
        self.geometry_editor = None
        self.doc = None
        self.assembly = None
        self.sketch = None
        self.part = None
        self.model = None
        self.study = None
        self.view = None
        self.filename = None
        self.study_type = None
        self.default_length = None
        self.default_angle = None
        self.visible = True

    def open(self, filename, length_unit, angle_unit):

        self.default_length = length_unit
        self.default_angle = angle_unit

        file_name, file_extension = os.path.splitext(filename)

        if file_extension is not '.jproj':
            raise TypeError('Incorrect file extension')

        jd_instance = DispatchEx('designerstarter.InstanceManager')
        self.jd = jd_instance.GetNamedInstance(filename, 0)
        self.set_visibility(self.visible)

        try:
            self.jd.Load(filename)
            self.filename = filename
        except FileNotFoundError:
            self

    def save(self):
        pass

    def save_as(self, filename):
        pass

    def close(self):
        pass

    def set_visibility(self, visible):
        self.visible = visible
        if self.visible:
            self.jd.Show()
        else:
            self.jd.Hide()
