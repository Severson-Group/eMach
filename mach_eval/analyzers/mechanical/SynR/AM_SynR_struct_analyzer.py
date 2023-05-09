import os
import numpy as np
import pandas as pd
import sys
from time import time as clock_time

from mach_cad import model_obj as mo
from mach_opt import InvalidDesign
from mach_cad.tools import jmag as JMAG

class AM_SynR_Struct_Problem:
    def __init__(self, machine, operating_point):
        self.machine = machine
        self.operating_point = operating_point
        self._validate_attr()

    def _validate_attr(self):
        if 'AM_SynR_Machine' in str(type(self.machine)):
            pass
        else:
            raise TypeError("Invalid machine type")

        if 'AM_SynR_Machine_Oper_Pt' in str(type(self.operating_point)):
            pass
        else:
            raise TypeError("Invalid settings type")


class AM_SynR_Struct_Analyzer:
    def __init__(self, configuration):
        self.config = configuration

    def analyze(self, problem):
        self.machine_variant = problem.machine
        self.operating_point = problem.operating_point
        
        ####################################################
        # 01 Setting project name and output folder
        ####################################################
        
        self.project_name = self.machine_variant.name
        expected_project_file = self.config.run_folder + "%s_Struct.jproj" % self.project_name
        # Create output folder
        if not os.path.isdir(self.config.jmag_csv_folder):
            os.makedirs(self.config.jmag_csv_folder)

        attempts = 1
        if os.path.exists(expected_project_file):
            print(
                "JMAG project exists already, I will not delete it but create a new one with a different name instead."
            )
            attempts = 2
            temp_path = expected_project_file[
                : -len(".jproj")
            ] + "_attempts_%d.jproj" % (attempts)
            while os.path.exists(temp_path):
                attempts += 1
                temp_path = expected_project_file[
                    : -len(".jproj")
                ] + "_attempts_%d.jproj" % (attempts)

            expected_project_file = temp_path

        if attempts > 1:
            self.project_name = self.project_name + "_attempts_%d" % (attempts)

        toolJmag = JMAG.JmagDesigner()

        toolJmag.visible = self.config.jmag_visible
        toolJmag.open(comp_filepath=expected_project_file, length_unit="DimMillimeter", study_type="StructuralStatic2D")
        toolJmag.save()

        self.study_name = self.project_name + "_Stat_AM_SynR"
        self.design_results_folder = (
            self.config.run_folder + "%s_results/" % self.project_name
        )
        if not os.path.isdir(self.design_results_folder):
            os.makedirs(self.design_results_folder)

        ################################################################
        # 02 Run Structural analysis
        ################################################################

        # Draw cross_section
        draw_success = self.draw_machine(toolJmag)
    
        if not draw_success:
            raise InvalidDesign

        toolJmag.doc.SaveModel(False)
        app = toolJmag.jd
        model = app.GetCurrentModel()

        # Pre-processing
        model.SetName(self.project_name)
        model.SetDescription(self.show(self.project_name, toString=True))

        valid_design = self.pre_process(model)

        if not valid_design:
            raise InvalidDesign

        # Create static study
        self.create_stator_material(
            app, self.machine_variant.stator_iron_mat["core_material"]
        )
        self.create_rotor_iron_material(
            app, self.machine_variant.rotor_iron_mat["rotor_iron_material"]
        )
        self.create_rotor_barrier_material(
            app, self.machine_variant.rotor_barrier_mat["rotor_barrier_material"]
        )
        app.SetCurrentStudy(self.study_name)
        study = self.add_struct_study(app, model, self.config.jmag_csv_folder, self.study_name)

        # Mesh study
        self.mesh_study(app, model, study)

        # Run study
        self.run_study(app, study, clock_time())

        toolJmag.save()
        app.Quit()

        ####################################################
        # 03 Load FEA output
        ####################################################

        fea_rated_output = self.extract_JMAG_results(
            self.config.jmag_csv_folder, self.study_name
        )

        return fea_rated_output

    @property
    def speed(self):
        return self.operating_point.speed


    def draw_machine(self, tool):
        ####################################################
        # Adding parts objects
        ####################################################

        rotor_rotation = mo.DimDegree(0)
        stator_rotation = mo.DimDegree(-180 / self.machine_variant.Q)

        self.stator_core = mo.CrossSectInnerRotorStatorPartial(
            name="StatorCore",
            dim_alpha_st=mo.DimDegree(self.machine_variant.alpha_st),
            dim_alpha_so=mo.DimDegree(self.machine_variant.alpha_so),
            dim_r_si=mo.DimMillimeter(self.machine_variant.r_si),
            dim_d_so=mo.DimMillimeter(self.machine_variant.d_so),
            dim_d_sp=mo.DimMillimeter(self.machine_variant.d_sp),
            dim_d_st=mo.DimMillimeter(self.machine_variant.d_st),
            dim_d_sy=mo.DimMillimeter(self.machine_variant.d_sy),
            dim_w_st=mo.DimMillimeter(self.machine_variant.w_st),
            dim_r_st=mo.DimMillimeter(0),
            dim_r_sf=mo.DimMillimeter(0),
            dim_r_sb=mo.DimMillimeter(0),
            Q=self.machine_variant.Q,
            location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],
            theta=stator_rotation),
            )

        self.winding_layer1 = mo.CrossSectInnerRotorStatorRightSlot(
            name="WindingLayer1",
            stator_core=self.stator_core,
            location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],
            theta=stator_rotation),
            )

        self.winding_layer2 = mo.CrossSectInnerRotorStatorLeftSlot(
            name="WindingLayer2",
            stator_core=self.stator_core,
            location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],
            theta=stator_rotation),
            )

        self.rotor_core_1i = mo.CrossSectFluxBarrierRotorAMPartial_Iron1(
            name="RotorCore1i",
            dim_r_ri=mo.DimMillimeter(self.machine_variant.r_ri),
            dim_r_ro=mo.DimMillimeter(self.machine_variant.r_ro),
            dim_d_r1=mo.DimMillimeter(self.machine_variant.d_r1),
            dim_d_r2=mo.DimMillimeter(self.machine_variant.d_r2),
            dim_w_b1=mo.DimMillimeter(self.machine_variant.w_b1),
            dim_w_b2=mo.DimMillimeter(self.machine_variant.w_b2),
            p=2,
            location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)], theta=rotor_rotation),
            )
        
        self.rotor_core_2i = mo.CrossSectFluxBarrierRotorAMPartial_Iron2(
            name="RotorCore2i",
            dim_r_ri=mo.DimMillimeter(self.machine_variant.r_ri),
            dim_r_ro=mo.DimMillimeter(self.machine_variant.r_ro),
            dim_d_r1=mo.DimMillimeter(self.machine_variant.d_r1),
            dim_d_r2=mo.DimMillimeter(self.machine_variant.d_r2),
            dim_w_b1=mo.DimMillimeter(self.machine_variant.w_b1),
            dim_w_b2=mo.DimMillimeter(self.machine_variant.w_b2),
            p=2,
            location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)], theta=rotor_rotation),
            )
        
        self.rotor_core_3i = mo.CrossSectFluxBarrierRotorAMPartial_Iron3(
            name="RotorCore3i",
            dim_r_ri=mo.DimMillimeter(self.machine_variant.r_ri),
            dim_r_ro=mo.DimMillimeter(self.machine_variant.r_ro),
            dim_d_r1=mo.DimMillimeter(self.machine_variant.d_r1),
            dim_d_r2=mo.DimMillimeter(self.machine_variant.d_r2),
            dim_w_b1=mo.DimMillimeter(self.machine_variant.w_b1),
            dim_w_b2=mo.DimMillimeter(self.machine_variant.w_b2),
            p=2,
            location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)], theta=rotor_rotation),
            )
        
        self.rotor_core_1b = mo.CrossSectFluxBarrierRotorAMPartial_Barrier1(
            name="RotorCore1b",
            dim_r_ri=mo.DimMillimeter(self.machine_variant.r_ri),
            dim_r_ro=mo.DimMillimeter(self.machine_variant.r_ro),
            dim_d_r1=mo.DimMillimeter(self.machine_variant.d_r1),
            dim_d_r2=mo.DimMillimeter(self.machine_variant.d_r2),
            dim_w_b1=mo.DimMillimeter(self.machine_variant.w_b1),
            dim_w_b2=mo.DimMillimeter(self.machine_variant.w_b2),
            p=2,
            location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)], theta=rotor_rotation),
            )
        
        self.rotor_core_2b = mo.CrossSectFluxBarrierRotorAMPartial_Barrier2(
            name="RotorCore2b",
            dim_r_ri=mo.DimMillimeter(self.machine_variant.r_ri),
            dim_r_ro=mo.DimMillimeter(self.machine_variant.r_ro),
            dim_d_r1=mo.DimMillimeter(self.machine_variant.d_r1),
            dim_d_r2=mo.DimMillimeter(self.machine_variant.d_r2),
            dim_w_b1=mo.DimMillimeter(self.machine_variant.w_b1),
            dim_w_b2=mo.DimMillimeter(self.machine_variant.w_b2),
            p=2,
            location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)], theta=rotor_rotation),
            )

        self.shaft = mo.CrossSectHollowCylinder(
            name="Shaft",
            dim_t=mo.DimMillimeter(self.machine_variant.r_ri),
            dim_r_o=mo.DimMillimeter(self.machine_variant.r_ri),
            location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)]),
            )


        self.comp_stator_core = mo.Component(
            name="StatorCore",
            cross_sections=[self.stator_core],
            material=mo.MaterialGeneric(name=self.machine_variant.stator_iron_mat["core_material"], color=r"#808080"),
            make_solid=mo.MakeExtrude(location=mo.Location3D(), 
                    dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )

        self.comp_winding_layer1 = mo.Component(
            name="WindingLayer1",
            cross_sections=[self.winding_layer1],
            material=mo.MaterialGeneric(name=self.machine_variant.coil_mat["coil_material"]),
            make_solid=mo.MakeExtrude(location=mo.Location3D(), 
            dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )

        self.comp_winding_layer2 = mo.Component(
            name="WindingLayer2",
            cross_sections=[self.winding_layer2],
            material=mo.MaterialGeneric(name=self.machine_variant.coil_mat["coil_material"]),
            make_solid=mo.MakeExtrude(location=mo.Location3D(), 
            dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )

        self.comp_rotor_core_1i = mo.Component(
            name="RotorCore1i",
            cross_sections=[self.rotor_core_1i],
            material=mo.MaterialGeneric(name=self.machine_variant.rotor_iron_mat["rotor_iron_material"], color=r"#808080"),
            make_solid=mo.MakeExtrude(location=mo.Location3D(), 
                    dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )
        
        self.comp_rotor_core_2i = mo.Component(
            name="RotorCore2i",
            cross_sections=[self.rotor_core_2i],
            material=mo.MaterialGeneric(name=self.machine_variant.rotor_iron_mat["rotor_iron_material"], color=r"#808080"),
            make_solid=mo.MakeExtrude(location=mo.Location3D(), 
                    dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )
        
        self.comp_rotor_core_3i = mo.Component(
            name="RotorCore3i",
            cross_sections=[self.rotor_core_3i],
            material=mo.MaterialGeneric(name=self.machine_variant.rotor_iron_mat["rotor_iron_material"], color=r"#808080"),
            make_solid=mo.MakeExtrude(location=mo.Location3D(), 
                    dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )
        
        self.comp_rotor_core_1b = mo.Component(
            name="RotorCore1b",
            cross_sections=[self.rotor_core_1b],
            material=mo.MaterialGeneric(name=self.machine_variant.rotor_barrier_mat["rotor_barrier_material"], color=r"#71797E"),
            make_solid=mo.MakeExtrude(location=mo.Location3D(), 
                    dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )
        
        self.comp_rotor_core_2b = mo.Component(
            name="RotorCore2b",
            cross_sections=[self.rotor_core_2b],
            material=mo.MaterialGeneric(name=self.machine_variant.rotor_barrier_mat["rotor_barrier_material"], color=r"#71797E"),
            make_solid=mo.MakeExtrude(location=mo.Location3D(), 
                    dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )
        
        self.comp_shaft = mo.Component(
            name="Shaft",
            cross_sections=[self.shaft],
            material=mo.MaterialGeneric(name=self.machine_variant.shaft_mat["shaft_material"], color=r"#71797E"),
            make_solid=mo.MakeExtrude(location=mo.Location3D(), 
                    dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )

        tool.bMirror = False

        tool.sketch = tool.create_sketch()
        tool.sketch.SetProperty("Name", self.stator_core.name)
        tool.sketch.SetProperty("Color", r"#808080")
        cs_stator = self.stator_core.draw(tool)
        stator_tool = tool.prepare_section(cs_stator, self.machine_variant.Q)

        tool.sketch = tool.create_sketch()
        tool.sketch.SetProperty("Name", self.winding_layer1.name)
        tool.sketch.SetProperty("Color", r"#B87333")
        cs_winding_layer1 = self.winding_layer1.draw(tool)
        winding_tool1 = tool.prepare_section(cs_winding_layer1, self.machine_variant.Q)
        self.winding_layer1_inner_coord = cs_winding_layer1.inner_coord

        tool.sketch = tool.create_sketch()
        tool.sketch.SetProperty("Name", self.winding_layer2.name)
        tool.sketch.SetProperty("Color", r"#B87333")
        cs_winding_layer2 = self.winding_layer2.draw(tool)
        winding_tool2 = tool.prepare_section(cs_winding_layer2, self.machine_variant.Q)
        self.winding_layer2_inner_coord = cs_winding_layer2.inner_coord

        tool.sketch = tool.create_sketch()
        tool.sketch.SetProperty("Name", self.rotor_core_1i.name)
        tool.sketch.SetProperty("Color", r"#808080")
        cs_rotor_core_1i = self.rotor_core_1i.draw(tool)
        rotor_1i_tool = tool.prepare_section(cs_rotor_core_1i, 2*self.machine_variant.p)

        tool.sketch = tool.create_sketch()
        tool.sketch.SetProperty("Name", self.rotor_core_2i.name)
        tool.sketch.SetProperty("Color", r"#808080")
        cs_rotor_core_2i = self.rotor_core_2i.draw(tool)
        rotor_2i_tool = tool.prepare_section(cs_rotor_core_2i, 2*self.machine_variant.p)

        tool.sketch = tool.create_sketch()
        tool.sketch.SetProperty("Name", self.rotor_core_3i.name)
        tool.sketch.SetProperty("Color", r"#808080")
        cs_rotor_core_3i = self.rotor_core_3i.draw(tool)
        rotor_3i_tool = tool.prepare_section(cs_rotor_core_3i, 2*self.machine_variant.p)

        tool.sketch = tool.create_sketch()
        tool.sketch.SetProperty("Name", self.rotor_core_1b.name)
        tool.sketch.SetProperty("Color", r"#71797E")
        cs_rotor_core_1b = self.rotor_core_1b.draw(tool)
        rotor_1b_tool = tool.prepare_section(cs_rotor_core_1b, 2*self.machine_variant.p)

        tool.sketch = tool.create_sketch()
        tool.sketch.SetProperty("Name", self.rotor_core_2b.name)
        tool.sketch.SetProperty("Color", r"#71797E")
        cs_rotor_core_2b = self.rotor_core_2b.draw(tool)
        rotor_2b_tool = tool.prepare_section(cs_rotor_core_2b, 2*self.machine_variant.p)

        tool.sketch = tool.create_sketch()
        tool.sketch.SetProperty("Name", self.shaft.name)
        tool.sketch.SetProperty("Color", r"#71797E")
        cs_shaft = self.shaft.draw(tool)
        shaft_tool = tool.prepare_section(cs_shaft)

        return True


    def show(self, name, toString=False):
        attrs = list(vars(self).items())
        key_list = [el[0] for el in attrs]
        val_list = [el[1] for el in attrs]
        the_dict = dict(list(zip(key_list, val_list)))
        sorted_key = sorted(
            key_list,
            key=lambda item: (
                int(item.partition(" ")[0]) if item[0].isdigit() else float("inf"),
                item,
            ),
        )  # this is also useful for string beginning with digiterations '15 Steel'.
        tuple_list = [(key, the_dict[key]) for key in sorted_key]
        if not toString:
            print("- AM SynR Individual #%s\n\t" % name, end=" ")
            print(", \n\t".join("%s = %s" % item for item in tuple_list))
            return ""
        else:
            return "\n- AM SynR Individual #%s\n\t" % name + ", \n\t".join(
                "%s = %s" % item for item in tuple_list
            )

    def pre_process(self, model):
        # pre-process : you can select part by coordinate!
        """Group"""

        def group(name, id_list):
            model.GetGroupList().CreateGroup(name)
            for the_id in id_list:
                model.GetGroupList().AddPartToGroup(name, the_id)

        part_ID_list = model.GetPartIDs()

        if len(part_ID_list) != int(
            1 + 1 + 2 * self.machine_variant.p * 4 + self.machine_variant.Q * 2 + 1
        ):
            print("Parts are missing in this machine")
            return False

        self.id_statorCore = part_ID_list[0]
        partIDRange_Coil = part_ID_list[1 : int(2 * self.machine_variant.Q + 1)]
        self.id_rotorCore = id_rotorCore = part_ID_list[int(2 * self.machine_variant.Q + 1) : int(2 * self.machine_variant.Q + 2 * self.machine_variant.p * 4 + 2) ]
        id_shaft = part_ID_list[-1]   

        group("Coils", partIDRange_Coil)
        #group("Rotor", id_rotorCore)

        """ Add Part to Set for later references """

        def add_part_to_set(name, x, y, ID=None):
            model.GetSetList().CreatePartSet(name)
            model.GetSetList().GetSet(name).SetMatcherType("Selection")
            model.GetSetList().GetSet(name).ClearParts()
            sel = model.GetSetList().GetSet(name).GetSelection()
            if ID is None:
                # print x,y
                sel.SelectPartByPosition(x, y, 0)  # z=0 for 2D
            else:
                sel.SelectPart(ID)
            model.GetSetList().GetSet(name).AddSelected(sel)

        def add_parts_to_set(name, x, y, ID=None):
            model.GetSetList().CreatePartSet(name)
            model.GetSetList().GetSet(name).SetMatcherType("Selection")
            model.GetSetList().GetSet(name).ClearParts()
            sel = model.GetSetList().GetSet(name).GetSelection()
            if ID is None:
                # print x,y
                sel.SelectPartByPosition(x, y, 0)  # z=0 for 2D
            else:
                for x in ID:
                    sel.SelectPart(x)
                model.GetSetList().GetSet(name).AddSelected(sel)

        # RotorSet
        # add_parts_to_set("RotorSet", 0.0, 0.0, ID=self.id_rotorCore)

        # StatorSet
        add_part_to_set("StatorSet", 0.0, 0.0, ID=self.id_statorCore)

        # Create Set for right layer
        Angle_StatorSlotSpan = 360 / self.machine_variant.Q
        R = np.sqrt(self.winding_layer1_inner_coord[0] ** 2 + self.winding_layer1_inner_coord[1] ** 2)
        THETA = np.arctan(self.winding_layer2_inner_coord[1] / self.winding_layer2_inner_coord[0])
        X = R * np.cos(THETA)
        Y = R * np.sin(THETA)
        count = 0
        for UVW, UpDown in zip(
            self.machine_variant.layer_phases[0], self.machine_variant.layer_polarity[0]
        ):
            count += 1
            add_part_to_set("coil_right_%s%s %d" % (UVW, UpDown, count), X, Y)

            THETA += Angle_StatorSlotSpan / 180.0 * np.pi
            X = R * np.cos(THETA)
            Y = R * np.sin(THETA)

        # Create Set for left layer
        THETA = np.arctan(self.winding_layer1_inner_coord[1] / self.winding_layer1_inner_coord[0])
        X = R * np.cos(THETA)
        Y = R * np.sin(THETA)
        count = 0
        for UVW, UpDown in zip(
            self.machine_variant.layer_phases[1], self.machine_variant.layer_polarity[1]
        ):
            count += 1
            add_part_to_set("coil_left_%s%s %d" % (UVW, UpDown, count), X, Y)

            THETA += Angle_StatorSlotSpan / 180.0 * np.pi
            X = R * np.cos(THETA)
            Y = R * np.sin(THETA)

        # Create Set for Motion Region
        def part_list_set(name, list_part_id1=None, list_part_id2=None, prefix=None):
            model.GetSetList().CreatePartSet(name)
            model.GetSetList().GetSet(name).SetMatcherType("Selection")
            model.GetSetList().GetSet(name).ClearParts()
            sel = model.GetSetList().GetSet(name).GetSelection()

            if list_part_id1 is not None:
                sel.SelectPart(list_part_id1)
            model.GetSetList().GetSet(name).AddSelected(sel)

            if list_part_id2 is not None:
                for ID in list_part_id2:
                    sel.SelectPart(ID)
            model.GetSetList().GetSet(name).AddSelected(sel)

        part_list_set(
            "Motion_Region", list_part_id1=id_shaft, list_part_id2=id_rotorCore
        )

        return True
    

    def create_stator_material(self, app, steel_name):

        core_mat_obj = app.GetMaterialLibrary().GetCustomMaterial(
            self.machine_variant.stator_iron_mat["core_material"]
        )
        app.GetMaterialLibrary().DeleteCustomMaterialByObject(core_mat_obj)

        app.GetMaterialLibrary().CreateCustomMaterial(
            self.machine_variant.stator_iron_mat["core_material"], "Custom Materials"
        )
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.stator_iron_mat["core_material"]
        ).SetValue(
            "Density", self.machine_variant.stator_iron_mat["core_material_density"] / 1000
        )
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.stator_iron_mat["core_material"]
        ).SetValue("MagneticSteelPermeabilityType", 2)
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.stator_iron_mat["core_material"]
        ).SetValue("CoerciveForce", 0)
        BH = np.loadtxt(
            self.machine_variant.stator_iron_mat["core_bh_file"],
            unpack=True,
            usecols=(0, 1),
        )  # values from Nishanth Magnet BH curve
        refarray = BH.T.tolist()
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.stator_iron_mat["core_material"]
        ).GetTable("BhTable").SetTable(refarray)
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.stator_iron_mat["core_material"]
        ).SetValue("DemagnetizationCoerciveForce", 0)
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.stator_iron_mat["core_material"]
        ).SetValue("MagnetizationSaturated", 0)
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.stator_iron_mat["core_material"]
        ).SetValue("MagnetizationSaturated2", 0)
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.stator_iron_mat["core_material"]
        ).SetValue("ExtrapolationMethod", 0)
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.stator_iron_mat["core_material"]
        ).SetValue(
            "YoungModulus", self.machine_variant.stator_iron_mat["core_youngs_modulus"] / 1000000
        )
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.stator_iron_mat["core_material"]
        ).SetValue("Loss_Type", 1)
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.stator_iron_mat["core_material"]
        ).SetValue(
            "LossConstantKhX", self.machine_variant.stator_iron_mat["core_ironloss_Kh"]
        )
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.stator_iron_mat["core_material"]
        ).SetValue(
            "LossConstantKeX", self.machine_variant.stator_iron_mat["core_ironloss_Ke"]
        )
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.stator_iron_mat["core_material"]
        ).SetValue(
            "LossConstantAlphaX",
            self.machine_variant.stator_iron_mat["core_ironloss_a"],
        )
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.stator_iron_mat["core_material"]
        ).SetValue(
            "LossConstantBetaX", self.machine_variant.stator_iron_mat["core_ironloss_b"]
        )


    def create_rotor_iron_material(self, app, steel_name):

        core_mat_obj = app.GetMaterialLibrary().GetCustomMaterial(
            self.machine_variant.rotor_iron_mat["rotor_iron_material"]
        )
        app.GetMaterialLibrary().DeleteCustomMaterialByObject(core_mat_obj)

        app.GetMaterialLibrary().CreateCustomMaterial(
            self.machine_variant.rotor_iron_mat["rotor_iron_material"], "Custom Materials"
        )
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_iron_mat["rotor_iron_material"]
        ).SetValue(
            "Density", self.machine_variant.rotor_iron_mat["rotor_iron_material_density"] / 1000
        )
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_iron_mat["rotor_iron_material"]
        ).SetValue("MagneticSteelPermeabilityType", 2)
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_iron_mat["rotor_iron_material"]
        ).SetValue("CoerciveForce", 0)
        BH = np.loadtxt(
            self.machine_variant.rotor_iron_mat["rotor_iron_bh_file"],
            unpack=True,
            usecols=(0, 1),
        )  # values from Dante Magnet BH curve
        refarray = BH.T.tolist()
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_iron_mat["rotor_iron_material"]
        ).GetTable("BhTable").SetTable(refarray)
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_iron_mat["rotor_iron_material"]
        ).SetValue("DemagnetizationCoerciveForce", 0)
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_iron_mat["rotor_iron_material"]
        ).SetValue("MagnetizationSaturated", 0)
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_iron_mat["rotor_iron_material"]
        ).SetValue("MagnetizationSaturated2", 0)
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_iron_mat["rotor_iron_material"]
        ).SetValue("ExtrapolationMethod", 0)
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_iron_mat["rotor_iron_material"]
        ).SetValue(
            "YoungModulus", self.machine_variant.rotor_iron_mat["rotor_iron_youngs_modulus"] / 1000000
        )
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_iron_mat["rotor_iron_material"]
        ).SetValue("Loss_Type", 1)
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_iron_mat["rotor_iron_material"]
        ).SetValue(
            "LossConstantKhX", self.machine_variant.rotor_iron_mat["rotor_iron_ironloss_Kh"]
        )
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_iron_mat["rotor_iron_material"]
        ).SetValue(
            "LossConstantKeX", self.machine_variant.rotor_iron_mat["rotor_iron_ironloss_Ke"]
        )
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_iron_mat["rotor_iron_material"]
        ).SetValue(
            "LossConstantAlphaX",
            self.machine_variant.rotor_iron_mat["rotor_iron_ironloss_a"],
        )
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_iron_mat["rotor_iron_material"]
        ).SetValue(
            "LossConstantBetaX", self.machine_variant.rotor_iron_mat["rotor_iron_ironloss_b"]
        )


    def create_rotor_barrier_material(self, app, steel_name):

        core_mat_obj = app.GetMaterialLibrary().GetCustomMaterial(
            self.machine_variant.rotor_barrier_mat["rotor_barrier_material"]
        )
        app.GetMaterialLibrary().DeleteCustomMaterialByObject(core_mat_obj)

        app.GetMaterialLibrary().CreateCustomMaterial(
            self.machine_variant.rotor_barrier_mat["rotor_barrier_material"], "Custom Materials"
        )
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_barrier_mat["rotor_barrier_material"]
        ).SetValue(
            "Density", self.machine_variant.rotor_barrier_mat["rotor_barrier_material_density"] / 1000
        )
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_barrier_mat["rotor_barrier_material"]
        ).SetComplexValue("Permeability", self.machine_variant.rotor_barrier_mat["rotor_barrier_permeability"], 0)

        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_barrier_mat["rotor_barrier_material"]
        ).SetValue("CoerciveForce", 0)
        
        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_barrier_mat["rotor_barrier_material"]
        ).SetValue("DemagnetizationCoerciveForce", 0)

        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_barrier_mat["rotor_barrier_material"]
        ).SetValue("MagnetizationSaturated", 0)

        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_barrier_mat["rotor_barrier_material"]
        ).SetValue("MagnetizationSaturated2", 0)

        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_barrier_mat["rotor_barrier_material"]
        ).SetValue(
            "YoungModulus", self.machine_variant.rotor_barrier_mat["rotor_barrier_youngs_modulus"] / 1000000
        )

        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_barrier_mat["rotor_barrier_material"]
        ).SetValue(
            "PoissonRatio", self.machine_variant.rotor_barrier_mat["rotor_barrier_poission_ratio"]
        )

        app.GetMaterialLibrary().GetUserMaterial(
            self.machine_variant.rotor_barrier_mat["rotor_barrier_material"]
        ).SetValue("ShearModulus", self.machine_variant.rotor_barrier_mat["rotor_barrier_shear_modulus"] / 1000000)


    def add_struct_study(
        self, app, model, dir_csv_output_folder, study_name
    ):

        model.CreateStudy("StructuralStatic2D", study_name)
        app.SetCurrentStudy(self.study_name)
        study = model.GetStudy(study_name)

        # Study properties
        study.GetStudyProperties().SetValue(
            "ModelThickness", self.machine_variant.l_st
        )  # [mm] Stack Length

        # Material
        self.add_materials(study)

        # Conditions - Displacement Restraint
        study.CreateCondition("Displacement", "Containment")
        study.GetCondition("Containment").SetXYZPoint("Direction", 0, 0, 1)
        study.GetCondition("Containment").ClearParts()
        study.GetCondition("Containment").AddSet(
            model.GetSetList().GetSet("Motion_Region"), 1
        )

        # Conditions - Centrifugal Force
        study.CreateCondition("CentrifugalForce",
            "RotCon") 
        study.GetCondition("RotCon").SetXYZPoint("Axis", 0, 0, 1) # megbox warning
        study.GetCondition("RotCon").SetValue("AngularVelocity",
            int(self.speed))
        study.GetCondition("RotCon").ClearParts()
        study.GetCondition("RotCon").AddSet(
            model.GetSetList().GetSet("Motion_Region"), 0
        )

        # Conditions - Target Result
        app.SetCurrentStudy(self.study_name)
        model.GetStudy(self.study_name).CreateCalculationDefinition("MaxStress")
        model.GetStudy(self.study_name).GetCalculationDefinition("MaxStress").SetResultType("MisesStress", "")
        model.GetStudy(self.study_name).GetCalculationDefinition("MaxStress").SetResultCoordinate("Global Rectangular")
        model.GetStudy(self.study_name).GetCalculationDefinition("MaxStress").SetCalculationType("max")
        model.GetStudy(self.study_name).GetCalculationDefinition("MaxStress").SetDirectionAxis(0, 0, 1)
        model.GetStudy(self.study_name).GetCalculationDefinition("MaxStress").ClearParts()
        model.GetStudy(self.study_name).GetCalculationDefinition("MaxStress").AddSet(
            model.GetSetList().GetSet("Motion_Region"), 0
        )

        # Suppress Stator
        model.GetStudy(self.study_name).SuppressPart("StatorCore", 1)
        model.GetStudy(self.study_name).SuppressPart("Coils", 1)

        # True: no mesh or field results are needed
        study.GetStudyProperties().SetValue(
            "OnlyTableResults", self.config.only_table_results
        )

        study.GetStudyProperties().SetValue("DirectSolverType", 1)

        if self.config.multiple_cpus:
            # This SMP(shared memory process) is effective only if there are tons of elements. e.g., over 100,000.
            # too many threads will in turn make them compete with each other and slow down the solve. 2 is good enough
            # for eddy current solve. 6~8 is enough for transient solve.
            study.GetStudyProperties().SetValue("UseMultiCPU", True)
            study.GetStudyProperties().SetValue("MultiCPU", self.config.num_cpus)

        # speed, freq
        study.GetCondition("RotCon").SetValue("AngularVelocity", "speed")

        # Calculate CSV results
        study.GetStudyProperties().SetValue(
            "CsvOutputPath", dir_csv_output_folder
        )  # it's folder rather than file!
        study.GetStudyProperties().SetValue(self.config.csv_results,1)
        study.GetStudyProperties().SetValue(
            "DeleteResultFiles", self.config.del_results_after_calc
        )

        return study


    def add_materials(self, study):
        # if 'M19' in self.machine_variant.stator_iron_mat["core_material"]:
        # study.SetMaterialByName(self.comp_stator_core.name, "M-19 Steel Gauge-29")
        # study.GetMaterial(self.comp_stator_core.name).SetValue("Laminated", 1)
        # study.GetMaterial(self.comp_stator_core.name).SetValue("LaminationFactor",
        #     self.machine_variant.stator_iron_mat["core_stacking_factor"])

        # study.SetMaterialByName(self.comp_rotor_core.name, "M-19 Steel Gauge-29")
        # study.GetMaterial(self.comp_rotor_core.name).SetValue("Laminated", 1)
        # study.GetMaterial(self.comp_rotor_core.name).SetValue("LaminationFactor",
        #     self.machine_variant.rotor_iron_mat["core_stacking_factor"])

        study.SetMaterialByName(self.comp_stator_core.name,
            self.machine_variant.stator_iron_mat["core_material"])
        study.GetMaterial(self.comp_stator_core.name).SetValue("Laminated", 1)
        study.GetMaterial(self.comp_stator_core.name).SetValue("LaminationFactor",
            self.machine_variant.stator_iron_mat["core_stacking_factor"])

        study.SetMaterialByName(self.comp_rotor_core_1i.name, 
            self.machine_variant.rotor_iron_mat["rotor_iron_material"])
        study.GetMaterial(self.comp_rotor_core_1i.name).SetValue("Laminated", 0)
        
        study.SetMaterialByName(self.comp_rotor_core_2i.name, 
            self.machine_variant.rotor_iron_mat["rotor_iron_material"])
        study.GetMaterial(self.comp_rotor_core_2i.name).SetValue("Laminated", 0)

        study.SetMaterialByName(self.comp_rotor_core_3i.name, 
            self.machine_variant.rotor_iron_mat["rotor_iron_material"])
        study.GetMaterial(self.comp_rotor_core_3i.name).SetValue("Laminated", 0)
        
        study.SetMaterialByName(self.comp_rotor_core_1b.name,
            self.machine_variant.rotor_barrier_mat["rotor_barrier_material"])
        study.GetMaterial(self.comp_rotor_core_1b.name).SetValue("Laminated", 0)

        study.SetMaterialByName(self.comp_rotor_core_2b.name,
            self.machine_variant.rotor_barrier_mat["rotor_barrier_material"])
        study.GetMaterial(self.comp_rotor_core_2b.name).SetValue("Laminated", 0)
        
        study.SetMaterialByName(self.comp_shaft.name,
            self.machine_variant.shaft_mat["shaft_material"])
        study.GetMaterial(self.comp_shaft.name).SetValue("Laminated", 0)
        study.GetMaterial(self.comp_shaft.name).SetValue("EddyCurrentCalculation", 1)

        study.SetMaterialByName(self.comp_winding_layer1.name, 
            self.machine_variant.coil_mat["coil_material"])
        study.GetMaterial(self.comp_shaft.name).SetValue("UserConductivityType", 1)
        

    def mesh_study(self, app, model, study):

        # mesh
        print("------------------Adding mesh")
        self.add_mesh(study, model)

        # Export Image
        app.View().ShowAllAirRegions()
        app.View().ShowMesh()
        app.View().Zoom(3)
        app.View().Pan(-self.machine_variant.r_si / 1000, 0)
        app.ExportImageWithSize(
            self.design_results_folder + self.project_name + "mesh.png", 2000, 2000
        )
        app.View().ShowModel()


    def add_mesh(self, study, model):
        # this is for multi slide planes, which we will not be usin
        refarray = [[0 for i in range(2)] for j in range(1)]
        refarray[0][0] = 3
        refarray[0][1] = 1
        study.GetMeshControl().GetTable("SlideTable2D").SetTable(refarray)

        study.GetMeshControl().SetValue("MeshType", 1)  # make sure this has been exe'd:
        study.GetMeshControl().SetValue(
            "RadialDivision", self.config.airgap_mesh_radial_div
        )  # for air region near which motion occurs
        study.GetMeshControl().SetValue(
            "CircumferentialDivision", self.config.airgap_mesh_circum_div
        )  # 1440) # for air region near which motion occurs
        study.GetMeshControl().SetValue(
            "AirRegionScale", self.config.mesh_air_region_scale
        )  # [Model Length]: Specify a value within (1.05 <= value < 1000)
        study.GetMeshControl().SetValue("MeshSize", self.config.mesh_size/5)
        study.GetMeshControl().SetValue("AutoAirMeshSize", 0)
        study.GetMeshControl().SetValue(
            "AirMeshSize", self.config.mesh_size_rotor
        )  # mm
        study.GetMeshControl().SetValue("Adaptive", 0)

        study.GetMeshControl().CreateCondition("RotationPeriodicMeshAutomatic", 
                "autoRotMesh") # with this you can choose to set CircumferentialDivision automatically

        study.GetMeshControl().CreateCondition("Part", "ShaftMeshCtrl")
        study.GetMeshControl().GetCondition("ShaftMeshCtrl").SetValue("Size", 1) # 10 mm
        study.GetMeshControl().GetCondition("ShaftMeshCtrl").ClearParts()
        study.GetMeshControl().GetCondition("ShaftMeshCtrl").AddSet(model.GetSetList().GetSet("ShaftSet"), 0)

        def mesh_all_cases(study):
            numCase = study.GetDesignTable().NumCases()
            for case in range(0, numCase):
                study.SetCurrentCase(case)
                if not study.HasMesh():
                    study.CreateMesh()

        mesh_all_cases(study)


    def run_study(self, app, study, toc):
        if not self.config.jmag_scheduler:
            print("-----------------------Running JMAG...")
            study.RunAllCases()
            msg = "Time spent on %s is %g s." % (study.GetName(), clock_time() - toc)
            print(msg)
        else:
            print("Submit to JMAG_Scheduler...")
            job = study.CreateJob()
            job.SetValue("Title", study.GetName())
            job.SetValue("Queued", True)
            job.Submit(False)  # False:CurrentCase, True:AllCases
            # wait and check
        
        app.Save()


    def prepare_section(
        self, list_regions, tool, bMirrorMerge=True, bRotateMerge=True
    ):  # csToken is a list of cross section's token

        def regionCircularPattern360Origin(region, tool, bMerge=True):
            # index is used to define name of region

            Q_float = float(tool.iRotateCopy)  # don't ask me, ask JSOL
            circular_pattern = tool.sketch.CreateRegionCircularPattern()
            circular_pattern.SetProperty("Merge", bMerge)

            ref2 = tool.doc.CreateReferenceFromItem(region)
            circular_pattern.SetPropertyByReference("Region", ref2)
            face_region_string = circular_pattern.GetProperty("Region")

            circular_pattern.SetProperty("CenterType", 2)  # origin I guess

            # print('Copy', Q_float)
            circular_pattern.SetProperty("Angle", "360/%d" % Q_float)
            circular_pattern.SetProperty("Instance", str(Q_float))

        list_region_objects = []
        for idx, list_segments in enumerate(list_regions):
            # Region
            tool.doc.GetSelection().Clear()
            for segment in list_segments:
                tool.doc.GetSelection().Add(tool.sketch.GetItem(segment.draw_token.GetName()))

            tool.sketch.CreateRegions()

            if idx == 0:
                region_object = tool.sketch.GetItem(
                    "Region"
                )  # This is how you get access to the region you create.
            else:
                region_object = tool.sketch.GetItem(
                    "Region.%d" % (idx + 1)
                )  # This is how you get access to the region you create.
            list_region_objects.append(region_object)
        # raise

        for idx, region_object in enumerate(list_region_objects):
            # Mirror
            if tool.bMirror == True:
                if tool.edge4Ref is None:
                    tool.regionMirrorCopy(
                        region_object,
                        edge4Ref=None,
                        symmetryType=2,
                        bMerge=bMirrorMerge,
                    )  # symmetryType=2 means x-axis as ref
                else:
                    tool.regionMirrorCopy(
                        region_object,
                        edge4Ref=tool.edge4ref,
                        symmetryType=None,
                        bMerge=bMirrorMerge,
                    )  # symmetryType=2 means x-axis as ref

            # RotateCopy
            if tool.iRotateCopy != 0:
                regionCircularPattern360Origin(
                    region_object, tool, bMerge=bRotateMerge
                )

        tool.sketch.CloseSketch()
        return list_region_objects

    def extract_JMAG_results(self, path, study_name):
        max_stress_csv_path = path + study_name + "_calculation_MaxStress.csv"
        max_stress_df = pd.read_csv(max_stress_csv_path, skiprows=5)
        
        fea_data = {
            "max_stress": max_stress_df,
        }

        return fea_data