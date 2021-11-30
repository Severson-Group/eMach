import sys

sys.path.append("..")

import emach.tools.jmag as jd
import emach.model_obj as mo

stator1 = mo.CrossSectInnerRotorStator(
    name='stator',
    dim_alpha_st=mo.DimDegree(44.5),
    dim_alpha_so=mo.DimDegree((44.5 / 2)),
    dim_r_si=mo.DimMillimeter(14.16),
    dim_d_sy=mo.DimMillimeter(13.54),
    dim_d_st=mo.DimMillimeter(16.94),
    dim_d_sp=mo.DimMillimeter(8.14),
    dim_d_so=mo.DimMillimeter(5.43),
    dim_w_st=mo.DimMillimeter(9.1),
    dim_r_st=mo.DimMillimeter(0),
    dim_r_sf=mo.DimMillimeter(0),
    dim_r_sb=mo.DimMillimeter(0),
    Q=6,
    location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)]),
    theta=mo.DimDegree(0))

rotor1 = mo.CrossSectInnerNotchedRotor(name='rotor',
                                       location=mo.Location2D(),
                                       dim_alpha_rm=mo.DimDegree(180),
                                       dim_alpha_rs=mo.DimDegree(90),
                                       dim_d_ri=mo.DimMillimeter(3),
                                       dim_r_ri=mo.DimMillimeter(5),
                                       dim_d_rp=mo.DimMillimeter(5),
                                       dim_d_rs=mo.DimMillimeter(3),
                                       p=1, s=2)

magnet1 = mo.CrossSectArc(name='magnet1', location=mo.Location2D(),
                          dim_d_a=mo.DimMillimeter(3.41), dim_r_o=mo.DimMillimeter(11.41), dim_alpha=mo.DimDegree(90))

magnet2 = mo.CrossSectArc(name='magnet2', location=mo.Location2D(theta=mo.DimDegree(90)),
                          dim_d_a=mo.DimMillimeter(3.41), dim_r_o=mo.DimMillimeter(11.41), dim_alpha=mo.DimDegree(90))

magnet3 = mo.CrossSectArc(name='magnet3', location=mo.Location2D(theta=mo.DimDegree(180)),
                          dim_d_a=mo.DimMillimeter(3.41), dim_r_o=mo.DimMillimeter(11.41), dim_alpha=mo.DimDegree(90))

magnet4 = mo.CrossSectArc(name='magnet4', location=mo.Location2D(theta=mo.DimDegree(270)),
                          dim_d_a=mo.DimMillimeter(3.41), dim_r_o=mo.DimMillimeter(11.41), dim_alpha=mo.DimDegree(90))


comp1 = mo.Component(
    name='Stator',
    cross_sections=[stator1],
    material=mo.MaterialGeneric(name="10JNEX900"),
    make_solid=mo.MakeExtrude(location=mo.Location3D(),
                                dim_depth=mo.DimMillimeter(25)))

comp2 = mo.Component(
    name='Rotor',
    cross_sections=[rotor1],
    material=mo.MaterialGeneric(name="10JNEX900"),
    make_solid=mo.MakeExtrude(location=mo.Location3D(),
                                dim_depth=mo.DimMillimeter(25)))

comp3 = mo.Component(
    name='Magnet1',
    cross_sections=[magnet1],
    material=mo.MaterialGeneric(name="Arnold/Reversible/N40H"),
    make_solid=mo.MakeExtrude(location=mo.Location3D(),
                                dim_depth=mo.DimMillimeter(25)))

comp4 = mo.Component(
    name='Magnet2',
    cross_sections=[magnet2],
    material=mo.MaterialGeneric(name="Arnold/Reversible/N40H"),
    make_solid=mo.MakeExtrude(location=mo.Location3D(),
                                dim_depth=mo.DimMillimeter(25)))

comp5 = mo.Component(
    name='Magnet3',
    cross_sections=[magnet3],
    material=mo.MaterialGeneric(name="Arnold/Reversible/N40H"),
    make_solid=mo.MakeExtrude(location=mo.Location3D(),
                                dim_depth=mo.DimMillimeter(25)))

comp6 = mo.Component(
    name='Magnet4',
    cross_sections=[magnet4],
    material=mo.MaterialGeneric(name="Arnold/Reversible/N40H"),
    make_solid=mo.MakeExtrude(location=mo.Location3D(),
                                dim_depth=mo.DimMillimeter(25)))

file = r'full_SPM_4pole2D.jproj'

tool_jmag = jd.JmagDesigner2D()
tool_jmag.open(comp_filepath=file, study_type='Transient2D')
tool_jmag.set_visibility(False)

stator_tool = comp1.make(tool_jmag, tool_jmag)
rotor_tool = comp2.make(tool_jmag, tool_jmag)
magnet1_tool = comp3.make(tool_jmag, tool_jmag)
magnet2_tool = comp4.make(tool_jmag, tool_jmag)
magnet3_tool = comp5.make(tool_jmag, tool_jmag)
magnet4_tool = comp6.make(tool_jmag, tool_jmag)

tool_jmag.save()
