# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 09:58:13 2021

@author: Martin Johnson
"""
import MechEval as me
import numpy as np
import copy
import pygmo as pg
from matplotlib import pyplot as plt

##############################################################################
############################## Define Machine ################################
##############################################################################
class ExampleMachine(me.Machine):
    """Machine Object for this optimization"""
    def __init__(self,design_param_dict):
        if ExampleMachine.check_required_properites(design_param_dict):
            for [key,value] in design_param_dict.items():
                setattr(self,key,value)
        else:
            missing_values=ExampleMachine.get_missing_properties(design_param_dict)
            raise(me.MissingValueError(missing_values,
                                    ('Missing inputs to initilize in'+str(ExampleMachine))))
        
    
    @classmethod
    def check_required_properites(cls,design_param_dict):
        """Checks to see if required inputs are available in input dict"""
        if cls.get_missing_properties(design_param_dict)==[]:
            return True
        else:
            return False
    
    @classmethod
    def get_missing_properties(cls,design_param_dict):
        """Returns missing values from input dict"""
        missing_values=[]
        for value in cls.required_properites() :
            if value in design_param_dict:
                pass
            else:
                missing_values.append(value)
        return missing_values
    
    @classmethod
    def required_properites(cls):
        return ['r_ro','d_m','delta','d_sy','r_sh','r_so','shaft_mat','PM_mat']
    
class Material:
    """Dummy Class to hold material information"""
    def __init__(self):
        pass

##############################################################################
############################## Define Architect ################################
##############################################################################
class ExampleArchitect(me.Architect):
    

    def __init__(self):
        """Initialize the Architect"""
        pass
    
    def create_new_design(self,x) -> "me.Machine":
        design_param_dict={'r_ro':x[0],
                           'd_m':x[1],
                           'delta':x[2],
                           'd_sy':x[3],}
        design_param_dict['r_sh']=(design_param_dict['r_ro']-
                                    design_param_dict['d_m'])
        design_param_dict['r_so']=(design_param_dict['r_ro']+
                                    design_param_dict['delta']+
                                    design_param_dict['d_sy'])
        shaft_mat=Material()
        shaft_mat.E=200E9
        shaft_mat.rho=7500
        design_param_dict['shaft_mat']=shaft_mat
        PM_mat=Material()
        PM_mat.B_r=1.28
        design_param_dict['PM_mat']=PM_mat
        machine=ExampleMachine(design_param_dict)
        return machine

##############################################################################
############################## Define Designer ################################
##############################################################################

class Settings:
    def __init__(self):
        pass

class ExampleDesigner(me.Designer):
    def __init__(self,arch):
        self.arch=arch
    def createDesign(self,x)->'me.Design':
        machine=self.arch.create_new_design(x)
        setting=Settings()
        setting.A_hat=80E3
        setting.v_tip=200
        setting.k_s=1.5
        setting.B_st_sat=1.2
        setting.P_m_prime=100
        setting.P_st_prime=100
        design=me.Design(machine,setting)
        return design

##############################################################################
############################ Define EvalSteps ################################
##############################################################################

class OperatingPoint:
    def __init__(self):
        pass

##################
##### Step 1 #####
##################

#Magnetic Loading

class MagneticLoadingAnalyzer(me.Analyzer):
    """This Class Performs Magnetic Loading Analysis"""
    
    def __init__(self):
        pass
    def analyze(self,problem):
        B_r=problem.B_r
        d_m=problem.d_m
        delta=problem.delta
        r_ro=problem.r_ro
        d_sy=problem.d_sy
        B_st_sat=problem.B_st_sat
        
        B_m=B_r*d_m/(d_m+delta)
        B_st=(2*np.pi*r_ro/d_sy)*B_m
        if B_st>=B_st_sat:
            B_st=B_st_sat
            B_m=(d_sy/(2*np.pi*r_ro))*B_st 
        return [B_m,B_st]
    
class  MagneticLoadingProblem(me.Problem):
    """Object that gets passed into Analyzer"""
    def __init__(self,machine,op):
        self.B_r=machine.PM_mat.B_r
        self.d_m=machine.d_m
        self.delta=machine.delta
        self.r_ro=machine.r_ro
        self.d_sy=machine.d_sy
        self.B_st_sat=op.B_st_sat
        

class MagneticLoadingProblemDefinition(me.ProblemDefinition):
    """Converts a State into a problem"""
    def __init__(self):
        pass
    def getProblem(self,state):
        op=OperatingPoint()
        op.B_st_sat=state.design.setting.B_st_sat
        problem=MagneticLoadingProblem(state.design.machine, op)
        return problem
class MagneticLoadingPostAnalyzer(me.PostAnalyzer):
    """Converts a results and intput state into output state"""
    def __init(self):
        pass
    def getNextState(self,results:'me.Results',stateIn:'me.State')->'me.State':
        stateOut=copy.deepcopy(stateIn)
        stateOut.stateConditions.B_m= results[0]
        stateOut.stateConditions.B_st= results[1]
        return stateOut

##################
##### Step 2 #####
##################

#Omega Calculation
class OmegaAnalyzer(me.Analyzer):
    def __init__(self):
        pass
    def analyze(self,problem):
        r_ro=problem.r_ro
        v_tip=problem.v_tip
        omega= v_tip/r_ro
        return omega
    
class  OmegaProblem(me.Problem):
    def __init__(self,machine,op):
        self.r_ro=machine.r_ro
        self.v_tip=op.v_tip
        
class OmegaProblemDefinition(me.ProblemDefinition):
    def __init__(self):
        pass
    def getProblem(self,state):
        op=OperatingPoint()
        op.v_tip=state.design.setting.v_tip
        problem=OmegaProblem(state.design.machine,op)
        return problem
    
class OmegaPostAnalyzer(me.PostAnalyzer):
    def __init(self):
        pass
    def getNextState(self,results:'me.Results',stateIn:'me.State')->'me.State':
        stateOut=copy.deepcopy(stateIn)
        stateOut.stateConditions.omega= results
        return stateOut

##################
##### Step 3 #####
##################

#Length Calculation
class LengthAnalyzer(me.Analyzer):
    def __init__(self):
        pass
    def analyze(self,problem):
        E=problem.E
        r_sh=problem.r_sh
        rho=problem.rho
        omega=problem.omega
        k_s=problem.k_s
        
        I=.25*np.pi*r_sh**4
        A=np.pi*r_sh**2
        BL=4.73
        L=( ((BL**4)/((k_s*omega)**2)) *(E*I/(rho*A)) )**(1/4)
        return L
    
class  LengthProblem(me.Problem):
    def __init__(self,machine,op):
        self.r_sh=machine.r_sh
        self.E=machine.shaft_mat.E
        self.rho=machine.shaft_mat.rho
        self.omega=op.omega
        self.k_s=op.k_s
        
class LengthProblemDefinition(me.ProblemDefinition):
    def __init__(self):
        pass
    def getProblem(self,state):
        op=OperatingPoint()
        op.omega=state.stateConditions.omega
        op.k_s=state.design.setting.k_s
        problem=LengthProblem(state.design.machine, op)
        return problem
    
class LengthPostAnalyzer(me.PostAnalyzer):
    def __init(self):
        pass
    def getNextState(self,results:'me.Results',stateIn:'me.State')->'me.State':
        stateOut=copy.deepcopy(stateIn)
        stateOut.design.machine.L=results
        return stateOut

##################
##### Step 4 #####
##################

#Torque Calculation
class TorqueAnalyzer(me.Analyzer):
    def __init__(self):
        pass
    def analyze(self,problem):
        V_r=problem.V_r
        B_m=problem.B_m
        A_hat=problem.A_hat
        T=V_r*B_m*A_hat
        return T
    
class  TorqueProblem(me.Problem):
    def __init__(self,machine,op):
        self.V_r=np.pi*(machine.r_ro**2)*machine.L
        self.B_m=op.B_m
        self.A_hat=op.A_hat
class TorqueProblemDefinition(me.ProblemDefinition):
    def __init__(self):
        pass
    def getProblem(self,state):
        op=OperatingPoint()
        op.B_m=state.stateConditions.B_m
        op.A_hat=state.design.setting.A_hat
        problem=TorqueProblem(state.design.machine, op)
        return problem
    
class TorquePostAnalyzer(me.PostAnalyzer):
    def __init(self):
        pass
    def getNextState(self,results:'me.Results',stateIn:'me.State')->'me.State':
        stateOut=copy.deepcopy(stateIn)
        stateOut.stateConditions.T=results
        return stateOut

##################
##### Step 5 #####
##################

#Power Calculation
class PowerAnalyzer(me.Analyzer):
    def __init__(self):
        pass
    def analyze(self,problem):
        T=problem.T
        omega=problem.omega
        P=T*omega
        return P
    
class PowerProblem(me.Problem):
    def __init__(self,machine,op):
        self.T=op.T
        self.omega=op.omega
class PowerProblemDefinition(me.ProblemDefinition):
    def __init__(self):
        pass
    def getProblem(self,state):
        op=OperatingPoint()
        op.T=state.stateConditions.T
        op.omega=state.stateConditions.omega
        problem=PowerProblem(state.design.machine, op)
        return problem
    
class PowerPostAnalyzer(me.PostAnalyzer):
    def __init(self):
        pass
    def getNextState(self,results:'me.Results',stateIn:'me.State')->'me.State':
        stateOut=copy.deepcopy(stateIn)
        stateOut.stateConditions.P=results
        return stateOut

##################
##### Step 6 #####
##################

#Loss Calculation
class LossAnalyzer(me.Analyzer):
    def __init__(self):
        pass
    def analyze(self,problem):
        d_m=problem.d_m
        B_st=problem.B_st
        omega=problem.omega
        delta=problem.delta
        P_m_prime=problem.P_m_prime
        P_st_prime=problem.P_st_prime
        Loss_m=P_m_prime*d_m**1
        Loss_st=P_st_prime*B_st**1
        Loss_wind=((1/delta)*omega)*(1*np.sin(1000*delta))**2
        Loss_total=Loss_m+Loss_st+Loss_wind
        return [Loss_m,Loss_st,Loss_total]
    
class LossProblem(me.Problem):
    def __init__(self,machine,op):
        self.d_m=machine.d_m
        self.B_st=op.B_st
        self.P_m_prime=op.P_m_prime
        self.P_st_prime=op.P_st_prime
        self.omega=op.omega
        self.delta=machine.delta
        
class LossProblemDefinition(me.ProblemDefinition):
    def __init__(self):
        pass
    def getProblem(self,state):
        op=OperatingPoint()
        op.B_st=state.stateConditions.B_st
        op.P_m_prime=state.design.setting.P_m_prime
        op.P_st_prime=state.design.setting.P_st_prime
        op.omega=state.stateConditions.omega
        problem=LossProblem(state.design.machine, op)
        return problem
    
class LossPostAnalyzer(me.PostAnalyzer):
    def __init(self):
        pass
    def getNextState(self,results:'me.Results',stateIn:'me.State')->'me.State':
        stateOut=copy.deepcopy(stateIn)
        stateOut.stateConditions.Loss_m=results[0]
        stateOut.stateConditions.Loss_st=results[1]
        stateOut.stateConditions.Loss_total=results[2]
        return stateOut

##################
##### Step 7 #####
##################

#Efficiency Calculation
class EfficiencyAnalyzer(me.Analyzer):
    def __init__(self):
        pass
    def analyze(self,problem):
        P=problem.P
        Loss_total=problem.Loss_total
        eff=(P-Loss_total)/P
        return eff
    
class EfficiencyProblem(me.Problem):
    def __init__(self,machine,op):
        self.P=op.P
        self.Loss_total=op.Loss_total
        
class EfficiencyProblemDefinition(me.ProblemDefinition):
    def __init__(self):
        pass
    def getProblem(self,state):
        op=OperatingPoint()
        op.P=state.stateConditions.P
        op.Loss_total=state.stateConditions.Loss_total
        problem=EfficiencyProblem(state.design.machine, op)
        return problem
    
class EfficiencyPostAnalyzer(me.PostAnalyzer):
    def __init(self):
        pass
    def getNextState(self,results:'me.Results',stateIn:'me.State')->'me.State':
        stateOut=copy.deepcopy(stateIn)
        stateOut.stateConditions.eff=results
        return stateOut
    
##################
##### Step 8 #####
##################

#Power Density Calculation
class PowerDensityAnalyzer(me.Analyzer):
    def __init__(self):
        pass
    def analyze(self,problem):
        P=problem.P
        V_m=problem.V_m
        P_density=P/V_m
        return P_density
    
class PowerDensityProblem(me.Problem):
    def __init__(self,machine,op):
        self.P=op.P
        self.V_m=machine.L*np.pi*(machine.r_so**2-
                                  (machine.r_so-machine.delta)**2+
                                  machine.r_ro**2)
        
class PowerDensityProblemDefinition(me.ProblemDefinition):
    def __init__(self):
        pass
    def getProblem(self,state):
        op=OperatingPoint()
        op.P=state.stateConditions.P
        problem=PowerDensityProblem(state.design.machine, op)
        return problem
    
class PowerDensityPostAnalyzer(me.PostAnalyzer):
    def __init(self):
        pass
    def getNextState(self,results:'me.Results',stateIn:'me.State')->'me.State':
        stateOut=copy.deepcopy(stateIn)
        stateOut.stateConditions.P_density=results
        return stateOut
    
##############################################################################
############################ Define Objectives ###############################
##############################################################################

class ExampleObjective(me.Objective):
    def getObjectives(self,fullResults)->'tuple':
        finalResults=fullResults[-1]
        finalState=finalResults[0][0]
        objs=(-finalState.stateConditions.P,
              -finalState.stateConditions.P_density)
        return objs
    
##############################################################################
############################ Define DataHandler ##############################
##############################################################################

class ExampleDataHandler(me.DataHandler):
    def __init__(self):
        pass
    def save(self,design,fullResults,objs):
        finalResults=fullResults[-1]
        finalState=finalResults[0][0]
        print('---------------------------')
        print('State Conditions')
        for key in finalState.stateConditions.__dict__.keys():
            print(key+' : '+str(getattr(finalState.stateConditions,key)))
        print('Machine Parameters')
        for key in finalState.design.machine.__dict__.keys():
            print(key+' : '+str(getattr(finalState.design.machine,key)))
    
    
    
if __name__ == '__main__':
    
    """Intiaiate objects needed for optimization"""
    #Designer
    arch=ExampleArchitect()
    des=ExampleDesigner(arch)
    #Evaluator
    evalSteps=[me.AnalysisStep(MagneticLoadingProblemDefinition(),
                               MagneticLoadingAnalyzer(),
                               MagneticLoadingPostAnalyzer()),
               me.AnalysisStep(OmegaProblemDefinition(),
                               OmegaAnalyzer(),
                               OmegaPostAnalyzer()),
               me.AnalysisStep(LengthProblemDefinition(),
                               LengthAnalyzer(),
                               LengthPostAnalyzer()),
               me.AnalysisStep(TorqueProblemDefinition(),
                               TorqueAnalyzer(),
                               TorquePostAnalyzer()),
               me.AnalysisStep(PowerProblemDefinition(),
                               PowerAnalyzer(),
                               PowerPostAnalyzer()),
               me.AnalysisStep(LossProblemDefinition(),
                               LossAnalyzer(),
                               LossPostAnalyzer()),
               me.AnalysisStep(EfficiencyProblemDefinition(),
                               EfficiencyAnalyzer(),
                               EfficiencyPostAnalyzer()),
               me.AnalysisStep(PowerDensityProblemDefinition(),
                               PowerDensityAnalyzer(),
                               PowerDensityPostAnalyzer())]
    evaluator=me.Evaluator(evalSteps)
    #Objectives
    objectives=ExampleObjective()
    #Data Handler
    dh=ExampleDataHandler()
    #Free variable bounds
    bounds=([.02,.009,.001,.01],[.5,.015,.01,.4])
    #Number of objectives
    n_obj=2
    """Create the MachineDesignProblem Object"""
    machDesProb=me.MachineDesignProblem(des,evaluator,objectives,dh,
                                        bounds,n_obj)
    """Create the optimizaiton object (This just hides pygmo code)"""
    opt=me.MachineOptimization(machDesProb)
    """Run the optimization"""
    pop_size=500
    gen_size=10
    pop=opt.run_optimization(pop_size,gen_size)
    """Plotting Parerto fronts"""
    fits, vectors = pop.get_f(), pop.get_x()
    ndf, dl, dc, ndr = pg.fast_non_dominated_sorting(fits) 
    fig2=plt.figure()   
    plot2=plt.axes()
    fig2.add_axes(plot2)
    plot2.plot(fits[ndf[0],0],fits[ndf[0],1],'x')
    plot2.set_xlabel('Power')
    plot2.set_ylabel('Power Density')
    plot2.set_title('Pareto Front')
