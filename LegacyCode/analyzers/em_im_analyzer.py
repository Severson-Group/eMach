from time import time as clock_time
import os
from .electrical_analysis_im.FEMM_Solver import FEMM_Solver


class IM_EM_Analysis():

    def __init__(self, configuration):
        self.configuration = configuration
        self.machine_variant = None
        self.operating_point = None

    def analyze(self, problem, counter = 0):
        self.machine_variant = problem.machine
        self.operating_point = problem.operating_point
        problem.configuration = self.configuration
        ####################################################
        # 01 Setting project name and output folder
        ####################################################
        self.project_name = 'proj_%d_' % (counter)
        # Create output folder
        if not os.path.isdir(self.configuration['JMAG_csv_folder']):
            os.makedirs(self.configuration['JMAG_csv_folder'])

        self.machine_variant.fea_config_dict = self.configuration
        self.machine_variant.bool_initial_design = self.configuration['bool_initial_design']
        self.machine_variant.ID = self.project_name
        self.bool_run_in_JMAG_Script_Editor = False

        print('Run greedy_search_for_breakdown_slip...')
        femm_tic = clock_time()
        self.femm_solver = FEMM_Solver(self.machine_variant, flag_read_from_jmag=False, freq=500)  # eddy+static
        self.femm_solver.greedy_search_for_breakdown_slip(self.configuration['JMAG_csv_folder'], self.project_name,
                                                          bool_run_in_JMAG_Script_Editor=self.bool_run_in_JMAG_Script_Editor,
                                                          fraction=1)

        slip_freq_breakdown_torque, breakdown_torque, breakdown_force = self.femm_solver.wait_greedy_search(femm_tic)

        
        return slip_freq_breakdown_torque, breakdown_torque, breakdown_force








            


    


