import numpy as np 
import pandas as pd
from tqdm import tqdm
import win32com.client
from ..electrical_analysis.JMAG import JMAG
from .....machines.bspm import BSPM_Machine, BSPM_Machine_Oper_Pt
from ...bspm.jmag_2d_config import JMAG_2D_Config
from ...bspm.jmag_2d import BSPM_EM_Analyzer
from typing import Tuple
###########################################################################
from functools import cached_property, lru_cache
# @lru_cache decoractor saves the return value of the method, 
# method will run once and the return value will be saved, from then everytime 
# the method is called it will simply return the saved return value, 
# sigificantly reducing computation time
###########################################################################

from ....force_vector_data import (
    ProcessForceDataProblem,
    ProcessForceDataAnalyzer
)

from ....torque_data import (
    ProcessTorqueDataProblem,
    ProcessTorqueDataAnalyzer
)

class BSPMMachineConstantProblem:
    def __init__(
            self,
            machine:BSPM_Machine,
            operating_point: BSPM_Machine_Oper_Pt,
            solve_Kf: bool = True,
            solve_Kt: bool = True,
            solve_Kdelta: bool = True,
            solve_Kphi: bool = True,
            ) -> 'BSPMMachineConstantProblem':
        """BSPMMachineConstantProblem Class

        Args:
            machine (BSPM_Machine): instance of `BSPM_Machine`
            operating_point (BSPM_Machine_Oper_Pt): instance of `BSPM_Machine_Oper_Pt`
            solve_Kf (bool, optional): solve force constant. Defaults to True.
            solve_Kt (bool, optional): solve torque constant. Defaults to True.
            solve_Kdelta (bool, optional): solve displacment constant. Defaults to True.
            solve_Kphi (bool, optional): solve back-emf constant. Defaults to True.

        Returns:
            BSPMMachineConstantProblem: instance of BSPMMachineConstantProblem
        """
        self.machine = machine
        self.operating_point = operating_point
        self.solve_Kf = solve_Kf
        self.solve_Kdelta = solve_Kdelta
        self._validate_attr()
        
    def _validate_attr(self):
        if not isinstance(self.machine,BSPM_Machine):
            raise TypeError(
                'Invalid machine type, must be BSPM_Machine.'
                )
        
        if not isinstance(self.operating_point, BSPM_Machine_Oper_Pt):
            raise TypeError(
                'Invalid settings type, must be BSPM_Machine_Oper_Pt.'
                )

