
CarbonFiber = {
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
    'alpha_sl_r'                 : 0.3e-6,
    'alpha_sl_t'                 : -4.7e-7
    }

Steel = {
    'shaft_material'             : 'S45C',
    'shaft_material_density'     : 7870, # kg/m3
    'shaft_youngs_modulus'       : 206E9, #Pa
    'shaft_poission_ratio'       : .3, #[]
    'shaft_therm_conductivity'   : 51.9, # W/m-k  
    'alpha_sh'                   : 1.2e-5
    }

Copper = {
    'copper_material_cost'       : 73228, # $/m3
    'copper_material_density'    : 8920,
    'copper_elec_conductivity'   : 5.7773*1e7, # S/m
    }

Air = {
    'air_therm_conductivity'     :.02624, #W/m-K
    'air_viscosity'              :1.562E-5, #m^2/s
    'air_cp'                     :1, #kJ/kg
    'air_temp'                   :25, #[C]
    }

Hub = {
       'rotor_hub_therm_conductivity':205.0, #W/m-K       
      }