import os

fea_config_dict = {
    ##########################
    # Design Specifications
    ##########################
    'DPNV'         : True,
    'p'            : 1,
    'ps'           : 2,
    'Q'            : 6,
    'J'            : 5e6, # Arms/m^2
    'Kcu'          : 0.5, # Stator slot fill/packing factor | FEMM_Solver.py is not consistent with this setting
    'Kov'          : 1.8, # Winding over length factor
    'B_st'         : 1, # [Tesla], magnetic field at stator tooth, this is used to size w_st 
    'B_sy'         : 0.9, # [Tesla], magnetic field at stator yoke, this is used to size d_sy 
    'efficiency'   : 0.95, # Guess efficiency for initial calculation
    'power_factor' : 0.7, # Guess power factor for initial calculation
    'n_m'          : 1, # Number of magnet segments
    ##########################
    # Initial parameters
    ##########################
    'initial_v_tip'        : 200, # [m/s], tip speed
    'initial_delta'        : 0.75*1e-3, # [m] initial airgap
    'initial_dsl'          : 2*1e-3, # [m] initial sleeve thickness
    'initial_B_delta'      : 0.5, # [Tesla], Magnetic loading
    'initial_A'            : 100000, # Electric loading, A_pk/m
    'initial_Q_flow'       : 0, 
    ##########################
    # Rated operating conditions
    ##########################
    'mech_power'              : 5.5e3, # kW
    'mech_omega'              : 16755.16, # rad/s
    'voltage_rating'          : 240, # Vrms (line-to-line, Wye-Connect)
    'Iq_rated_ratio'          : 0.975, # per rated coil currents
    # 'TORQUE_CURRENT_RATIO'    : 0.95,
    # 'SUSPENSION_CURRENT_RATIO': 0.05,
    ##########################
    # Operating point
    ##########################
    'Id_ratio'      : 0,        # per rated coil currents
    'Iq_ratio'      : 0.975,    # per rated coil currents
    'Ix_ratio'      : 0,        # per rated coil currents
    'Iy_ratio'      : 0.025,    # per rated coil currents
    'operating_zQ'  : 1,     # This will be used when evaluating designs at operating point
    'operating_l_st' : 1,     # This will be used when evaluating designs at operating point
    ##########################
    # Material property
    ##########################
    # Core property 
    'core_material'              : 'Arnon5', #'M19','Arnon5', 
    'core_material_density'      : 7650, # kg/m3
    'core_youngs_modulus'        : 185E9, # Pa
    'core_poission_ratio'        : .3, 
    'core_material_cost'         : 17087, # $/m3
    'core_ironloss_a'            : 1.58, 
    'core_ironloss_b'            : 1.17, 
    'core_ironloss_Kh'           : 78.94, # W/m3
    'core_ironloss_Ke'           : 0.0372, # W/m3
    'core_therm_conductivity'    : 28, # W/m-k
    # Magnet property 
    'magnet_material'            : 'N40', 
    'magnet_material_density'    : 7450, # kg/m3
    'magnet_youngs_modulus'      : 160E9, # Pa
    'magnet_poission_ratio'      :.24,
    'magnet_material_cost'       : 712756, # $/m3
    'magnetization_direction'    : 'Parallel',
    'B_r'                        : 1.285, # Tesla, magnet residual flux density
    'mu_r'                       : 1.062, # magnet relative permeability
    'magnet_max_temperature'     : 80, # deg C
    'magnet_max_rad_stress'      : 0, # Mpa  
    'magnet_therm_conductivity'  : 8.95, # W/m-k
    # Sleeve property 
    'sleeve_material'            : 'CarbonFiber',
    'sleeve_material_density'    : 1800, # kg/m3
    'sleeve_youngs_th_direction' : 125E9,  #Pa
    'sleeve_youngs_p_direction'  : 8.8E9,  #Pa
    'sleeve_poission_ratio_p'    :.015,
    'sleeve_poission_ratio_tp'   :.28,
    'sleeve_safety_factor'       : 1.5, #
    'sleeve_max_tan_stress'      : 1950E6, # Pa
    'sleeve_max_rad_stress'      : -100E6, # Pa
    'sleeve_therm_conductivity'  : 0.71, # W/m-k
    # Shaft property 
    'shaft_material'             : 'Steel',
    'shaft_material_density'     : 7870, # kg/m3
    'shaft_youngs_modulus'       : 206E9, #Pa
    'shaft_poission_ratio'       : .3, #[]
    'shaft_therm_conductivity'   : 51.9, # W/m-k  
    # Copper property 
    'copper_material_cost'       : 73228, # $/m3
    'copper_elec_conductivity'   : 5.7773*1e7, # S/m
    # Air property
    'air_therm_conductivity'     :.02624, #W/m-K
    'air_viscosity'              :1.562E-5, #m^2/s
    'air_cp'                     :1, #kJ/kg
    'air_temp'                   :25, #[C]
    # Rotor Hub Property
    'rotor_hub_therm_conductivity':205.0, #W/m-K
    ##########################
    # FEA Setting
    ##########################
    'TranRef-StepPerCycle'       : 40, # FEMM: 5 deg   # 360 to be precise as FEMM: 0.5 deg
    'number_of_revolution_1TS'   : 3,
    'number_of_revolution_2TS'   : 0.5, 
    'number_of_steps_per_rev_1TS': 8, # Should be TSS actually... Also, number_of_steps_1stTTS is not implemented.
    'number_of_steps_per_rev_2TS': 64, # use a multiples of 4! # 8*32 # steps for half period (0.5). That is, we implement two time sections, the 1st section lasts half slip period and the 2nd section lasts half fandamental period.
    'number_cycles_prolonged'    : 1, # 150
    'OnlyTableResults'           : False, 
    'Restart'                    : False, # restart from frequency analysis is not needed, because SSATA is checked and JMAG 17103l version is used.
    'MultipleCPUs'               : True,
    'JMAG_Scheduler'             : False,
    'max_nonlinear_iterations'   : 50, 
    ##########################
    # Mesh settings
    ##########################
    'mesh_size'                  : 4*1e-3, # m
    'mesh_magnet_size'           : 2*1e-3, # m
    'mesh_radial_division'       : 4,
    'mesh_circum_division'       : 720,
    'mesh_air_region_scale'      : 1.15,
    ##########################
    # Optimization
    ##########################
    'use_weights':'cost_function_O2', # For DE. | This is not used in MOO
#    'bool_refined_bounds': False, # Don't use this. Use classic bounds based on an initial design instead.
    ##########################
    # System Control
    ##########################
    'designer.Show'                                : False,
    'local_sensitivity_analysis'                   : False,
    'local_sensitivity_analysis_number_of_variants': 20,
    'delete_results_after_calculation'             : False, # check if True can we still export Terminal Voltage?
    'post_process'                                 : False,
    'do_not_eval_pop'                              : False, 
    'manual_set_init_pop'                          : False,
    'eval_designs_at_operating'                    : False,
    'read_data_from_v2'                            : False,
    'resume_optimization'                          : False, # resume optimization from the swarm survivor data if available
    ##########################
    # System path
    ##########################
    'dir_interpreter': os.path.abspath(''),
    'dir_parent'     : os.path.abspath('') + '/../',
    'dir_codes'      : os.path.abspath(''),
    'pc_name'        : os.environ["COMPUTERNAME"],
    'run_folder'     : os.path.abspath('') + '/../run_data/' ,  #storing FEM files path
    'JMAG_csv_folder': os.path.abspath('') + '/../run_data/JMAG_csv/',
    'eval_folder'     : os.path.abspath('') + '/../run_data/' ,  #storing FEM files path
}




