import os
import numpy as np
import pandas as pd
import sys
import femm
import subprocess
from time import sleep
from time import time as clock_time
import logging
import operator
import win32com.client

sys.path.append(os.path.dirname(__file__) + "/../../../..")
from mach_cad.model_obj.cross_sects import (
    CrossSectInnerRotorStator, CrossSectInnerRotorRoundSlots
)
import mach_cad.model_obj as mo
import mach_cad.tools.jmag as JMAG

from mach_opt import InvalidDesign


class BIM_Transient_2TSS_Problem:
    def __init__(self, machine, operating_point, breakdown_slip_freq=None):
        self.machine = machine
        self.operating_point = operating_point
        self.breakdown_slip_freq = breakdown_slip_freq
        self._validate_attr()

    def _validate_attr(self):
        if 'BIM_Machine' in str(type(self.machine)):
            pass
        else:
            raise TypeError("Invalid machine type")

        if 'BIM_Machine_Oper_Pt' in str(type(self.operating_point)):
            pass
        else:
            raise TypeError("Invalid settings type")


class BIM_Transient_2TSS_Analyzer:
    def __init__(self, configuration):
        self.config = configuration

    def analyze(self, problem):
        self.machine_variant = problem.machine
        self.operating_point = problem.operating_point
        self.breakdown_slip_freq = problem.breakdown_slip_freq
        ####################################################
        # 01 Setting project name and output folder
        ####################################################
        self.project_name = self.machine_variant.name
        # expected_project_file = self.config.run_folder + "%s_attempts_2.jproj" % self.project_name
        expected_project_file = self.config.run_folder + "%s.jproj" % self.project_name
        # Create output folder
        if not os.path.isdir(self.config.jmag_csv_folder):
            os.makedirs(self.config.jmag_csv_folder)

        attempts = 1
        if os.path.exists(expected_project_file):
            print(
                "JMAG project exists already, I will not delete it but create a new one with a different name instead."
            )
            # os.remove(expected_project_file_path)
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
        # toolJmag.defaultUnit = "Millimeter"
        # toolJmag.default_length = "Millimeter"

        toolJmag.study_type = "Transient2D"
        toolJmag.open(comp_filepath=expected_project_file, length_unit="DimMillimeter")
        toolJmag.save()
        # toolJmag.open(comp_filepath="example_machine_attempts_2.jproj")

        self.study_name = self.project_name + "_Tran_2TSS_BIM"
        self.design_results_folder = (
            self.config.run_folder + "%s_results/" % self.project_name
        )
        if not os.path.isdir(self.design_results_folder):
            os.makedirs(self.design_results_folder)

        ################################################################
        # 02 Run ElectroMagnetic analysis
        ################################################################
        # Draw cross_section
        draw_success = self.draw_machine(toolJmag)
        if not draw_success:
            raise InvalidDesign
        toolJmag.doc.SaveModel(False)
        toolJmag.model = toolJmag.jd.GetCurrentModel()
        # app = win32com.client.Dispatch("designer.Application")
        # if self.config.jmag_visible == True:
        #     app.Show()
        # else:
        #     app.Hide()
        
        # app.Quit()
        # self.app = app  # means that the JMAG Designer is turned ON now.

        # Pre-processing
        toolJmag.model.SetName(self.project_name)
        toolJmag.model.SetDescription(self.show(self.project_name, toString=True))
        
        # model.SetDescription(self.show(self.project_name, toString=True))
        valid_design = self.pre_process(toolJmag.model)
        if not valid_design:
            raise InvalidDesign
        
        # Create transient study with two time step sections
        toolJmag = self.add_transient_2tss_study(toolJmag)
        # self.create_custom_material(
        #     toolJmag.jd, self.machine_variant.stator_iron_mat["core_material"]
        # )
        toolJmag.jd.SetCurrentStudy(self.study_name)
        toolJmag.study = toolJmag.jd.GetCurrentStudy()

        # Mesh study
        self.mesh_study(toolJmag.jd, toolJmag.model, toolJmag.study)

        # Set slip
        toolJmag.study.GetDesignTable().GetEquation("slip").SetExpression("%g"%(self.slip))

        # toolJmag.jd = win32com.client.Dispatch("designer.Application")
        self.run_study(toolJmag.jd, toolJmag.study, clock_time())

        toolJmag.save()
        toolJmag.jd.Quit()
        ####################################################
        # 03 Load FEA output
        ####################################################

        fea_rated_output = self.extract_JMAG_results(
            self.config.jmag_csv_folder, self.study_name
        )

        return fea_rated_output


    @property
    def slip_freq(self):
        if self.breakdown_slip_freq == None:
            slip_freq = self.operating_point.slip_freq  
        else:
            slip_freq = self.breakdown_slip_freq
        return slip_freq

    @property
    def drive_freq(self):
        speed_in_elec_ang = self.operating_point.speed / 60 * self.machine_variant.p
        drive_freq = speed_in_elec_ang + self.slip_freq
        return drive_freq

    # @property
    # def drive_freq(self):
    #     return self.operating_point.drive_freq

    @property
    def speed(self):
        return self.operating_point.speed

    @property
    def slip(self):
        slip = self.slip_freq / self.drive_freq
        return slip

    @property
    def elec_omega(self):
        return 2 * np.pi * self.drive_freq

    @property
    def It_hat(self):
        return self.operating_point.It_hat

    @property
    def Is_hat(self):
        return self.operating_point.Is_hat

    @property
    def phi_t_0(self):
        return self.operating_point.phi_t_0

    @property
    def phi_s_0(self):
        return self.operating_point.phi_s_0

    @property
    def R_end_ring(self):
        if self.config.non_zero_end_ring_res == True:
            R_end_ring = self.machine_variant.R_end_ring
        else:
            R_end_ring = 0

        return R_end_ring

    @property
    def l_coil(self):
        l_coil = self.machine_variant.l_coil
        return l_coil

    @property
    def R_coil(self):
        R_coil = self.machine_variant.R_coil
        return R_coil

    @property
    def l_coil_end_wdg(self):
        l_coil_end_wdg = self.machine_variant.l_coil_end_wdg
        return l_coil_end_wdg

    # @property
    # def R_coil(self):
    #     R_coil = self.machine_variant.R_coil
    #     return R_coil

    @property
    def R_coil_end_wdg(self):
        R_coil_end_wdg = self.machine_variant.R_coil_end_wdg
        return R_coil_end_wdg

    @property
    def z_C(self):
        if len(self.machine_variant.layer_phases) == 1:
            z_C = self.machine_variant.Q / (2 * self.machine_variant.no_of_phases)
        elif len(self.machine_variant.layer_phases) == 2:
            z_C = self.machine_variant.Q / (self.machine_variant.no_of_phases)

        return z_C

    @property
    def stator_calc_ohmic_loss(self):
        R_ph = self.R_coil * self.z_C
        m = self.machine_variant.no_of_phases
        stator_calc_ohmic_loss = R_ph * m / 2 * (self.operating_point.It_hat ** 2 + self.operating_point.Is_hat**2)

        return stator_calc_ohmic_loss

    @property
    def stator_calc_ohmic_loss_end_wdg(self):
        R_ph = self.R_coil_end_wdg * self.z_C
        m = self.machine_variant.no_of_phases
        stator_calc_ohmic_loss_end_wdg = R_ph * m / 2 * (self.operating_point.It_hat ** 2 + self.operating_point.Is_hat**2)

        return stator_calc_ohmic_loss_end_wdg

    @property
    def stator_calc_ohmic_loss_along_stack(self):
        stator_calc_ohmic_loss_along_stack = self.stator_calc_ohmic_loss - self.stator_calc_ohmic_loss_end_wdg
        return stator_calc_ohmic_loss_along_stack



    def draw_machine(self, tool):
        ####################################################
        # Adding parts objects
        ####################################################
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
            theta=mo.DimRadian(0)),
            )

        self.winding_layer1 = mo.CrossSectInnerRotorStatorRightSlot(
            name="WindingLayer1",
            stator_core=self.stator_core,
            location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],
            theta=mo.DimRadian(0)),
            )

        # self.winding_layer1 = []
        # for i in range (0, self.machine_variant.Q):
        #     self.winding_layer1.append(mo.CrossSectInnerRotorStatorRightSlot(
        #         name="WindingLayer1",
        #         stator_core=self.stator_core,
        #         location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],
        #         theta=mo.DimRadian(2 * np.pi / self.machine_variant.Q * i)),
        #         ))

        self.winding_layer2 = mo.CrossSectInnerRotorStatorLeftSlot(
            name="WindingLayer2",
            stator_core=self.stator_core,
            location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],
            theta=mo.DimRadian(0)),
            )

        # self.winding_layer2 = []
        # for i in range (0, 1):
        #     self.winding_layer2.append(mo.CrossSectInnerRotorStatorLeftSlot(
        #         name="WindingLayer2",
        #         stator_core=self.stator_core,
        #         location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],
        #         theta=mo.DimRadian(2 * np.pi / self.machine_variant.Q * i)),
        #         ))

        self.rotor_core = mo.CrossSectInnerRotorRoundSlotsPartial(
            name="RotorCore",
            dim_r_ri=mo.DimMillimeter(self.machine_variant.r_ri),
            dim_d_ri=mo.DimMillimeter(self.machine_variant.d_ri),
            dim_r_rb=mo.DimMillimeter(self.machine_variant.r_rb),
            dim_d_so=mo.DimMillimeter(self.machine_variant.d_rso),
            dim_w_so=mo.DimMillimeter(self.machine_variant.w_so),
            Qr=self.machine_variant.Qr,
            location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)]),
            )

        self.rotor_bar = mo.CrossSectInnerRotorRoundSlotsBar(
            name="RotorBar",
            rotor_core=self.rotor_core,
            location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],
            theta=mo.DimRadian(0)),
            )

        self.shaft = mo.CrossSectHollowCylinder(
            name="Shaft",
            dim_t=mo.DimMillimeter(self.machine_variant.r_ri),
            dim_r_o=mo.DimMillimeter(self.machine_variant.r_ri),
            location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)]),
            )

        # self.rotor_bar = []
        # for i in range(0, 1):
        #     self.rotor_bar.append(mo.CrossSectInnerRotorRoundSlotsBar(
        #         name="Bar",
        #         rotor_core=self.rotor_core,
        #         location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],
        #         theta=mo.DimRadian(2 * np.pi / self.machine_variant.Qr * i)),
        #         ))


        self.comp_stator_core = mo.Component(
            name="StatorCore",
            cross_sections=[self.stator_core],
            material=mo.MaterialGeneric(name=self.machine_variant.stator_iron_mat["core_material"], color=r"#808080"),
            make_solid=mo.MakeExtrude(location=mo.Location3D(), 
                    dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )

        # self.comp_winding_layer1 = []
        # for i in range(0, 1):
        #     self.comp_winding_layer1.append(mo.Component(
        #         name="WindingLayer1",
        #         cross_sections=[self.winding_layer1[i]],
        #         material=mo.MaterialGeneric(name=self.machine_variant.coil_mat["coil_material"]),
        #         make_solid=mo.MakeExtrude(location=mo.Location3D(), 
        #         dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
        #     ))

        self.comp_winding_layer1 = mo.Component(
            name="WindingLayer1",
            cross_sections=[self.winding_layer1],
            material=mo.MaterialGeneric(name=self.machine_variant.coil_mat["coil_material"]),
            make_solid=mo.MakeExtrude(location=mo.Location3D(), 
            dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )


        # self.comp_winding_layer2 = []
        # for i in range(0, 1):
        #     self.comp_winding_layer2.append(mo.Component(
        #         name="WindingLayer2",
        #         cross_sections=[self.winding_layer2[i]],
        #         material=mo.MaterialGeneric(name=self.machine_variant.coil_mat["coil_material"]),
        #         make_solid=mo.MakeExtrude(location=mo.Location3D(), 
        #         dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
        #     ))


        self.comp_winding_layer2 = mo.Component(
            name="WindingLayer2",
            cross_sections=[self.winding_layer2],
            material=mo.MaterialGeneric(name=self.machine_variant.coil_mat["coil_material"]),
            make_solid=mo.MakeExtrude(location=mo.Location3D(), 
            dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )

        self.comp_rotor_core = mo.Component(
            name="RotorCore",
            cross_sections=[self.rotor_core],
            material=mo.MaterialGeneric(name=self.machine_variant.rotor_iron_mat["core_material"], color=r"#808080"),
            make_solid=mo.MakeExtrude(location=mo.Location3D(), 
                    dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )

        # self.comp_rotor_bar = []
        # for i in range(0, 1):
        #     self.comp_rotor_bar.append(mo.Component(
        #         name="Bar",
        #         cross_sections=[self.rotor_bar[i]],
        #         material=mo.MaterialGeneric(name=self.machine_variant.rotor_bar_mat["rotor_bar_material"]),
        #         make_solid=mo.MakeExtrude(location=mo.Location3D(),
        #         dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
        #     ))

        self.comp_rotor_bar = mo.Component(
            name="RotorBar",
            cross_sections=[self.rotor_bar],
            material=mo.MaterialGeneric(name=self.machine_variant.rotor_bar_mat["rotor_bar_material"], color=r"#C89E9B"),
            make_solid=mo.MakeExtrude(location=mo.Location3D(),
            dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )


        tool.bMirror = False

        tool.sketch = tool.create_sketch()
        tool.sketch.SetProperty("Name", self.stator_core.name)
        tool.sketch.SetProperty("Color", r"#808080")
        self.cs_stator = self.stator_core.draw(tool)
        self.stator_tool = tool.prepare_section(self.cs_stator, self.machine_variant.Q)
        # self.stator_tool = self.prepare_section([cs_stator.token], tool)

        tool.sketch = tool.create_sketch()
        tool.sketch.SetProperty("Name", self.winding_layer1.name)
        tool.sketch.SetProperty("Color", r"#B87333")
        self.cs_winding_layer1 = self.winding_layer1.draw(tool)
        self.winding_tool1 = tool.prepare_section(self.cs_winding_layer1, self.machine_variant.Q)

        tool.sketch = tool.create_sketch()
        tool.sketch.SetProperty("Name", self.winding_layer2.name)
        tool.sketch.SetProperty("Color", r"#B87333")
        self.cs_winding_layer2 = self.winding_layer2.draw(tool)
        self.winding_tool2 = tool.prepare_section(self.cs_winding_layer2, self.machine_variant.Q)

        tool.sketch = tool.create_sketch()
        tool.sketch.SetProperty("Name", self.rotor_core.name)
        tool.sketch.SetProperty("Color", r"#808080")
        self.cs_rotor_core = self.rotor_core.draw(tool)
        self.rotor_tool = tool.prepare_section(self.cs_rotor_core, self.machine_variant.Qr)

        tool.sketch = tool.create_sketch()
        tool.sketch.SetProperty("Name", self.rotor_bar.name)
        tool.sketch.SetProperty("Color", r"#C89E9B")
        self.cs_rotor_bar = self.rotor_bar.draw(tool)
        self.rotor_bar_tool = tool.prepare_section(self.cs_rotor_bar, self.machine_variant.Qr)

        tool.sketch = tool.create_sketch()
        tool.sketch.SetProperty("Name", self.shaft.name)
        tool.sketch.SetProperty("Color", r"#71797E")
        self.cs_shaft = self.shaft.draw(tool)
        self.shaft_tool = tool.prepare_section(self.cs_shaft)


        # tool.iRotateCopy = self.machine_variant.Q
        # self.stator_tool = self.comp_stator_core.make(tool, tool)

        # tool.iRotateCopy = self.machine_variant.Q
        # self.winding_tool1 = self.comp_winding_layer1.make(tool, tool)

        # tool.iRotateCopy = self.machine_variant.Q
        # self.winding_tool2 = self.comp_winding_layer2.make(tool, tool)
        
        # tool.iRotateCopy = self.machine_variant.Qr
        # self.rotor_tool = self.comp_rotor_core.make(tool, tool)

        # tool.iRotateCopy = self.machine_variant.Qr
        # self.rotor_bar_tool = self.comp_rotor_bar.make(tool, tool)


        # self.winding_tool1 = []
        # for i in range(0,self.machine_variant.Q):
        #     self.winding_tool1.append(self.comp_winding_layer1[i].make(tool, tool))
        # self.winding_tool2 = []
        # for i in range(0,self.machine_variant.Q):
        #     self.winding_tool2.append(self.comp_winding_layer2[i].make(tool, tool))

        # self.rotor_bar_tool = []
        # for i in range(0,self.machine_variant.Qr):
        #     self.rotor_bar_tool.append(self.comp_rotor_bar[i].make(tool, tool))

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
            print("- Bearingless PMSM Individual #%s\n\t" % name, end=" ")
            print(", \n\t".join("%s = %s" % item for item in tuple_list))
            return ""
        else:
            return "\n- Bearingless PMSM Individual #%s\n\t" % name + ", \n\t".join(
                "%s = %s" % item for item in tuple_list
            )

    def pre_process(self, model):
        # pre-process : you can select part by coordinate!
        """Group"""

        def group(name, id_list):
            model.GetGroupList().CreateGroup(name)
            for the_id in id_list:
                model.GetGroupList().AddPartToGroup(name, the_id)
                # model.GetGroupList().AddPartToGroup(name, name) #<- this also works

        part_ID_list = model.GetPartIDs()

        if len(part_ID_list) != int(
            1 + 1 + self.machine_variant.Q * 2 + self.machine_variant.Qr + 1
        ):
            print("Parts are missing in this machine")
            return False

        self.id_statorCore = id_statorCore = part_ID_list[0]
        partIDRange_Coil = part_ID_list[1 : int(2 * self.machine_variant.Q + 1)]
        self.id_rotorCore = id_rotorCore = part_ID_list[int(2 * self.machine_variant.Q + 1)]
        partIDRange_Bar = part_ID_list[int(2 * self.machine_variant.Q + 2) 
            : int(2 * self.machine_variant.Q + 2 + self.machine_variant.Qr)]
        id_shaft = part_ID_list[-1]

        # model.SuppressPart(id_sleeve, 1)

        group("Cage", partIDRange_Bar)
        group("Coils", partIDRange_Coil)

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

        # Shaft
        add_part_to_set("ShaftSet", 0.0, 0.0, ID=id_shaft)

        # Create Set for right layer
        Angle_StatorSlotSpan = 360 / self.machine_variant.Q
        # R = self.r_si + self.d_sp + self.d_st *0.5 # this is not generally working (JMAG selects stator core instead.)
        # THETA = 0.25*(Angle_StatorSlotSpan)/180.*np.pi
        R = np.sqrt(self.cs_winding_layer1.inner_coord[0] ** 2 + self.cs_winding_layer1.inner_coord[1] ** 2)
        THETA = np.arctan(self.cs_winding_layer1.inner_coord[1] / self.cs_winding_layer1.inner_coord[0])
        X = R * np.cos(THETA)
        Y = R * np.sin(THETA)
        count = 0
        for UVW, UpDown in zip(
            self.machine_variant.layer_phases[0], self.machine_variant.layer_polarity[0]
        ):
            count += 1
            add_part_to_set("coil_right_%s%s %d" % (UVW, UpDown, count), X, Y)

            # print(X, Y, THETA)
            THETA += Angle_StatorSlotSpan / 180.0 * np.pi
            X = R * np.cos(THETA)
            Y = R * np.sin(THETA)

        # Create Set for left layer
        THETA = np.arctan(self.cs_winding_layer2.inner_coord[1] / self.cs_winding_layer2.inner_coord[0])
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

        # Create Set for Bars
        R = self.machine_variant.R_bar_center
        Angle_RotorSlotSpan = 360 / self.machine_variant.Qr
        THETA = 0.001  # initial position
        X = R * np.cos(THETA)
        Y = R * np.sin(THETA)
        list_xy_bars = []
        count = 0
        for ind in range(int(self.machine_variant.Qr)):
            count += 1
            add_part_to_set("bar_%d" % count, X, Y)
            list_xy_bars.append([X, Y])

            THETA += Angle_RotorSlotSpan / 180.0 * np.pi
            X = R * np.cos(THETA)
            Y = R * np.sin(THETA)

        self.list_xy_bars = list_xy_bars

        # Create Set for Motion Region
        def part_list_set(name, list_xy, list_part_id=None, prefix=None):
            model.GetSetList().CreatePartSet(name)
            model.GetSetList().GetSet(name).SetMatcherType("Selection")
            model.GetSetList().GetSet(name).ClearParts()
            sel = model.GetSetList().GetSet(name).GetSelection()
            for xy in list_xy:
                sel.SelectPartByPosition(xy[0], xy[1], 0)  # z=0 for 2D
            if list_part_id is not None:
                for ID in list_part_id:
                    sel.SelectPart(ID)
            model.GetSetList().GetSet(name).AddSelected(sel)

        part_list_set(
            "Motion_Region", list_xy_bars, list_part_id=[id_rotorCore, partIDRange_Bar, id_shaft]
        )

        # Create Set for Cage
        part_list_set("CageSet", list_xy_bars)
        # model.GetSetList().CreatePartSet("CageSet")
        # model.GetSetList().GetSet("CageSet").SetMatcherType("MatchNames")
        # model.GetSetList().GetSet("CageSet").SetParameter("style", "prefix")
        # model.GetSetList().GetSet("CageSet").SetParameter("text", "Cage")
        # model.GetSetList().GetSet("CageSet").Rebuild()

        return True




    def create_custom_material(self, app, steel_name):

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
        # app.GetMaterialLibrary().GetUserMaterial(u"Arnon5-final").GetTable("BhTable").SetName(u"SmoothZeroPointOne")
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



    def add_transient_2tss_study(
        self, toolJmag
    ):      # app, model, dir_csv_output_folder, study_name
        # model.CreateStudy("Transient2D", study_name)
        # app.SetCurrentStudy(study_name)
        # study = model.GetStudy(study_name)

        dir_csv_output_folder = self.config.jmag_csv_folder
        study_name = self.study_name

        model = toolJmag.create_model(self.study_name)
        study = toolJmag.create_study(self.study_name, "Transient2D", model)
        app = toolJmag.jd
        app.SetCurrentStudy(self.study_name)

        # model.CreateStudy("Transient2D", self.study_name)
        # app.SetCurrentStudy(self.study_name)
        # study = model.GetStudy(self.study_name)

        # Study properties
        study.GetStudyProperties().SetValue("ApproximateTransientAnalysis", 1) # psuedo steady state freq is for PWM drive to use
        study.GetStudyProperties().SetValue("SpecifySlip", 1)
        study.GetStudyProperties().SetValue("Slip", self.slip)
        study.GetStudyProperties().SetValue("OutputSteadyResultAs1stStep", 0)
        study.GetStudyProperties().SetValue("ConversionType", 0)
        study.GetStudyProperties().SetValue(
            "NonlinearMaxIteration", self.config.max_nonlinear_iterations
        )
        study.GetStudyProperties().SetValue(
            "ModelThickness", self.machine_variant.l_st
        )  # [mm] Stack Length

        # Material
        self.add_materials(study)

        # Conditions - Motion
        study.CreateCondition("RotationMotion",
            "RotCon") # study.GetCondition(u"RotCon").SetXYZPoint(u"", 0, 0, 1) # megbox warning
        study.GetCondition("RotCon").SetValue("AngularVelocity",
            int(self.speed))
        study.GetCondition("RotCon").ClearParts()
        study.GetCondition("RotCon").AddSet(
            model.GetSetList().GetSet("Motion_Region"), 0
        )

        study.CreateCondition(
            "Torque", "TorCon"
        )  # study.GetCondition(u"TorCon").SetXYZPoint(u"", 0, 0, 0) # megbox warning
        study.GetCondition("TorCon").SetValue("TargetType", 1)
        study.GetCondition("TorCon").SetLinkWithType("LinkedMotion", "RotCon")
        study.GetCondition("TorCon").ClearParts()

        study.CreateCondition("Force", "ForCon")
        study.GetCondition("ForCon").SetValue("TargetType", 1)
        study.GetCondition("ForCon").SetLinkWithType("LinkedMotion", "RotCon")
        study.GetCondition("ForCon").ClearParts()

        # Conditions - FEM Coils & Conductors (i.e. stator/rotor winding)
        self.add_circuit(app, model, study, bool_3PhaseCurrentSource=False)
        self.set_currents_standard_excitation(self.It_hat, self.Is_hat, 
            self.drive_freq, self.phi_t_0, self.phi_s_0, app, study)

        # True: no mesh or field results are needed
        study.GetStudyProperties().SetValue(
            "OnlyTableResults", self.config.only_table_results
        )

        # this can be said to be super fast over ICCG solver.
        # https://www2.jmag-international.com/support/en/pdf/JMAG-Designer_Ver.17.1_ENv3.pdf
        study.GetStudyProperties().SetValue("DirectSolverType", 1)

        if self.config.multiple_cpus:
            # This SMP(shared memory process) is effective only if there are tons of elements. e.g., over 100,000.
            # too many threads will in turn make them compete with each other and slow down the solve. 2 is good enough
            # for eddy current solve. 6~8 is enough for transient solve.
            study.GetStudyProperties().SetValue("UseMultiCPU", True)
            study.GetStudyProperties().SetValue("MultiCPU", self.config.num_cpus)

        # two sections of different time step
        number_of_revolution_1TS = self.config.no_of_rev_1TS
        number_of_revolution_2TS = self.config.no_of_rev_2TS
        number_of_steps_1TS = (
            self.config.no_of_steps_per_rev_1TS * number_of_revolution_1TS
        )
        number_of_steps_2TS = (
            self.config.no_of_steps_per_rev_2TS * number_of_revolution_2TS
        )

        DM = app.GetDataManager()
        DM.CreatePointArray("point_array/timevsdivision", "SectionStepTable")
        refarray = [[0 for i in range(3)] for j in range(3)]
        refarray[0][0] = 0
        refarray[0][1] = 1
        refarray[0][2] = 50
        refarray[1][0] = number_of_revolution_1TS / (self.drive_freq * self.slip)
        refarray[1][1] = number_of_steps_1TS
        refarray[1][2] = 50
        refarray[2][0] = refarray[1][0] + number_of_revolution_2TS / self.drive_freq
        refarray[2][1] = number_of_steps_2TS  # number_of_steps_2TS
        refarray[2][2] = 50
        DM.GetDataSet("SectionStepTable").SetTable(refarray)
        number_of_total_steps = (
            1 + number_of_steps_1TS + number_of_steps_2TS
        )  # don't forget to modify here!
        study.GetStep().SetValue("Step", number_of_total_steps)
        study.GetStep().SetValue("StepType", 3)
        study.GetStep().SetTableProperty("Division", DM.GetDataSet("SectionStepTable"))

        # add equations
        study.GetDesignTable().AddEquation("freq")
        study.GetDesignTable().AddEquation("slip")
        study.GetDesignTable().AddEquation("speed")
        study.GetDesignTable().GetEquation("freq").SetType(0)
        study.GetDesignTable().GetEquation("freq").SetExpression(
            "%g" % self.drive_freq
        )
        study.GetDesignTable().GetEquation("freq").SetDescription(
            "Excitation Frequency"
        )
        study.GetDesignTable().GetEquation("slip").SetType(0)
        study.GetDesignTable().GetEquation("slip").SetExpression("%g"%(self.slip))
        study.GetDesignTable().GetEquation("slip").SetDescription("Slip [1]")
        study.GetDesignTable().GetEquation("speed").SetType(1)
        study.GetDesignTable().GetEquation("speed").SetExpression("freq * (1 - slip) * %d"%(60/(self.machine_variant.p)))
        study.GetDesignTable().GetEquation("speed").SetDescription(
            "mechanical speed of rotor"
        )

        # speed, freq, slip
        study.GetCondition("RotCon").SetValue("AngularVelocity", "speed")
        study.GetStudyProperties().SetValue("ApproximateTransientAnalysis", 1) # psuedo steady state freq is for PWM drive to use
        study.GetStudyProperties().SetValue("SpecifySlip", 1)
        study.GetStudyProperties().SetValue("OutputSteadyResultAs1stStep", 0)
        study.GetStudyProperties().SetValue("Slip", "slip") # overwrite with variables

        # Iron Loss Calculation Condition
        # Stator
        if True:
            cond = study.CreateCondition("Ironloss", "IronLossConStator")
            cond.SetValue("RevolutionSpeed", "freq*60/%d" % self.machine_variant.p)
            cond.ClearParts()
            sel = cond.GetSelection()
            # EPS = 1e-2  # unit: mm
            sel.SelectPart(self.id_statorCore)
            # sel.SelectPartByPosition(self.machine_variant.r_si / 1000 + EPS, EPS, 0)
            cond.AddSelected(sel)
            # Use FFT for hysteresis to be consistent with FEMM's results and to have a FFT plot
            cond.SetValue("HysteresisLossCalcType", 1)
            cond.SetValue("PresetType", 3)  # 3:Custom
            # Specify the reference steps yourself because you don't really know what JMAG is doing behind you
            cond.SetValue(
                "StartReferenceStep",
                number_of_total_steps + 1 - number_of_steps_2TS * 0.5,
            )  # 1/4 period = number_of_steps_2TS*0.5
            cond.SetValue("EndReferenceStep", number_of_total_steps)
            cond.SetValue("UseStartReferenceStep", 1)
            cond.SetValue("UseEndReferenceStep", 1)
            cond.SetValue(
                "Cyclicity", 4
            )  # specify reference steps for 1/4 period and extend it to whole period
            cond.SetValue("UseFrequencyOrder", 1)
            cond.SetValue("FrequencyOrder", "1-50")  # Harmonics up to 50th orders
        # Check CSV results for iron loss (You cannot check this for Freq study) # CSV and save space
        study.GetStudyProperties().SetValue(
            "CsvOutputPath", dir_csv_output_folder
        )  # it's folder rather than file!
        study.GetStudyProperties().SetValue("CsvResultTypes", self.config.csv_results)
        study.GetStudyProperties().SetValue(
            "DeleteResultFiles", self.config.del_results_after_calc
        )
        study.GetMaterial("Shaft").SetValue("OutputResult", 0)
        study.GetMaterial("Cage").SetValue("OutputResult", 0)
        study.GetMaterial("Coils").SetValue("OutputResult", 0)

        # Rotor
        if True:
            cond = study.CreateCondition("Ironloss", "IronLossConRotor")
            cond.SetValue("BasicFrequencyType", 2)
            cond.SetValue("BasicFrequency", "freq")
            # cond.SetValue(u"BasicFrequency", u"slip*freq") # this require the signal length to be at least 1/4 of
            # slip period, that's too long!
            cond.ClearParts()
            sel = cond.GetSelection()
            sel.SelectPart(self.id_rotorCore)

            cond.AddSelected(sel)
            # Use FFT for hysteresis to be consistent with FEMM's results
            cond.SetValue("HysteresisLossCalcType", 1)
            cond.SetValue("PresetType", 3)
            # Specify the reference steps yourself because you don't really know what JMAG is doing behind you
            cond.SetValue(
                "StartReferenceStep",
                number_of_total_steps + 1 - number_of_steps_2TS * 0.5,
            )  # 1/4 period = number_of_steps_2TS*0.5
            cond.SetValue("EndReferenceStep", number_of_total_steps)
            cond.SetValue("UseStartReferenceStep", 1)
            cond.SetValue("UseEndReferenceStep", 1)
            cond.SetValue(
                "Cyclicity", 4
            )  # specify reference steps for 1/4 period and extend it to whole period
            cond.SetValue("UseFrequencyOrder", 1)
            cond.SetValue("FrequencyOrder", "1-50")  # Harmonics up to 50th orders
        self.study_name = study_name

        toolJmag.jd = app
        toolJmag.model = model
        toolJmag.study = study
        return toolJmag


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

        study.SetMaterialByName(self.comp_rotor_core.name, 
            self.machine_variant.rotor_iron_mat["core_material"])
        study.GetMaterial(self.comp_rotor_core.name).SetValue("Laminated", 1)
        study.GetMaterial(self.comp_rotor_core.name).SetValue("LaminationFactor",
            self.machine_variant.rotor_iron_mat["core_stacking_factor"])

        study.SetMaterialByName(
            "Shaft", self.machine_variant.shaft_mat["shaft_material"]
        )
        study.GetMaterial("Shaft").SetValue("Laminated", 0)
        study.GetMaterial("Shaft").SetValue("EddyCurrentCalculation", 1)

        study.SetMaterialByName("Coils", "Copper")
        study.GetMaterial("Coils").SetValue("UserConductivityType", 1)

        # study.SetMaterialByName(self.comp_rotor_bar.name,
        #     self.machine_variant.rotor_bar_mat["rotor_bar_material"])
        # study.GetMaterial(self.comp_rotor_bar.name).SetValue("EddyCurrentCalculation", 1)
        # study.GetMaterial(self.comp_rotor_bar.name).SetValue("UserConductivityType", 1)
        # study.GetMaterial(self.comp_rotor_bar.name).SetValue("UserConductivityValue",
        #     self.machine_variant.rotor_bar_mat["bar_conductivity"])

        study.SetMaterialByName("Cage", self.machine_variant.rotor_bar_mat["rotor_bar_material"])
        study.GetMaterial("Cage").SetValue("EddyCurrentCalculation", 1)
        study.GetMaterial("Cage").SetValue("UserConductivityType", 1)
        study.GetMaterial("Cage").SetValue("UserConductivityValue",
            self.machine_variant.rotor_bar_mat["bar_conductivity"])

        # study.SetMaterialByName(self.comp_rotor_bar.name,
        #     self.machine_variant.coil_mat["coil_material"])
        # study.GetMaterial(self.comp_rotor_bar.name).SetValue("EddyCurrentCalculation", 1)
        # study.GetMaterial(self.comp_rotor_bar.name).SetValue("UserConductivityType", 1)
        # study.GetMaterial(self.comp_rotor_bar.name).SetValue("UserConductivityValue",
        #     self.machine_variant.coil_mat["copper_elec_conductivity"])


    def add_circuit(self, app, model, study, bool_3PhaseCurrentSource=True):
        def add_mp_circuit(study, turns, Rs, x=10, y=10):
            # Placing coils/phase windings
            coil_name = []
            for i in range(0, self.machine_variant.no_of_phases):
                coil_name.append("coil_" + self.machine_variant.name_phases[i])
                study.GetCircuit().CreateComponent("Coil", 
                    coil_name[i])
                study.GetCircuit().CreateInstance(coil_name[i],
                    x + 4 * i, y)
                study.GetCircuit().GetComponent(coil_name[i]).SetValue("Turn", turns)
                study.GetCircuit().GetComponent(coil_name[i]).SetValue("Resistance", Rs)
                study.GetCircuit().GetInstance(coil_name[i], 0).RotateTo(90)

            self.coil_name = coil_name

            # Connecting all phase windings to a neutral point
            for i in range(0, self.machine_variant.no_of_phases - 1):         
                study.GetCircuit().CreateWire(x + 4 * i, y - 2, x + 4 * (i + 1), y - 2)

            study.GetCircuit().CreateComponent("Ground", "Ground")
            study.GetCircuit().CreateInstance("Ground", x + 8, y - 4)
            
            # Placing current sources
            cs_name = []
            for i in range(0, self.machine_variant.no_of_phases):
                cs_name.append("cs_" + self.machine_variant.name_phases[i])
                study.GetCircuit().CreateComponent("CurrentSource", cs_name[i])
                study.GetCircuit().CreateInstance(cs_name[i], x + 4 * i, y + 4)
                study.GetCircuit().GetInstance(cs_name[i], 0).RotateTo(90)

            self.cs_name = cs_name

            # Terminal Voltage/Circuit Voltage: Check for outputting CSV results
            terminal_name = []
            for i in range(0, self.machine_variant.no_of_phases):
                terminal_name.append("vp_" + self.machine_variant.name_phases[i])
                study.GetCircuit().CreateTerminalLabel(terminal_name[i], x + 4 * i, y + 2)
                study.GetCircuit().CreateComponent("VoltageProbe", terminal_name[i])
                study.GetCircuit().CreateInstance(terminal_name[i], x + 2 + 4 * i, y + 2)
                study.GetCircuit().GetInstance(terminal_name[i], 0).RotateTo(90)

            self.terminal_name = terminal_name

        def add_rotor_circuit(study):
            # Condition - Conductor (i.e. rotor winding)
            for ind in range(int(self.machine_variant.Qr)):
                natural_ind = ind + 1

                study.CreateCondition("FEMConductor", "conductor_%d"%(natural_ind))
                condition = study.GetCondition("conductor_%d"%(natural_ind))


                condition.GetSubCondition("untitled").SetName("Conductor Set %d"%(natural_ind))
                subcondition = condition.GetSubCondition("Conductor Set %d"%(natural_ind))
                subcondition.ClearParts()




                # sel_group0 = subcondition.GetSelectionByGroup(0)
                # sel_group0.SelectFaceByPosition(self.list_xy_bars[ind][0], self.list_xy_bars[ind][1], 0)
                # subcondition.AddSelectedByGroup(sel_group0, 0)
                subcondition.AddSet(model.GetSetList().GetSet("bar_%d" % (natural_ind)), 0)

            # Condition - Conductor - Grouping
            study.CreateCondition("GroupFEMConductor", "conductor_group")
            for ind in range(int(self.machine_variant.Qr)):
                natural_ind = ind + 1
                study.GetCondition("conductor_group").AddSubCondition("conductor_%d"%(natural_ind), ind)

            # Link Conductors to Circuit
            def place_conductor(x, y, name):
                study.GetCircuit().CreateComponent("FEMConductor", name)
                study.GetCircuit().CreateInstance(name, x, y)
            def place_resistor(x, y, name, R_end_ring, rotation):
                study.GetCircuit().CreateComponent("Resistor", name)
                study.GetCircuit().CreateInstance(name, x, y)
                study.GetCircuit().GetComponent(name).SetValue("Resistance", R_end_ring)
                study.GetCircuit().GetInstance(name, 0).RotateTo(rotation)

        
            X = - 20
            Y = 100
            count = 0
            vertical_length = 6
            conductors_per_phase = len(self.machine_variant.layer_phases_rotor[0])/ self.machine_variant.no_of_phases_rotor
            conductor_names = []
            for index_phase, phase in enumerate(self.machine_variant.name_phases_rotor):
                count2 = 1
                for index_layer_phase, layer_phase in enumerate(self.machine_variant.layer_phases_rotor[0]):
                    if phase == layer_phase:
                        string_conductor = "conductor_" + layer_phase + "_" + str(index_layer_phase + 1)
                        conductor_names.append(string_conductor)
                        place_conductor(X, Y - vertical_length * count, string_conductor)
                        study.GetCondition("conductor_%d"%(index_layer_phase + 1)).SetLink(string_conductor)
                        if count2 < conductors_per_phase:
                            if self.R_end_ring == 0:
                                study.GetCircuit().CreateWire(X - 2, Y - vertical_length * count, X - 2, Y - vertical_length * count - vertical_length)
                                study.GetCircuit().CreateWire(X + 2, Y - vertical_length * count, X + 2, Y - vertical_length * count - vertical_length)
                            else:
                                study.GetCircuit().CreateWire(X - 2, Y - vertical_length * count, X - 2, Y - vertical_length * count - 1)
                                study.GetCircuit().CreateWire(X + 2, Y - vertical_length * count, X + 2, Y - vertical_length * count - 1)
                                place_resistor(X - 2, Y - vertical_length * count - 3, "R_" + phase + "_1", self.R_end_ring, rotation=90)
                                place_resistor(X + 2, Y - vertical_length * count - 3, "R_" + phase + "_2", self.R_end_ring, rotation=90)
                                study.GetCircuit().CreateWire(X - 2, Y - vertical_length * count - 5, X - 2, Y - vertical_length * count - 6)
                                study.GetCircuit().CreateWire(X + 2, Y - vertical_length * count - 5, X + 2, Y - vertical_length * count - 6)
                        
                        if (count2 == conductors_per_phase) and (index_phase + 1 < self.machine_variant.no_of_phases_rotor):
                            study.GetCircuit().CreateWire(X - 2, Y - vertical_length * count, X - 2, Y - vertical_length * count - vertical_length)

                        count += 1
                        count2 += 1

            self.conductor_names = conductor_names
            study.GetCircuit().CreateInstance("Ground", X - 4, Y - 2)
            study.GetCircuit().CreateWire(X - 4, Y, X - 2, Y)


        app.ShowCircuitGrid(True)
        study.CreateCircuit()

        add_mp_circuit(study, self.machine_variant.Z_q, Rs=self.R_coil)
        # set_currents(ampT=self.It_hat, ampS=self.Is_hat, freq=self.drive_freq)

        for phase_name in self.machine_variant.name_phases:
            study.CreateCondition("FEMCoil", phase_name)
            # link between FEM Coil Condition and Circuit FEM Coil
            condition = study.GetCondition(phase_name)
            condition.SetLink("coil_%s" % (phase_name))
            condition.GetSubCondition("untitled").SetName("delete")

        count = 0  # count indicates which slot the current rightlayer is in.
        index = 0
        dict_dir = {"+": 1, "-": 0}
        coil_pitch = self.machine_variant.pitch  # self.dict_coil_connection[0]
        # select the part (via `Set') to assign the FEM Coil condition
        for UVW, UpDown in zip(
            self.machine_variant.layer_phases[0], self.machine_variant.layer_polarity[0]
        ):

            count += 1
            condition = study.GetCondition(UVW)

            # right layer
            # print (count, "Coil Set %d"%(count), end=' ')
            condition.CreateSubCondition("FEMCoilData", "Coil Set Right %d" % count)
            subcondition = condition.GetSubCondition("Coil Set Right %d" % count)
            subcondition.ClearParts()
            subcondition.AddSet(
                model.GetSetList().GetSet(
                    "coil_%s%s%s %d" % ("right_", UVW, UpDown, count)
                ),
                0,
            )  # right layer
            subcondition.SetValue("Direction2D", dict_dir[UpDown])

            # left layer
            if coil_pitch > 0:
                if count + coil_pitch <= self.machine_variant.Q:
                    count_leftlayer = count + coil_pitch
                    index_leftlayer = index + coil_pitch
                else:
                    count_leftlayer = int(count + coil_pitch - self.machine_variant.Q)
                    index_leftlayer = int(index + coil_pitch - self.machine_variant.Q)
            else:
                if count + coil_pitch > 0:
                    count_leftlayer = count + coil_pitch
                    index_leftlayer = index + coil_pitch
                else:
                    count_leftlayer = int(count + coil_pitch + self.machine_variant.Q)
                    index_leftlayer = int(index + coil_pitch + self.machine_variant.Q)

            # Check if it is a distributed windg???
            if self.machine_variant.pitch == 1:
                UVW = self.machine_variant.layer_phases[1][index_leftlayer]
                UpDown = self.machine_variant.layer_polarity[1][index_leftlayer]
            else:
                if self.machine_variant.layer_phases[1][index_leftlayer] != UVW:
                    print("[Warn] Potential bug in your winding layout detected.")
                    raise Exception("Bug in winding layout detected.")
                if UpDown == "+":
                    UpDown = "-"
                else:
                    UpDown = "+"
            # print (count_leftlayer, "Coil Set %d"%(count_leftlayer))
            condition.CreateSubCondition(
                "FEMCoilData", "Coil Set Left %d" % count_leftlayer
            )
            subcondition = condition.GetSubCondition(
                "Coil Set Left %d" % count_leftlayer
            )
            subcondition.ClearParts()
            subcondition.AddSet(
                model.GetSetList().GetSet(
                    "coil_%s%s%s %d" % ("left_", UVW, UpDown, count_leftlayer)
                ),
                0,
            )  # left layer
            subcondition.SetValue("Direction2D", dict_dir[UpDown])
            index += 1
            # clean up
            for phase_name in self.machine_variant.name_phases:
                condition = study.GetCondition(phase_name)
                condition.RemoveSubCondition("delete")

        add_rotor_circuit(study)


    def set_currents_standard_excitation(self, ampT, ampS, freq, phi_t_0, phi_s_0, app, study):
        # Setting current values after creating a circuit using "add_mp_circuit" method
        # "freq" variable cannot be used here. So pay extra attention when you 
        # create new case of a different freq.
        for i in range(0, self.machine_variant.no_of_phases):
            func = app.FunctionFactory().Composite()
            f1 = app.FunctionFactory().Sin(ampT, freq,
                - self.machine_variant.p * 360 / self.machine_variant.no_of_phases * i - phi_t_0 + 90)
            f2 = app.FunctionFactory().Sin(ampS, freq,
                - self.machine_variant.ps * 360 / self.machine_variant.no_of_phases * i - phi_s_0 + 90)
            func.AddFunction(f1)
            func.AddFunction(f2)
            study.GetCircuit().GetComponent(self.cs_name[i]).SetFunction(func)


    def mesh_study(self, app, model, study):

        # this `if' judgment is effective only if JMAG-DeleteResultFiles is False
        # if not study.AnyCaseHasResult():
        # mesh
        print("------------------Adding mesh")
        self.add_mesh(study, model)

        # Export Image
        app.View().ShowAllAirRegions()
        # app.View().ShowMeshGeometry() # 2nd btn
        app.View().ShowMesh()  # 3rn btn
        app.View().Zoom(3)
        app.View().Pan(-self.machine_variant.r_si / 1000, 0)
        app.ExportImageWithSize(
            self.design_results_folder + self.project_name + "mesh.png", 2000, 2000
        )
        app.View().ShowModel()  # 1st btn. close mesh view, and note that mesh data will be deleted if only ouput table
        # results are selected.


    def add_mesh(self, study, model):
        # this is for multi slide planes, which we will not be usin
        refarray = [[0 for i in range(2)] for j in range(1)]
        refarray[0][0] = 3
        refarray[0][1] = 1
        study.GetMeshControl().GetTable("SlideTable2D").SetTable(refarray)

        study.GetMeshControl().SetValue("MeshType", 1)  # make sure this has been exe'd:
        # study.GetCondition(u"RotCon").AddSet(model.GetSetList().GetSet(u"Motion_Region"), 0)
        study.GetMeshControl().SetValue(
            "RadialDivision", self.config.airgap_mesh_radial_div
        )  # for air region near which motion occurs
        study.GetMeshControl().SetValue(
            "CircumferentialDivision", self.config.airgap_mesh_circum_div
        )  # 1440) # for air region near which motion occurs
        study.GetMeshControl().SetValue(
            "AirRegionScale", self.config.mesh_air_region_scale
        )  # [Model Length]: Specify a value within (1.05 <= value < 1000)
        study.GetMeshControl().SetValue("MeshSize", self.config.mesh_size)
        study.GetMeshControl().SetValue("AutoAirMeshSize", 0)
        study.GetMeshControl().SetValue(
            "AirMeshSize", self.config.mesh_size
        )  # mm
        study.GetMeshControl().SetValue("Adaptive", 0)

        study.GetMeshControl().CreateCondition("RotationPeriodicMeshAutomatic", 
                "autoRotMesh") # with this you can choose to set CircumferentialDivision automatically

        study.GetMeshControl().CreateCondition("Part", "CageMeshCtrl")
        study.GetMeshControl().GetCondition("CageMeshCtrl").SetValue("Size", self.config.mesh_size_rotor)
        study.GetMeshControl().GetCondition("CageMeshCtrl").ClearParts()
        study.GetMeshControl().GetCondition("CageMeshCtrl").AddSet(model.GetSetList().GetSet("CageSet"), 0)

        study.GetMeshControl().CreateCondition("Part", "ShaftMeshCtrl")
        study.GetMeshControl().GetCondition("ShaftMeshCtrl").SetValue("Size", 10) # 10 mm
        study.GetMeshControl().GetCondition("ShaftMeshCtrl").ClearParts()
        study.GetMeshControl().GetCondition("ShaftMeshCtrl").AddSet(model.GetSetList().GetSet("ShaftSet"), 0)

        def mesh_all_cases(study):
            numCase = study.GetDesignTable().NumCases()
            for case in range(0, numCase):
                study.SetCurrentCase(case)
                if not study.HasMesh():
                    study.CreateMesh()

        # if self.MODEL_ROTATE:
        #     if self.total_number_of_cases>1: # just to make sure
        #         model.RestoreCadLink()
        #         study.ApplyAllCasesCadParameters()

        mesh_all_cases(study)


    def run_study(self, app, study, toc):
        if not self.config.jmag_scheduler:
            print("-----------------------Running JMAG...")
            # if run_list[1] == True:
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
            # study.CheckForCaseResults()
        
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
            # self.sketch.CreateRegionsWithCleanup(EPS, True) # StatorCore will fail

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
                # print('Copy', self.iRotateCopy)
                regionCircularPattern360Origin(
                    region_object, tool, bMerge=bRotateMerge
                )

        tool.sketch.CloseSketch()
        return list_region_objects


    def extract_JMAG_results(self, path, study_name):
        current_csv_path = path + study_name + "_circuit_current.csv"
        voltage_csv_path = path + study_name + "_circuit_voltage.csv"
        torque_csv_path = path + study_name + "_torque.csv"
        force_csv_path = path + study_name + "_force.csv"
        iron_loss_path = path + study_name + "_iron_loss_loss.csv"
        hysteresis_loss_path = path + study_name + "_hysteresis_loss_loss.csv"
        eddy_current_loss_path = path + study_name + "_joule_loss_loss.csv"
        ohmic_loss_path = path + study_name + "_joule_loss.csv"

        curr_df = pd.read_csv(current_csv_path, skiprows=7)
        volt_df = pd.read_csv(voltage_csv_path, skiprows=7)
        tor_df = pd.read_csv(torque_csv_path, skiprows=7)
        force_df = pd.read_csv(force_csv_path, skiprows=7)
        iron_df = pd.read_csv(iron_loss_path, skiprows=7)
        hyst_df = pd.read_csv(hysteresis_loss_path, skiprows=7)
        eddy_df = pd.read_csv(eddy_current_loss_path, skiprows=7)
        ohmic_df = pd.read_csv(ohmic_loss_path, skiprows=7)

        range_2TS = int(self.config.no_of_steps_per_rev_2TS * self.config.no_of_rev_2TS)

        curr_df = curr_df.set_index("Time(s)")
        volt_df = volt_df.set_index("Time(s)")
        tor_df = tor_df.set_index("Time(s)")
        force_df = force_df.set_index("Time(s)")
        eddy_df = eddy_df.set_index("Frequency(Hz)")
        hyst_df = hyst_df.set_index("Frequency(Hz)")
        iron_df = iron_df.set_index("Frequency(Hz)")
        ohmic_df = ohmic_df.set_index("Time(s)")

        fea_data = {
            "current": curr_df,
            "voltage": volt_df,
            "torque": tor_df,
            "force": force_df,
            "iron_loss": iron_df,
            "hysteresis_loss": hyst_df,
            "eddy_current_loss": eddy_df,
            "ohmic_loss": ohmic_df,
            "stator_calc_ohmic_loss": [self.stator_calc_ohmic_loss, 
                        self.stator_calc_ohmic_loss_along_stack,
                        self.stator_calc_ohmic_loss_end_wdg],
            "range_fine_step": range_2TS,
            "conductor_names": self.conductor_names,
            "non_zero_end_ring_res": self.config.non_zero_end_ring_res
        }

        return fea_data