class BSPMMachineConstantAnalyzer(BSPM_EM_Analyzer):
    def __init__(
            self,
            configuration: JMAG_2D_Config,
            **kwargs
            ): 
        self.configuration = configuration
        super().__init__(self.configuration)

        ############# Simulation Steps #############
        # Unless kwargs are provided, analyzer will use default values
        # kwargs.get(key, default_val)
        self.Iq_step = kwargs.get('Iq_step',10)

        coord = []
        for x in np.linspace(-0.3,0.3,3):
            for y in np.linspace(-0.3,0.3,3):
                coord.append([x,y])
        self.Kdelta_coordinates = kwargs.get('Kdelta_coord',coord)
        self.Kphi_speed = np.linspace(0,160000,11)

    def analyze(self, problem: BSPMMachineConstantProblem):

        self.problem = problem
        self.machine = problem.machine
        self._validate_attr()

        # Run initial analysis to build the model 
        print('Performing initial run...')
        super().analyze(self.problem)
        print('Initial run complete...')
    
        # open .jproj file and obtain initial model and study properties
        print(f'Re-opening {self.project_name}.jproj')
        self.toolJd = self._open_JMAG_file()

        (self.init_model,
         self.init_study,
         self.init_study_name,
         self.init_properties) = self._get_init_study(self.toolJd)

           
    @cached_property
    def Kf(self)->float:
        "Machine Force Constant"
        Is_list, force = self.Kf_data
        Kf,_ = np.polyfit(Is_list,force,deg=1)
        return Kf 
    
    @cached_property
    def Kt(self)->float:
        "Machine Torque Constant"
        Iq_list, torque = self.Kt_data
        Kt,_ = np.polyfit(Iq_list,torque,deg=1)
        return Kt
    
    @cached_property
    def Kdelta(self)->float:
        "Machine Displacement Constant"
        disp,force = self.Kdelta_data
        Kdelta,_ = np.polyfit(disp,force,deg=1)
        return Kdelta
    
    @cached_property
    def Kphi(self)->float:
        "Machine Back-EMF Constant"
        speed, bemf = self.Kphi_data
        Kphi,_ = np.polyfit(speed,bemf,deg=1)
        return Kphi

    @cached_property
    def Kf_data(self)->Tuple[list,list]:
        # run simulations and extract data from JMAG
        _,Is_list,_,force_df_list = self.run_Kf_Kt_simulations()

        # determine average torque in each simulation run
        force = np.zeros(len(force_df_list))
        for idx, force_df in enumerate(force_df_list):
            force_prob = ProcessForceDataProblem(
                Fx=force_df["ForCon:1st"].iloc[self.idx_ignore:].to_numpy(),
                Fy=force_df["ForCon:2nd"].iloc[self.idx_ignore:].to_numpy()
                )
            force_ana = ProcessForceDataAnalyzer()
            _,_,f_abs_avg,_,_ = force_ana.analyze(force_prob)
            force[idx] = f_abs_avg

        return Is_list, force
    
    @cached_property
    def Kt_data(self)->Tuple[list,list]:
        # run simulations and extract data from JMAG
        Iq_list, _, torque_df_list, _ = self.run_Kf_Kt_simulations()

        # determine average torque in each simulation run
        torque = np.zeros(len(torque_df_list))
        for idx, torque_df in enumerate(torque_df_list):
            torq_prob = ProcessTorqueDataProblem(
                torque_df["TorCon"].iloc[self.idx_ignore:].to_numpy()
                )
            torq_analyzer = ProcessTorqueDataAnalyzer()
            torq_avg,_ = torq_analyzer.analyze(torq_prob)
            torque[idx] = torq_avg

        return Iq_list, torque
    
    
    @cached_property
    def Kdelta_data(self)->list:
        """Analyze force and displacement data"""
        force_df_list = self.run_Kdelta_simulations()

        force = []
        for force_df in force_df_list:
            force_prob = ProcessForceDataProblem(
                Fx=force_df["ForCon:1st"].iloc[self.idx_ignore:].to_numpy(),
                Fy=force_df["ForCon:2nd"].iloc[self.idx_ignore:].to_numpy())
            force_ana = ProcessForceDataAnalyzer()
            _,_,f_abs_avg,_,_ = force_ana.analyze(force_prob)
            force.append(f_abs_avg)
        disp = [np.linalg.norm(coord) for coord in self.Kdelta_coordinates]

        # combine and sort force and displacement data and unzip into 
        # two seperate list after sorting
        disp, force = (list(t) for t in zip(*sorted(zip(disp,force))))
        return disp, force
    
    @cached_property
    def Kphi_data(self):
        """Analyze back-EMF data from Kphi simulations"""
        bemf_df_list = self.run_Kphi_simulations()
        
        bemf = []
        for bemf_df in bemf_df_list:
            phase_voltage = bemf_df["Terminal_Wt"].iloc[self.idx_ignore:]
            if len(phase_voltage) == 0:
                rms_voltage = 0
            else:
                rms_voltage = np.sqrt(sum(np.square(phase_voltage)) / len(phase_voltage))
            bemf.append(rms_voltage)

        return self.Kphi_speed, bemf
    
    @lru_cache
    def run_Kf_Kt_simulations(self)->Tuple[list, list, list, list]:
        """_summary_

        Returns:
            Tuple[list, list, list, list]: _description_
        """

        # define torque and suspension current for simulation
        Iq_list = np.linspace(
            0,np.sqrt(2)*self.machine.Rated_current,self.Iq_step)
        Is_list = np.sqrt(2)*self.machine.Rated_current - Iq_list

        force_df_list = []
        torque_df_list = []

        print('==============================================================')
        print('Running Kf and Kt simulations ......')
        for idx, (Iq_val,Is_val) in enumerate(
            tqdm(zip(Iq_list,Is_list),total=len(Iq_list))):

            # duplicate initial study
            self.init_model.DuplicateStudyName(self.init_study_name,
                                f"{self.init_study_name}_Kf_Kt_step{idx}",True)
            
            present_study = self.toolJd.GetCurrentStudy()
            
            # obtain handle to circuit for present study
            circuit = present_study.GetCircuit()
            self._set_circuit_current_value(
                circuit, 
                ampT=2*Iq_val, 
                ampS=Is_val, 
                freq=super().excitation_freq)
            present_study.RunAllCases()

            # extract FEA results from CSV
            force_df = self._extract_csv_results(present_study.GetName(), "Force")
            torque_df = self._extract_csv_results(present_study.GetName(),"Torque")
            force_df_list.append(force_df)
            torque_df_list.append(torque_df)
        
        return Iq_list, Is_list, torque_df_list, force_df_list
    
    @lru_cache
    def run_Kdelta_simulations(self)->list:
        """Script to perform Kdelta simulations in JMAG.
        
        When called, script will either use default list of coordinates or 
        user-defined kwargs `Kdelta_coord` if provided.

        Must follow the following format

        Returns:
            list: list of pd.Dataframes containing force results from simulations
        """
        
        print('==============================================================')
        print('Running Kdelta simulations ......')

        force_df_list = []
        for coord in tqdm(self.Kdelta_coordinates):

            study_name = f'{self.init_study_name}_Kdelta_X{coord[0]}_Y{coord[1]}'
            study_name = study_name.replace(".", "_")

            # duplicate initial study
            self.init_model.DuplicateStudyName(
                self.init_study_name,
                study_name,
                True)
            
            # set rotor displacment 
            present_study = self.toolJd.GetCurrentStudy()
            present_study.GetCondition(0).SetValue("UseEccentricity", 1)
            present_study.GetCondition(0).SetXYZPoint(
                "PartOffset",coord[0],coord[1],0)
            present_study.GetCondition(0).SetXYZPoint(
                "AxisOffset",coord[0],coord[1],0)
           
            # obtain handle to circuit for present study
            circuit = present_study.GetCircuit()
            self._set_circuit_current_value(
                circuit,ampT=0,ampS=0, freq=0)
            present_study.RunAllCases()

            # extract FEA results from CSV
            force_df = self._extract_csv_results(
                present_study.GetName(),"Force")
            force_df_list.append(force_df)

        return force_df_list
    
    @lru_cache
    def run_Kphi_simulations(self):
        """Script to run Kdelta simulations in JMAG 
        
        Script uses default list of coordinates or user-defined kwargs `Kdelta_speed`

        Returns:
            _type_: _description_
        """
            
        print('==============================================================')
        print("Running Kphi simulations ......")
        
        bemf_df_list = []
        for speed in tqdm(self.Kphi_speed):

            # duplicate initial study
            self.init_model.DuplicateStudyName(
                self.init_study_name,
                f'{self.init_study_name}_Kphi_{str(round(speed,6)).replace(".", "_")}',
                True)
            
            # set rotor speed
            present_study = self.toolJd.GetCurrentStudy()
            present_study.GetCondition(0).SetValue("AngularVelocity",speed)

            # obtain handle to circuit for present study
            circuit = present_study.GetCircuit()
            self._set_circuit_current_value(
                circuit,ampT=0,ampS=0,freq=0)
            present_study.RunAllCases()

            # extract FEA results from CSV
            bemf_df = self._extract_csv_results(present_study.GetName(),"Voltage")
            bemf_df_list.append(bemf_df)

        return bemf_df_list
    
    @cached_property
    def idx_ignore(self)->int:
        """Number of initial data points to ignore for first time step 1TS"""
        idx_ignore = int(self.configuration.no_of_rev_1TS
                         *self.configuration.no_of_steps_per_rev_1TS)
        return idx_ignore

    @cached_property
    def project_file_path(self)->str:
        """Path to JMAG .jproj file"""
        path = f'{self.configuration.run_folder}{self.project_name}.jproj'
        return path
    
    def _set_circuit_current_value(self,circuit,ampT,ampS,freq):
        """Set DPNV circuit current sources to specified values"""

        torq_current_source = ['CS_t-1', 'CS_t-2', 'CS_t-3']
        sus_current_source = ['CS_s-1', 'CS_s-2', 'CS_s-3']
        
        for idx, source in enumerate(torq_current_source):
            func = self.toolJd.FunctionFactory().Composite()
            f1 = self.toolJd.FunctionFactory().Sin(ampT, freq, -120*idx)
            func.AddFunction(f1)
            circuit.GetComponent(source).SetFunction(func)

        for idx, source in enumerate(sus_current_source):
            func = self.toolJd.FunctionFactory().Composite()
            f1 = self.toolJd.FunctionFactory().Sin(
                ampS, freq, 120*idx)
            f2 = self.toolJd.FunctionFactory().Sin(
                -ampT / 2, freq, -120*idx)
            func.AddFunction(f1)
            func.AddFunction(f2)
            circuit.GetComponent(source).SetFunction(func)
    
    def _extract_csv_results(self, study_name, type:str):
        """Extract JMAG output from .csv file"""
        csv_type_dict = {'Force':'_force.csv',
                         'Torque':'_torque.csv',
                         'Flux':'_flux_of_fem_coil.csv'}
        path = self.configuration.jmag_csv_folder + study_name + csv_type_dict[type]
        df = pd.read_csv(path, skiprows=6)
        return df
        
    def _open_JMAG_file(self):
        """Open and load specified JMAG file"""
        toolJd = win32com.client.Dispatch("designer.Application")
        toolJd.Show()
        toolJd.load(self.project_file_path)
        return toolJd

    def _get_init_study(self,toolJd):
        """Obtain initial JMAG study and properties"""
        toolJd.SetCurrentModel(0)
        model = toolJd.GetModel(0)
        study = toolJd.GetStudy(0)
        study_name = study.GetName()
        properties = study.GetStudyProperties()
        return model,study,study_name,properties

    def _validate_attr(self):     
        """Validate input attributes"""   
        if not isinstance(self.problem, BSPMMachineConstantProblem):
            raise TypeError(
                'Invalid problem type, must be BSPMMachineConstantProblem.'
                )
        
        if not isinstance(self.configuration, JMAG_2D_Config):
            raise TypeError(
                'Invalid configuration type, must be JMAG_2D_Config.'
                )

class BSPMMachineConstantAnalyzer3D(BSPMMachineConstantAnalyzer):
    def __init__(self, 
                 problem: BSPMMachineConstantProblem, 
                 configuration: JMAG_2D_Config):
        super().__init__(problem, configuration)