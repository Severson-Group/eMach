import sys

sys.path.append("..")

import emach.tools.jmag as jd
import emach.model_obj as mo
import numpy as np

rotor1 = mo.CrossSectFluxBarrierRotor(name='rotor',
                                       dim_alpha_b=mo.DimDegree(135),
                                       dim_r_ri=mo.DimMillimeter(6),
                                       dim_r_ro=mo.DimMillimeter(50),
                                       dim_r_f1=mo.DimMillimeter(0.3),
                                       dim_r_f2=mo.DimMillimeter(0.3),
                                       dim_r_f3=mo.DimMillimeter(0.2),
                                       dim_d_r1=mo.DimMillimeter(4),
                                       dim_d_r2=mo.DimMillimeter(4),
                                       dim_d_r3=mo.DimMillimeter(4),
                                       dim_w_b1=mo.DimMillimeter(4),
                                       dim_w_b2=mo.DimMillimeter(4),
                                       dim_w_b3=mo.DimMillimeter(4),
                                       dim_l_b1=mo.DimMillimeter(18),
                                       dim_l_b2=mo.DimMillimeter(15),
                                       dim_l_b3=mo.DimMillimeter(12),
                                       dim_l_b4=mo.DimMillimeter(18),
                                       dim_l_b5=mo.DimMillimeter(15),
                                       dim_l_b6=mo.DimMillimeter(12),
                                       p =2,
                                       location=mo.Location2D())

comp1 = mo.Component(
    name='Rotor',
    cross_sections=[rotor1],
    material=mo.MaterialGeneric(name="Silicon Steel"),
    make_solid=mo.MakeExtrude(location=mo.Location3D(),
                            dim_depth=mo.DimMillimeter(25)))

file = r'Flux_Barrier_Rotor.jproj'

tool_jmag = jd.JmagDesigner()
tool_jmag.open(comp_filepath=file)
tool_jmag.set_visibility(True)

comp1.make(tool_jmag, tool_jmag)
tool_jmag.save()
