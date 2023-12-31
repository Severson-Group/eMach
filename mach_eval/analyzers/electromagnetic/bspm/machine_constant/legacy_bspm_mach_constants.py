import numpy as np
import os
from tqdm.autonotebook import tqdm
import pandas as pd
import win32com.client

from eMach.mach_eval.analyzers.force_vector_data import (
    ProcessForceDataProblem,
    ProcessForceDataAnalyzer,
)
from eMach.mach_eval.analyzers.torque_data import (
    ProcessTorqueDataProblem,
    ProcessTorqueDataAnalyzer,
)

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
#sys.path.append("../../..")

class BSPMMachineConstantProblem:
    def __init__(
            self
            ) -> None:
        pass

class BSPMMachineConstantAnalyzer:
    """Analyzer for determining machine constants of BSPM in JMAG. 
    
    Attributes:
        project_name (str): .jproj JMAG file to evaluate.
    """
    def __init__(self, project_name:str) -> 'BSPMMachineConstantAnalyzer':
        self.project_name = project_name

        # open .jproj file and obtain initial model and study properties
        toolJd = self._open_JMAG_file()
        init_model,init_study,init_study_name,init_properties = self._get_init_study(toolJd)

        self.toolJd = toolJd
        self.init_model = init_model
        self.init_study = init_study
        self.init_study_name = init_study_name
        self.init_properties = init_properties

        # set result csv path
        self.csv_path = self._set_csv_result_path()

        print("Project File Name: " + project_name+".jproj")
        print("Initial Model Name: " + init_model.GetName())
        print("Initial Study Name: " + init_study_name)

    ######################################################################################
    #################################### Kf Kt methods ###################################
    ######################################################################################
    
    def get_Kf_Kt(self, Iq_pu:list, I_rms:float, angle_step:int=1, rev:int=3, rev_ignore:int=1):
        """Run JMAG simulation and analyze force and torque data to obtain Kf and Kt value.

        Args:
            Iq_pu (list): list of Iq per unit values to evaluate. Values should be between 0-1. 
            I_rms (float): machine rated RMS current.
            angle_step (int, optional): step size of rotational angle. Defaults to 1.
            rev (int, optional): number of revolution rotor will take in the simulation. Defaults to 3.
            rev_ignore (int, optional): number of initial revolutions to ignore from simulation to ignore eddy current effect. Defaults to 1.

        Returns:
            Kf, Kt
        """

        # Run simulations to obtain necessary data
        force_df_list, torque_df_list = self.run_Kf_Kt_simulations(Iq_pu, I_rms, angle_step, rev)

        # calculate the number of initial data point to ignore
        idx_ignore = int(360/angle_step*rev_ignore)
        print(idx_ignore)

        # extract average force value from each run
        force = []
        for force_df in force_df_list:
            force_prob = ProcessForceDataProblem(
                Fx=force_df["ForCon:1st"].iloc[idx_ignore:].to_numpy(),
                Fy=force_df["ForCon:2nd"].iloc[idx_ignore:].to_numpy())
            force_ana = ProcessForceDataAnalyzer()
            _,_,f_abs_avg,_,_ = force_ana.analyze(force_prob)
            force.append(f_abs_avg)

        # extract average torque value from each run
        torque = []
        for torque_df in torque_df_list:
            torque_prob = ProcessTorqueDataProblem(torque_df["TorCon"].iloc[idx_ignore:].to_numpy())
            torque_analyzer = ProcessTorqueDataAnalyzer()
            torque_avg,_ = torque_analyzer.analyze(torque_prob)
            torque.append(torque_avg)

        # get fitted slope value
        Iq = [np.sqrt(2)*I_rms*Iq_pu_val for Iq_pu_val in Iq_pu]
        Kt,_ = np.polyfit(Iq,torque,deg=1)
        
        Is = [np.sqrt(2)*I_rms*(1-Iq_pu_val) for Iq_pu_val in Iq_pu]
        Kf,_ = np.polyfit(Is,force,deg=1)

        print("Kt = "+str(Kt))
        print("Kf = "+str(Kf))
        return Kt, Kf 
            
    def run_Kf_Kt_simulations(self, Iq_pu:list, I_rms:float, angle_step:int, rev:int):
        """
        Run simulations in JMAG to obtain data used for determining Kf and Kt constant.
        
        Args:
            Iq_pu (list): list of Iq per unit values to evaluate. Values should be between 0-1. 
            I_rms (float): machine rated RMS current.
            angle_step (int): step size of rotational angle.
            rev (int): number of revolution rotor will take in the simulation.

        Returns:
            force_df_list, torque df_list (tuple): force and torque dataframe lists.
        """
        print("Running force Kf and torqe Kt simulations...")
        print("Angle_Step = "+str(angle_step))
        print("Number of revolution = "+str(rev))

        # iterate through each specified coordinates
        force_df_list = []
        torque_df_list = []
        tqdm_Iq_pu = tqdm(Iq_pu, desc='') 
        for idx, Iq_pu_val in enumerate(tqdm_Iq_pu):
            tqdm_Iq_pu.set_description("Run "+ str(idx+1)+"/"+str(len(Iq_pu))
                                    +" , Iq_pu = "+str(round(Iq_pu_val,2)))

            # duplicate initial study
            self.init_model.DuplicateStudyName(self.init_study_name,
                                self.init_study_name+'_Kf_Kt'
                                +'_Iq_'+str(round(Iq_pu_val,2)).replace(".", "_")
                                +'_Is_'+str(round(1-Iq_pu_val, 2)).replace(".", "_"),True)
            
            # set duplicated study as present study
            present_study = self.toolJd.GetCurrentStudy()
            
            # rotor should rotate one full revolution over 1 second
            # 1 rev/s = 60 rev/min
            speed = 60
            self._set_study_speed(present_study,speed)
            excitation_freq = self._get_elec_freq(present_study,speed)

            # set study step control
            self._set_study_steps(present_study,angle_step,rev)

            # obtain handle to circuit for present study
            circuit = present_study.GetCircuit()

            # set torque and suspension currents for all coils
            ampT = 2*Iq_pu_val*I_rms*np.sqrt(2)
            ampS = (1-Iq_pu_val)*I_rms*np.sqrt(2)

            func = self.toolJd.FunctionFactory().Composite()
            f1 = self.toolJd.FunctionFactory().Sin(ampT, excitation_freq, 0)
            # "freq" variable cannot be used here. So pay extra attension when you create new case of a different freq.
            func.AddFunction(f1)
            circuit.GetComponent("CS_t-1").SetFunction(func)

            func = self.toolJd.FunctionFactory().Composite()
            f1 = self.toolJd.FunctionFactory().Sin(ampT, excitation_freq, -120)
            func.AddFunction(f1)
            circuit.GetComponent("CS_t-2").SetFunction(func)

            func = self.toolJd.FunctionFactory().Composite()
            f1 = self.toolJd.FunctionFactory().Sin(ampT, excitation_freq, -240)
            func.AddFunction(f1)
            circuit.GetComponent("CS_t-3").SetFunction(func)

            func = self.toolJd.FunctionFactory().Composite()
            f1 = self.toolJd.FunctionFactory().Sin(ampS, excitation_freq, 0)
            f2 = self.toolJd.FunctionFactory().Sin(-ampT / 2, excitation_freq, 0)
            func.AddFunction(f1)
            func.AddFunction(f2)
            circuit.GetComponent("CS_s-1").SetFunction(func)

            func = self.toolJd.FunctionFactory().Composite()
            f1 = self.toolJd.FunctionFactory().Sin(ampS, excitation_freq, 120)
            f2 = self.toolJd.FunctionFactory().Sin(-ampT / 2, excitation_freq, -120)
            func.AddFunction(f1)
            func.AddFunction(f2)
            circuit.GetComponent("CS_s-2").SetFunction(func)

            func = self.toolJd.FunctionFactory().Composite()
            f1 = self.toolJd.FunctionFactory().Sin(ampS, excitation_freq, 240)
            f2 = self.toolJd.FunctionFactory().Sin(-ampT / 2, excitation_freq, -240)
            func.AddFunction(f1)
            func.AddFunction(f2)
            circuit.GetComponent("CS_s-3").SetFunction(func)

            # run the study
            present_study.RunAllCases()

            # extract FEA results from CSV
            force_df = self._extract_csv_results(present_study.GetName(), "Force")
            torque_df = self._extract_csv_results(present_study.GetName(),"Torque")
            force_df_list.append(force_df)
            torque_df_list.append(torque_df)

        self.force_df_list = force_df_list
        return force_df_list, torque_df_list

    ######################################################################################
    #################################### Kdelta methods ##################################
    ######################################################################################

    def get_Kdelta(self, coordinates:list, angle_step:int=1, rev:int=3, rev_ignore:int=1):
        """Run JMAG simulation and analyze force and displacement data to obtain Kdelta value.

        Args:
            coordinates (list): list of coordinates to evaluate in simulation
            angle_step (int, optional): step size of rotational angle. Defaults to 1.
            rev (int, optional): number of revolution rotor will take in the simulation. Defaults to 1.
            rev_ignore (int, optional): number of initial revolutions to ignore from simulation to ignore eddy current effect. Defaults to 1.

        Returns:
            _type_: _description_
        """
        # run simualtions on all specified coordinates
        force_df_list = self.run_Kdelta_simulations(coordinates,angle_step,rev)

        # calculate the number of initial data point to ignore
        idx_ignore = int(360/angle_step*rev_ignore)
        
        force = []
        for force_df in force_df_list:
            force_prob = ProcessForceDataProblem(
                Fx=force_df["ForCon:1st"].iloc[idx_ignore:].to_numpy(),
                Fy=force_df["ForCon:2nd"].iloc[idx_ignore:].to_numpy())
            force_ana = ProcessForceDataAnalyzer()
            _,_,f_abs_avg,_,_ = force_ana.analyze(force_prob)
            force.append(f_abs_avg)
        disp = [np.linalg.norm(coord) for coord in coordinates]

        # combine and sort force and displacement data and unzip into 
        # two seperate list after sorting
        disp, force = (list(t) for t in zip(*sorted(zip(disp,force))))

        # get fitted slope value
        K_delta,_ = np.polyfit(disp,force,deg=1)

        return K_delta

    def run_Kdelta_simulations(self, coordinates:list, angle_step:int, rev:int):
        """Run simulations in JMAG to obtain data used for determining Kdelta constant"""
        print("Running Kdelta rotor displacement simulations...")
        print("Angle_Step = "+str(angle_step))
        print("Number of revolution = "+str(rev))

        # determine if model is 2D or 3D
        is_2D = self._is_2D_model(self.init_model)
            
        force_df_list = []
        tqdm_coord = tqdm(coordinates, desc='')
        # iterate through each specified coordinates 
        for idx, coord in enumerate(tqdm_coord):
            tqdm_coord.set_description("Run " + str(idx+1)+"/"+str(len(coordinates))
                                    +" , Co-ord = "+str(coord))
            x_coord = coord[0]
            y_coord = coord[1]

            # set rotor offset depending on model type
            if is_2D:
                present_study = self._create_Kdelta_2D_study(x=x_coord,y=y_coord)
            else:
                present_study = self._create_Kdelta_3D_study(x=x_coord,y=y_coord)
 
            # set study step control
            # rotor should rotate one full revolution over 1 second
            self._set_study_steps(present_study, angle_step, rev)

            # set rotor angular velocity
            # 60 RPM = 1 rev/sec
            speed = 60
            self._set_study_speed(present_study, speed)

            # obtain handle to circuit for present study
            circuit = present_study.GetCircuit()

            # zero current for all coils
            function1 = self.toolJd.FunctionFactory().Constant(0)
            circuit.GetComponent("CS_t-1").SetFunction(function1)
            circuit.GetComponent("CS_t-2").SetFunction(function1)
            circuit.GetComponent("CS_t-3").SetFunction(function1)
            circuit.GetComponent("CS_s-1").SetFunction(function1)
            circuit.GetComponent("CS_s-2").SetFunction(function1)
            circuit.GetComponent("CS_s-3").SetFunction(function1)

            # run the study
            present_study.RunAllCases()

            # extract FEA results from CSV
            force_df = self._extract_csv_results(present_study.GetName(),"Force")
            force_df_list.append(force_df)

        self.force_df_list = force_df_list
        return force_df_list
    
    def _create_Kdelta_2D_study(self,x,y):
        """Offset rotor by enabling eccentricity setting under RotCon condition"""
        
        # duplicate initial study
        # replace all decimal in strings with underscore to avoid windows file naming error 
        self.init_model.DuplicateStudyName(self.init_study_name,
                                      self.init_study_name+'_Kdelta'
                                      +'_X'+str(x).replace(".", "_")
                                      +'_Y'+str(y).replace(".", "_"),True)
        
        present_study = self.toolJd.GetCurrentStudy()
        present_study.GetCondition(0).SetValue("UseEccentricity", 1)
        present_study.GetCondition(0).SetXYZPoint("PartOffset",x,y,0)
        present_study.GetCondition(0).SetXYZPoint("AxisOffset",x,y,0)
        return present_study

    def _create_Kdelta_3D_study(self,x,y):
        """Offset rotor by repositioning rotor in GeometryEditor"""

        # Open Geometry Editior and offset rotor from stator center
        self.toolJd.SetCurrentModel(0)
        self.init_model.RestoreCadLink()
        geomApp = self.toolJd.CreateGeometryEditor()
        
        # select rotor parts
        shaft = geomApp.GetDocument().GetAssembly().GetItem("Shaft")
        rotmag = geomApp.GetDocument().GetAssembly().GetItem("RotorMagnet")
        rotorCore = geomApp.GetDocument().GetAssembly().GetItem("NotchedRotor")
        geomApp.GetDocument().GetSelection().Add(rotorCore)
        geomApp.GetDocument().GetSelection().Add(shaft)
        geomApp.GetDocument().GetSelection().Add(rotmag)

        # translate rotor
        translation = geomApp.GetDocument().GetAssemblyManager().CreateMovePartParameter()
        translation.SetProperty("MoveX", x)
        translation.SetProperty("MoveY", y)
        geomApp.GetDocument().GetAssemblyManager().Execute(translation)

        # update model and close geometry editor
        # everytime model is updated, new model is created
        self.toolJd.GetCurrentModel().UpdateCadModel()
        geomApp.SaveCurrent()
        geomApp.Quit()

        # set current study and renanme
        present_study = self.toolJd.GetCurrentStudy()
        present_study.SetName(self.init_study_name+'_displacement'
                                        +'_X'+str(x).replace(".", "_")
                                        +'_Y'+str(y).replace(".", "_"))
        present_model = self.toolJd.GetCurrentModel()
        present_model.SetName(self.init_study_name+'_displacement'
                                        +'_X'+str(x).replace(".", "_")
                                        +'_Y'+str(y).replace(".", "_"))
        
        # align axis of rotation to center of shaft
        present_study.GetCondition("RotCon").SetXYZPoint("Origin", x, y, 1)
        present_study.GetCondition("TorCon").SetXYZPoint("Origin", x, y, 1)

        # create face set for creating symmetry boundary
        present_model.GetSetList().CreateFaceSet("Symmetry_Face_bottom")
        symmetry_face1 = present_model.GetSetList().GetSet("Symmetry_Face_bottom")
        symmetry_face1.SetUpdateByRelation(False)
        symmetry_face1.SetMatcherType("OnPlane")
        symmetry_face1.SetXYZPoint("direction", 0, 0, 1)
        symmetry_face1.SetXYZPoint("origin", 0, 0, 0)
        symmetry_face1.SetParameter("tolerance", 1e-6)
        symmetry_face1.Rebuild()

        present_model.GetSetList().CreateFaceSet("Symmetry_Face_top")
        symmetry_face2 = present_model.GetSetList().GetSet("Symmetry_Face_top")
        symmetry_face2.SetUpdateByRelation(False)
        symmetry_face2.SetMatcherType("OnPlane")
        symmetry_face2.SetXYZPoint("direction", 0, 0, 1)
        # FIND way to get coil height
        symmetry_face2.SetXYZPoint("origin", 0, 0, 22.5)
        symmetry_face2.SetParameter("tolerance", 1e-6)
        symmetry_face2.Rebuild()

        # create new symmetry boundary condition
        present_study.CreateCondition("SymmetryBoundary", "SymBound")
        sym_bound = present_study.GetCondition("SymBound")
        sym_bound.ClearParts()
        sym_bound.AddSet(symmetry_face1, 0)
        sym_bound.AddSet(symmetry_face2, 0)

        return present_study
    
    
    ######################################################################################
    #################################### Kphi methods ####################################
    ######################################################################################

    def get_Kphi(self):
        pass

    def run_Kphi_simulations(self):
        pass

    ######################################################################################

    def _get_elec_freq(self,study,speed):
        """Calculate electric frequency to acheiev specified speed

        Args:
            study (): instance of JMAG study to evaluate
            speed (float): speed of rotor in RPM

        Returns:
            freq: electric frequency in Hz
        """

        # obtain magnet pole pair value
        p = study.GetMaterial("Magnet").GetValue("Poles")/2

        # convert RPM to Hz
        freq = speed/60*p 
        return freq

    def _set_study_speed(self, study, speed=60):
        """Set rotor speed under RotCon"""
        study.GetCondition(0).SetValue("AngularVelocity",speed)
        
    def _set_study_steps(self,study,
                         angle_step:int,
                         rev:int):
        """Set the number of steps in transient study based on angle step size and number of revolutions.

        Args:
            study (): instance of JMAG study to evaluate
            angle_step (int): step size for rotational angle in deg
            rev (int): number of revolutions to evaluate study 
        """

        tran_steps = rev*360/angle_step
        study.GetStep().SetValue("Step",tran_steps)
        study.GetStep().SetValue("StepType",1)
        study.GetStep().SetValue("StepDivision",tran_steps-1)
        study.GetStep().SetValue("EndPoint", rev)

    def _is_2D_model(self,model):
        """Check if model in JMAG project is 2D"""
        if model.GetDimension() == 2:
            print("2D model detected...")
            return True
        else:
            print("3D model detected...")
            return False

    def _get_init_study(self,toolJd):
        """Obtain initial JMAG study and properties"""
        toolJd.SetCurrentModel(0)
        init_model = toolJd.GetModel(0)
        init_study = toolJd.GetStudy(0)
        init_study_name = init_study.GetName()
        init_properties = init_study.GetStudyProperties()
        return init_model,init_study,init_study_name,init_properties

    def _open_JMAG_file(self):
        """Open and load specified JMAG file"""
        toolJd = win32com.client.Dispatch("designer.Application")
        toolJd.Show()
        toolJd.load(os.path.dirname(__file__)+"/run_data/"+self.project_name+".jproj")
        return toolJd
    
    def _set_csv_result_path(self):
        """Set JMAG .csv result path and create one if not exist"""
        csv_path = os.path.dirname(__file__)+"/run_data/"+self.project_name+"_mach_const_results_csv/"

        # create result folder if not exist
        if not os.path.exists(csv_path):
            os.mkdir(csv_path)
            print("CSV result folder created at "+ csv_path)

        self.init_properties.SetValue("CsvOutputPath",csv_path)
        return csv_path

    def _extract_csv_results(self, study_name, type:str):
        """Extract coil flux linkage data from JMAG output .csv files"""
        csv_type_dict = {'Force':'_force.csv',
                         'Torque':'_torque.csv',
                         'Flux':'_flux_of_fem_coil.csv'}
        path = self.csv_path + study_name + csv_type_dict[type]
        df = pd.read_csv(path, skiprows=6)
        return df
    
##################################################################
analyzer = BSPMMachineConstantAnalyzer("BP4")

coord = []
for x in np.linspace(-0.3,0.3,3):
    for y in np.linspace(-0.3,0.3,3):
        coord.append([x,y])
coord.append([0,0.2])
coord.append([0,0.4])

Iq_pu = np.linspace(0,1,11)
analyzer.get_Kf_Kt(Iq_pu, I_rms = 18)
analyzer.get_Kdelta(coord)