
DesignSpec = {
    'DPNV'              : True,
    'p'                 : 2,
    'ps'                : 1,
    'Q'                 : 24,
    'J'                 : 5e6,  # Arms/m^2
    'wire_A'            : 2*1e-6,  # cross sectional area of conductors m^2
    'Kcu'               : 0.5,  # Stator slot fill/packing factor | FEMM_Solver.py is not consistent with this setting
    'Kov'               : 1.8,  # Winding over length factor
    'rated_speed'       : 2617.993875,  # rated speed in ead/s
    'rated_power'       : 50e3,  # rated power in W
    'voltage_rating'    : 480,  # line-line voltage rating
    }

