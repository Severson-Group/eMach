import sys

sys.path.append("..")

import emach.tools.jmag as jd
import emach.model_obj as mo
import numpy as np

rotor1 = mo.CrossSectInnerReluctanceRotor(name='rotor',
                                       dim_alpha_rpi=mo.DimDegree(30),
                                       dim_alpha_rpo=mo.DimDegree(20),
                                       dim_r_ri=mo.DimMillimeter(4),
                                       dim_d_ri=mo.DimMillimeter(16),
                                       dim_d_rp=mo.DimMillimeter(15),
                                       dim_r_if=mo.DimMillimeter(1),
                                       dim_r_of=mo.DimMillimeter(1),     
                                       Q_r =8,
                                       location=mo.Location2D())

comp1 = mo.Component(
    name='Rotor',
    cross_sections=[rotor1],
    material=mo.MaterialGeneric(name="Silicon Steel"),
    make_solid=mo.MakeExtrude(location=mo.Location3D(),
                            dim_depth=mo.DimMillimeter(25)))

file = r'Inner_Reluctance_Rotor.jproj'

tool_jmag = jd.JmagDesigner()
tool_jmag.open(comp_filepath=file)
tool_jmag.set_visibility(True)

comp1.make(tool_jmag, tool_jmag)

tool_jmag.save()
