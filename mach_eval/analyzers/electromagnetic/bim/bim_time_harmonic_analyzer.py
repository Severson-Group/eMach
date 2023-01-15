import os
import numpy as np
import sys
import femm
from time import sleep
from time import time as clock_time
import logging

sys.path.append(os.path.dirname(__file__) + "/../../../..")
import mach_cad.model_obj as mo
from mach_cad.tools.femm import FEMM


class BIM_Time_Harmonic_Problem:
    def __init__(self, machine, operating_point):
        self.machine = machine
        self.operating_point = operating_point
        self._validate_attr()

    def _validate_attr(self):
        if 'BIM_Machine' or 'BIM_Double_Cage_Machine' in str(type(self.machine)):
            pass
        else:
            raise TypeError("Invalid machine type")

        if 'BIM_Machine_Oper_Pt' in str(type(self.operating_point)):
            pass
        else:
            raise TypeError("Invalid settings type")


class BIM_Time_Harmonic_Analyzer:
    def __init__(self, configuration):
        self.config = configuration

    def analyze(self, problem):
        self.machine_variant = problem.machine
        self.operating_point = problem.operating_point
        id_rotor_iron = self.config.id_rotor_iron
        id_rotor_bars = self.config.id_rotor_bars
        id_stator_slots = self.config.id_stator_slots
        id_stator_iron = self.config.id_stator_iron

        ####################################################
        # 01 Setting project name and output folder
        ####################################################
        self.project_name = self.machine_variant.name
        self.expected_project_file = self.config.run_folder + "%s.fem" % self.project_name

        attempts = 1
        if os.path.exists(self.expected_project_file):
            print(
                "FEMM project exists already, I will not delete it but create a new one with a different name instead."
            )
            # os.remove(expected_project_file_path)
            attempts = 2
            temp_path = self.expected_project_file[
                : -len(".fem")
            ] + "_attempts_%d.fem" % (attempts)
            while os.path.exists(temp_path):
                attempts += 1
                temp_path = self.expected_project_file[
                    : -len(".fem")
                ] + "_attempts_%d.fem" % (attempts)

            self.expected_project_file = temp_path

        if attempts > 1:
            self.project_name = self.project_name + "_attempts_%d" % (attempts)


        if not os.path.isdir(self.config.run_folder):
            os.makedirs(self.config.run_folder)

        for suffix in ['.ans', '.csv', '.fem']:
            fname = self.config.run_folder + 'femm_found' + suffix
            if os.path.exists(fname):
                os.remove(fname)


        toolFEMM = FEMM.FEMMDesigner()
        toolFEMM.newdocument(hide_window=1, problem_type=0)
        toolFEMM.probdef(freq=1, depth=self.machine_variant.l_st, acsolver=1)
        ################################################################
        # 02 Run Electromagnetic analysis
        ################################################################
        # Add materials from the library
        toolFEMM.add_material("Air")
        toolFEMM.add_material(mat_name=self.machine_variant._materials_dict["coil_mat"]["coil_material"])

        # Add new materials
        toolFEMM.add_new_material(mat_name=self.machine_variant.rotor_bar_mat["rotor_bar_material"],
                                    Cduct=self.machine_variant.rotor_bar_mat["bar_conductivity"] * 1e-6)
        hdata, bdata = np.loadtxt(self.machine_variant.stator_iron_mat['core_bh_file'], 
                                    unpack=True, usecols=(0, 1))
        toolFEMM.add_new_material(mat_name=self.machine_variant.stator_iron_mat["core_material"],
                                    hdata=hdata,bdata=bdata)

        # Draw the model
        if self.config.double_cage == True:
            draw_success = self.draw_machine_double_cage(toolFEMM)
        else:
            draw_success = self.draw_machine(toolFEMM)
        
        # Set air regions
        toolFEMM.set_block_prop(
            new_block=1,
            inner_coord=[0, 0],
            material_name='<No Mesh>',
            meshsize_if_no_automesh=self.config.mesh_size_other_regions
            )
        toolFEMM.set_block_prop(
            new_block=1,
            inner_coord=[self.machine_variant.R_airgap, 0],
            material_name='Air',
            automesh=self.config.automesh,
            meshsize_if_no_automesh=self.config.mesh_size_airgap
            )
        # toolFEMM.set_block_prop(
        #     new_block=1,
        #     inner_coord=[self.machine_variant.r_so * 1.1, 0],
        #     material_name='Air',
        #     automesh=self.config.automesh,
        #     meshsize_if_no_automesh=self.config.mesh_size_other_regions
        #     )

        # Create boundary condition
        # toolFEMM.create_boundary_condition(number_of_shells=7, 
        #     radius=self.machine_variant.r_so * 1.2, centerxy=(0,0), bc=1)

        # Redraw the outer part of the stator (needed for creating boundary conditions)
        for i in range(0, self.machine_variant.Q):
            alpha_u = 2 * np.pi / self.machine_variant.Q
            alpha_i = alpha_u * i
            x_arc = self.machine_variant.r_so * np.cos(alpha_i)
            y_arc = self.machine_variant.r_so * np.sin(alpha_i)
            femm.mi_selectarcsegment(x_arc, y_arc)
            x_node = self.machine_variant.r_so * np.cos(alpha_i + alpha_u / 2)
            y_node = self.machine_variant.r_so * np.sin(alpha_i + alpha_u / 2)
            femm.mi_selectnode(x_node, y_node)
        femm.mi_deleteselected()
        toolFEMM.draw_arc([0, 0], [+self.machine_variant.r_so, 0], [-self.machine_variant.r_so, 0])
        toolFEMM.draw_arc([0, 0], [-self.machine_variant.r_so, 0], [+self.machine_variant.r_so, 0])
        
        femm.mi_addboundprop('BC:A=0', 0,0,0, 0,0,0,0,0,0,0,0)
        
        femm.mi_selectarcsegment(0, -self.machine_variant.r_so)
        femm.mi_setarcsegmentprop(20, "BC:A=0", False, 10) # maxseg = 20 deg (only this is found effective)
        femm.mi_clearselected()

        femm.mi_selectarcsegment(0, self.machine_variant.r_so)
        femm.mi_setarcsegmentprop(20, "BC:A=0", False, 10)
        femm.mi_clearselected()

        femm.mi_selectarcsegment(0, -self.machine_variant.r_sh)
        femm.mi_setarcsegmentprop(20, "BC:A=0", False, 100)
        femm.mi_clearselected()
        femm.mi_selectarcsegment(0, self.machine_variant.r_sh)
        femm.mi_setarcsegmentprop(20, "BC:A=0", False, 100)
        femm.mi_clearselected()

        # Reduce the number of arc segments of bars to reduce the number of mesh elements
        if self.config.double_cage == False:
            x_arc_0 = self.machine_variant.R_bar_center
            y_arc_0 = self.machine_variant.r_rb
            alpha_u = 2 * np.pi / self.machine_variant.Qr
            for i in range(0, self.machine_variant.Qr):
                alpha_i = alpha_u * i
                x_arc_1 = x_arc_0 * np.cos(alpha_i) - y_arc_0 * np.sin(alpha_i)
                y_arc_1 = x_arc_0 * np.sin(alpha_i) + y_arc_0 * np.cos(alpha_i)

                x_arc_2 = x_arc_0 * np.cos(alpha_i) - -y_arc_0 * np.sin(alpha_i)
                y_arc_2 = x_arc_0 * np.sin(alpha_i) + -y_arc_0 * np.cos(alpha_i)

                femm.mi_selectarcsegment(x_arc_1, y_arc_1)
                femm.mi_setarcsegmentprop(8, "<None>", False, 0)
                femm.mi_clearselected()
                femm.mi_selectarcsegment(x_arc_2, y_arc_2)
                femm.mi_setarcsegmentprop(8, "<None>", False, 0)
                femm.mi_clearselected()
        else:
            x_arc_0 = self.machine_variant.R_bar1_center
            y_arc_0 = self.machine_variant.r_rb
            alpha_u = 2 * np.pi / self.machine_variant.Qr
            for i in range(0, self.machine_variant.Qr):
                alpha_i = alpha_u * i
                x_arc_1 = x_arc_0 * np.cos(alpha_i) - y_arc_0 * np.sin(alpha_i)
                y_arc_1 = x_arc_0 * np.sin(alpha_i) + y_arc_0 * np.cos(alpha_i)

                x_arc_2 = x_arc_0 * np.cos(alpha_i) - -y_arc_0 * np.sin(alpha_i)
                y_arc_2 = x_arc_0 * np.sin(alpha_i) + -y_arc_0 * np.cos(alpha_i)

                femm.mi_selectarcsegment(x_arc_1, y_arc_1)
                femm.mi_setarcsegmentprop(8, "<None>", False, 0)
                femm.mi_clearselected()
                femm.mi_selectarcsegment(x_arc_2, y_arc_2)
                femm.mi_setarcsegmentprop(8, "<None>", False, 0)
                femm.mi_clearselected()

            x_arc_0 = self.machine_variant.R_bar2_center
            for i in range(0, self.machine_variant.Qr):
                alpha_i = alpha_u * i
                x_arc_1 = x_arc_0 * np.cos(alpha_i) - y_arc_0 * np.sin(alpha_i)
                y_arc_1 = x_arc_0 * np.sin(alpha_i) + y_arc_0 * np.cos(alpha_i)

                x_arc_2 = x_arc_0 * np.cos(alpha_i) - -y_arc_0 * np.sin(alpha_i)
                y_arc_2 = x_arc_0 * np.sin(alpha_i) + -y_arc_0 * np.cos(alpha_i)

                femm.mi_selectarcsegment(x_arc_1, y_arc_1)
                femm.mi_setarcsegmentprop(8, "<None>", False, 0)
                femm.mi_clearselected()
                femm.mi_selectarcsegment(x_arc_2, y_arc_2)
                femm.mi_setarcsegmentprop(8, "<None>", False, 0)
                femm.mi_clearselected()


        # Create stator circuits, add mesh sizes
        m = self.machine_variant.no_of_phases
        for i in range(0, m):
            toolFEMM.add_circuit(circuitname=self.machine_variant.name_phases[i])
        for i in range(0, self.machine_variant.Q):
            toolFEMM.set_block_prop(
                inner_coord=self.winding_tool1[i].cs_token[0].inner_coord,
                material_name=self.comp_winding_layer1[i].material.name,
                incircuit=self.machine_variant.layer_phases[0][i],
                turns=-float(self.machine_variant.layer_polarity[0][i]+
                str(self.machine_variant.Z_q)),
                group_no=id_stator_slots,
                automesh=self.config.automesh,
                meshsize_if_no_automesh=self.config.mesh_size_copper
                )
        for i in range(0, self.machine_variant.Q):
            toolFEMM.set_block_prop(
                inner_coord=self.winding_tool2[i].cs_token[0].inner_coord,
                material_name=self.comp_winding_layer2[i].material.name,
                incircuit=self.machine_variant.layer_phases[1][i],
                turns=-float(self.machine_variant.layer_polarity[1][i]+
                str(self.machine_variant.Z_q)),
                group_no=id_stator_slots,
                automesh=self.config.automesh,
                meshsize_if_no_automesh=self.config.mesh_size_copper
                )

        toolFEMM.set_block_prop(
            inner_coord=self.stator_tool.cs_token[0].inner_coord,
            material_name=self.comp_stator_core.material.name,
            group_no = id_stator_iron,
            automesh=self.config.automesh,
            meshsize_if_no_automesh=self.config.mesh_size_steel
            )

        # Add block id-s to rotor iron and rotor bars
        toolFEMM.set_block_prop(
            inner_coord=self.rotor_tool.cs_token[0].inner_coord,
            material_name=self.comp_rotor_core.material.name,
            group_no = id_rotor_iron,
            automesh=self.config.automesh,
            meshsize_if_no_automesh=self.config.mesh_size_steel
            )

        
        if self.config.double_cage == False:
            for i in range(0, self.machine_variant.no_of_phases_rotor):
                toolFEMM.add_circuit(circuitname=self.machine_variant.name_phases_rotor[i], series_or_parallel=0)
            for i in range(0, self.machine_variant.Qr):
                toolFEMM.set_block_prop(
                    inner_coord=self.rotor_bar_tool[i].cs_token[0].inner_coord,
                    material_name=self.comp_rotor_bar[i].material.name,
                    incircuit=self.machine_variant.layer_phases_rotor[0][i],
                    turns=-float(self.machine_variant.layer_polarity_rotor[0][i]+
                    str(self.machine_variant.Z_q_rotor)),
                    group_no=id_rotor_bars,
                    automesh=self.config.automesh,
                    meshsize_if_no_automesh=self.config.mesh_size_aluminum
                    )
        else:
            for i in range(0, self.machine_variant.no_of_phases_rotor):
                toolFEMM.add_circuit(circuitname=self.machine_variant.name_phases_rotor[i], series_or_parallel=0)
            for i in range(0, self.machine_variant.Qr):
                toolFEMM.set_block_prop(
                    inner_coord=self.rotor_bar_tool1[i].cs_token[0].inner_coord,
                    material_name=self.comp_rotor_bar1[i].material.name,
                    incircuit=self.machine_variant.layer_phases_rotor[0][i],
                    turns=-float(self.machine_variant.layer_polarity_rotor[0][i]+
                    str(self.machine_variant.Z_q_rotor)),
                    group_no=id_rotor_bars,
                    automesh=self.config.automesh,
                    meshsize_if_no_automesh=self.config.mesh_size_aluminum
                    )
                toolFEMM.set_block_prop(
                    inner_coord=self.rotor_bar_tool2[i].cs_token[0].inner_coord,
                    material_name=self.comp_rotor_bar2[i].material.name,
                    incircuit=self.machine_variant.layer_phases_rotor[1][i],
                    turns=-float(self.machine_variant.layer_polarity_rotor[1][i]+
                    str(self.machine_variant.Z_q_rotor)),
                    group_no=id_rotor_bars,
                    automesh=self.config.automesh,
                    meshsize_if_no_automesh=self.config.mesh_size_aluminum
                    )

        # Start the analysis
        It_hat = self.operating_point.It_ratio * self.machine_variant.rated_current * np.sqrt(2)
        p = self.machine_variant.p
        for i in range(0, m):
            toolFEMM.set_current(circuitname=self.machine_variant.name_phases[i],
                        current=It_hat*(np.cos(i * p * 2 * np.pi / m) - 1j * np.sin(i * p * 2 * np.pi / m)))
        toolFEMM.smartmesh(state=0)

        print('Run greedy_search_for_breakdown_slip...')
        toolFEMM.save_as(self.expected_project_file)
        toolFEMM.close()

        self.dir_femm_temp = self.config.run_folder

        femm_tic = clock_time()
        print('\n' + '-' * 20, self.project_name)

        # self.find_breakdown_slip_torque(toolFEMM)

        print(os.path.dirname(os.path.abspath(__file__)) + '/bim_time_harmonic_analyzer_extra_files/parasolve_greedy_search_manager.py')
        import subprocess
        proc = subprocess.Popen(
            [sys.executable, os.path.dirname(os.path.abspath(__file__)) + '/bim_time_harmonic_analyzer_extra_files/parasolve_greedy_search_manager.py',
            self.dir_femm_temp, self.expected_project_file, str(self.machine_variant.l_st),
            str(self.config.freq_start), str(self.config.freq_end), str(self.config.no_of_freqs),
            str(self.config.max_freq_error), str(self.config.id_rotor_iron), str(self.config.id_rotor_bars) ], bufsize=-1
            )

        if self.config.get_results_in_t2tss_analyzer == True: # if we want to run BIM_Transient_2TSS_Analyzer in parallel
            slip_freq_breakdown_torque = None
            breakdown_torque = None
        else: # if we want to run the subsequent analyzer of the evaluator in sequence or if there are no subsequent analyzers to run
            slip_freq_breakdown_torque, breakdown_torque = self.wait_greedy_search(femm_tic, id_rotor_bars, id_stator_slots)

        # Output
        bim_tha_results = {
            "slip_freq_breakdown_torque": slip_freq_breakdown_torque,
            "breakdown_torque": breakdown_torque,
            "configuration": self.config,
        }

        return bim_tha_results

    def draw_machine(self, tool):
        ####################################################
        # Adding parts objects
        ####################################################
        self.stator_core = mo.CrossSectInnerRotorStator(
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

        self.winding_layer1 = []
        for i in range (0, self.machine_variant.Q):
            self.winding_layer1.append(mo.CrossSectInnerRotorStatorRightSlot(
                name="WindingLayer1",
                stator_core=self.stator_core,
                location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],
                theta=mo.DimRadian(2 * np.pi / self.machine_variant.Q * i)),
                ))

        self.winding_layer2 = []
        for i in range (0, self.machine_variant.Q):
            self.winding_layer2.append(mo.CrossSectInnerRotorStatorLeftSlot(
                name="WindingLayer2",
                stator_core=self.stator_core,
                location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],
                theta=mo.DimRadian(2 * np.pi / self.machine_variant.Q * i)),
                ))

        self.rotor_core = mo.CrossSectInnerRotorRoundSlots(
            name="RotorCore",
            dim_r_ri=mo.DimMillimeter(self.machine_variant.r_ri),
            dim_d_ri=mo.DimMillimeter(self.machine_variant.d_ri),
            dim_r_rb=mo.DimMillimeter(self.machine_variant.r_rb),
            dim_d_so=mo.DimMillimeter(self.machine_variant.d_rso),
            dim_w_so=mo.DimMillimeter(self.machine_variant.w_so),
            Qr=self.machine_variant.Qr,
            location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)]),
            )

        self.rotor_bar = []
        for i in range(0,self.machine_variant.Qr):
            self.rotor_bar.append(mo.CrossSectInnerRotorRoundSlotsBar(
                name="Bar",
                rotor_core=self.rotor_core,
                location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],
                theta=mo.DimRadian(2 * np.pi / self.machine_variant.Qr * i)),
                ))


        self.comp_stator_core = mo.Component(
            name="StatorCore",
            cross_sections=[self.stator_core],
            material=mo.MaterialGeneric(name=self.machine_variant.stator_iron_mat["core_material"]),
            make_solid=mo.MakeExtrude(location=mo.Location3D(), 
                    dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )

        self.comp_winding_layer1 = []
        for i in range(0,self.machine_variant.Q):
            self.comp_winding_layer1.append(mo.Component(
                name="WindingLayer1",
                cross_sections=[self.winding_layer1[i]],
                material=mo.MaterialGeneric(name=self.machine_variant.coil_mat["coil_material"]),
                make_solid=mo.MakeExtrude(location=mo.Location3D(), 
                dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            ))

        self.comp_winding_layer2 = []
        for i in range(0,self.machine_variant.Q):
            self.comp_winding_layer2.append(mo.Component(
                name="WindingLayer2",
                cross_sections=[self.winding_layer2[i]],
                material=mo.MaterialGeneric(name=self.machine_variant.coil_mat["coil_material"]),
                make_solid=mo.MakeExtrude(location=mo.Location3D(), 
                dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            ))

        self.comp_rotor_core = mo.Component(
            name="RotorCore",
            cross_sections=[self.rotor_core],
            material=mo.MaterialGeneric(name=self.machine_variant.rotor_iron_mat["core_material"]),
            make_solid=mo.MakeExtrude(location=mo.Location3D(), 
                    dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )

        self.comp_rotor_bar = []
        for i in range(0,self.machine_variant.Qr):
            self.comp_rotor_bar.append(mo.Component(
                name="Bar",
                cross_sections=[self.rotor_bar[i]],
                material=mo.MaterialGeneric(name=self.machine_variant.rotor_bar_mat["rotor_bar_material"]),
                make_solid=mo.MakeExtrude(location=mo.Location3D(),
                dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            ))

        self.stator_tool = self.comp_stator_core.make(tool, tool)
        self.winding_tool1 = []
        for i in range(0,self.machine_variant.Q):
            self.winding_tool1.append(self.comp_winding_layer1[i].make(tool, tool))
        self.winding_tool2 = []
        for i in range(0,self.machine_variant.Q):
            self.winding_tool2.append(self.comp_winding_layer2[i].make(tool, tool))
        self.rotor_tool = self.comp_rotor_core.make(tool, tool)
        self.rotor_bar_tool = []
        for i in range(0,self.machine_variant.Qr):
            self.rotor_bar_tool.append(self.comp_rotor_bar[i].make(tool, tool))

        return True

    def draw_machine_double_cage(self, tool):
        ####################################################
        # Adding parts objects
        ####################################################
        self.stator_core = mo.CrossSectInnerRotorStator(
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

        self.winding_layer1 = []
        for i in range (0, self.machine_variant.Q):
            self.winding_layer1.append(mo.CrossSectInnerRotorStatorRightSlot(
                name="WindingLayer1",
                stator_core=self.stator_core,
                location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],
                theta=mo.DimRadian(2 * np.pi / self.machine_variant.Q * i)),
                ))

        self.winding_layer2 = []
        for i in range (0, self.machine_variant.Q):
            self.winding_layer2.append(mo.CrossSectInnerRotorStatorLeftSlot(
                name="WindingLayer2",
                stator_core=self.stator_core,
                location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],
                theta=mo.DimRadian(2 * np.pi / self.machine_variant.Q * i)),
                ))

        self.rotor_core = mo.CrossSectInnerRotorRoundSlotsDoubleCage(
            name="RotorCore",
            dim_r_ri=mo.DimMillimeter(self.machine_variant.r_ri),
            dim_d_ri=mo.DimMillimeter(self.machine_variant.d_ri),
            dim_d_rb=mo.DimMillimeter(self.machine_variant.d_rb),
            dim_r_rb=mo.DimMillimeter(self.machine_variant.r_rb),
            dim_d_so=mo.DimMillimeter(self.machine_variant.d_rso),
            dim_w_so=mo.DimMillimeter(self.machine_variant.w_so),
            Qr=self.machine_variant.Qr,
            location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)]),
            )

        self.rotor_bar1 = []
        for i in range(0,self.machine_variant.Qr):
            self.rotor_bar1.append(mo.CrossSectInnerRotorRoundSlotsDoubleCageBar1(
                name="Bar1",
                rotor_core=self.rotor_core,
                location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],
                theta=mo.DimRadian(2 * np.pi / self.machine_variant.Qr * i)),
                ))

        self.rotor_bar2 = []
        for i in range(0,self.machine_variant.Qr):
            self.rotor_bar2.append(mo.CrossSectInnerRotorRoundSlotsDoubleCageBar2(
                name="Bar2",
                rotor_core=self.rotor_core,
                location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],
                theta=mo.DimRadian(2 * np.pi / self.machine_variant.Qr * i)),
                ))

        self.comp_stator_core = mo.Component(
            name="StatorCore",
            cross_sections=[self.stator_core],
            material=mo.MaterialGeneric(name=self.machine_variant.stator_iron_mat["core_material"]),
            make_solid=mo.MakeExtrude(location=mo.Location3D(), 
                    dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )

        self.comp_winding_layer1 = []
        for i in range(0,self.machine_variant.Q):
            self.comp_winding_layer1.append(mo.Component(
                name="WindingLayer1",
                cross_sections=[self.winding_layer1[i]],
                material=mo.MaterialGeneric(name=self.machine_variant.coil_mat["coil_material"]),
                make_solid=mo.MakeExtrude(location=mo.Location3D(), 
                dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            ))

        self.comp_winding_layer2 = []
        for i in range(0,self.machine_variant.Q):
            self.comp_winding_layer2.append(mo.Component(
                name="WindingLayer2",
                cross_sections=[self.winding_layer2[i]],
                material=mo.MaterialGeneric(name=self.machine_variant.coil_mat["coil_material"]),
                make_solid=mo.MakeExtrude(location=mo.Location3D(), 
                dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            ))

        self.comp_rotor_core = mo.Component(
            name="RotorCore",
            cross_sections=[self.rotor_core],
            material=mo.MaterialGeneric(name=self.machine_variant.rotor_iron_mat["core_material"]),
            make_solid=mo.MakeExtrude(location=mo.Location3D(), 
                    dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            )

        self.comp_rotor_bar1 = []
        for i in range(0,self.machine_variant.Qr):
            self.comp_rotor_bar1.append(mo.Component(
                name="Bar1",
                cross_sections=[self.rotor_bar1[i]],
                material=mo.MaterialGeneric(name=self.machine_variant.rotor_bar_mat["rotor_bar_material"]),
                make_solid=mo.MakeExtrude(location=mo.Location3D(),
                dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            ))

        self.comp_rotor_bar2 = []
        for i in range(0,self.machine_variant.Qr):
            self.comp_rotor_bar2.append(mo.Component(
                name="Bar2",
                cross_sections=[self.rotor_bar2[i]],
                material=mo.MaterialGeneric(name=self.machine_variant.rotor_bar_mat["rotor_bar_material"]),
                make_solid=mo.MakeExtrude(location=mo.Location3D(),
                dim_depth=mo.DimMillimeter(self.machine_variant.l_st)),
            ))

        self.stator_tool = self.comp_stator_core.make(tool, tool)
        self.winding_tool1 = []
        for i in range(0,self.machine_variant.Q):
            self.winding_tool1.append(self.comp_winding_layer1[i].make(tool, tool))
        self.winding_tool2 = []
        for i in range(0,self.machine_variant.Q):
            self.winding_tool2.append(self.comp_winding_layer2[i].make(tool, tool))
        self.rotor_tool = self.comp_rotor_core.make(tool, tool)
        self.rotor_bar_tool1 = []
        for i in range(0,self.machine_variant.Qr):
            self.rotor_bar_tool1.append(self.comp_rotor_bar1[i].make(tool, tool))
        self.rotor_bar_tool2 = []
        for i in range(0,self.machine_variant.Qr):
            self.rotor_bar_tool2.append(self.comp_rotor_bar2[i].make(tool, tool))

        return True


    def wait_greedy_search(self, tic, id_rotor_bars, id_stator_slots):
        while True:
            fname = self.config.run_folder + 'femm_found.csv'
            if os.path.exists(fname):
                with open(fname, 'r') as f:
                    data = f.readlines()
                    freq = float(data[0][:-1])
                    torque = float(data[1][:-1])
                femm.openfemm(True)
                vals_results_rotor_current, stator_slot_area, rotor_slot_area = \
                    self.femm_integrate_4_current(fname[:-4] + '.ans', self.config.fraction, id_rotor_bars, 
                            id_stator_slots, dir_output=self.config.run_folder, returnData=True)
                femm.closefemm()

                new_fname = self.config.run_folder + self.project_name + '.csv'
                # os.rename(fname, new_fname)
                with open(new_fname, 'w') as f:
                    str_results = "%g\n%g\n" % (freq, torque)
                    str_results += "%g\n%g\n" % (stator_slot_area, rotor_slot_area)
                    for el in vals_results_rotor_current:
                        str_results += "%g,%g\n" % (el.real, el.imag)
                    f.write(str_results)

                # also save for loss evaluation query # this is not good for restart, just recover your data from csv files
                self.vals_results_rotor_current = vals_results_rotor_current
                self.stator_slot_area = stator_slot_area
                self.rotor_slot_area = rotor_slot_area

                # leave the fem file for ease of reproduction
                # os.remove(fname[:-4]+'.fem')
                #os.remove(fname[:-4] + '.ans')
                #os.rename(fname[:-4] + '.fem', new_fname[:-4] + '.fem')
                break
            else:
                print('Wait for greedy search: sleep 1 sec...')
                sleep(1)
                # print clock_time() - tic, 's'
        toc = clock_time()
        logger = logging.getLogger(__name__)
        logger.debug('Time spent on femm frequency search is %g s.', toc - tic)
        return freq, torque

    def femm_integrate_4_current(self, fname, fraction, id_rotor_bars, id_stator_slots, dir_output=None, returnData=False):
        '''Make sure femm is opened
        Returns:
            [type] -- [list of complex number of rotor currents from FEMM]
        '''

        # get corresponding rotor current conditions for later static FEA
        femm.opendocument(fname)
        # physical amount of Cage
        im = self.machine_variant
        vals_results_rotor_current = []

        if self.config.double_cage == False:
            R = im.R_bar_center  # Since 5/23/2019
            angle_per_slot = 2 * np.pi / im.Qr
            THETA_BAR = 0
            for i in range(im.Qr):
                THETA = THETA_BAR
                X = R * np.cos(THETA)
                Y = R * np.sin(THETA)
                femm.mo_selectblock(X, Y)  # or you can select circuit rA rB ...
                vals_results_rotor_current.append(femm.mo_blockintegral(7))  # integrate for current
                femm.mo_clearblock()
                THETA_BAR += angle_per_slot
        else:
            R = im.R_bar1_center
            angle_per_slot = 2 * np.pi / im.Qr
            THETA_BAR = 0
            for i in range(im.Qr):
                THETA = THETA_BAR
                X = R * np.cos(THETA)
                Y = R * np.sin(THETA)
                femm.mo_selectblock(X, Y)  # or you can select circuit rA rB ...
                vals_results_rotor_current.append(femm.mo_blockintegral(7))  # integrate for current
                femm.mo_clearblock()
                THETA_BAR += angle_per_slot
            R = im.R_bar2_center
            angle_per_slot = 2 * np.pi / im.Qr
            THETA_BAR = 0
            for i in range(im.Qr):
                THETA = THETA_BAR
                X = R * np.cos(THETA)
                Y = R * np.sin(THETA)
                femm.mo_selectblock(X, Y)  # or you can select circuit rA rB ...
                vals_results_rotor_current.append(femm.mo_blockintegral(7))  # integrate for current
                femm.mo_clearblock()
                THETA_BAR += angle_per_slot

        ################################################################
        # Also collect slot area information for loss evaluation in JMAG optimization
        ################################################################
        # get stator slot area for copper loss calculation
        femm.mo_groupselectblock(id_stator_slots)
        stator_slot_area = femm.mo_blockintegral(5) / (
                    im.Q / fraction)  # unit: m^2 (verified by GUI operation)
        femm.mo_clearblock()

        # get rotor slot area for copper loss calculation
        femm.mo_groupselectblock(id_rotor_bars)
        if self.config.double_cage == False:
            rotor_slot_area = femm.mo_blockintegral(5) / (im.Qr / fraction)
        else:
            rotor_slot_area = femm.mo_blockintegral(5) / (2 * im.Qr / fraction)
        femm.mo_clearblock()

        femm.mo_close()
            # return [-el for el in vals_results_rotor_current[self.rotor_slot_per_pole:2*self.rotor_slot_per_pole]] # 用第四象限的转子电流，因为第三象限的被切了一半，麻烦！
            # vals_results_rotor_current[self.rotor_slot_per_pole:2*self.rotor_slot_per_pole]这里用的都是第四象限的转子电流了，我们后面默认用的是第三象限的转子电流，即rA1 rB1 ...，所以要反相一下(-el)
        
        # vals_results_rotor_current = [-el for el in vals_results_rotor_current[
        #                                                 self.rotor_slot_per_pole:2 * self.rotor_slot_per_pole]]
        # vals_results_rotor_current = self.femm_integrate_4_current(self.fraction)

        # if dir_output is None:
        #     dir_output = self.dir_run_sweeping

        # if returnData == False:  # no return then write to file
        #     with open(dir_output + "femm_rotor_current_conditions.txt", "w") as stream:
        #         str_results = ''
        #         for el in vals_results_rotor_current:
        #             stream.write("%g %g \n" % (el.real, el.imag))
        #     print('done. append to eddycurrent_results.txt.')
        #     return None
        # else:
        return vals_results_rotor_current, stator_slot_area, rotor_slot_area


