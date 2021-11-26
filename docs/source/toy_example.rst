.. _toy_example:

Analytical Machine Design Example
#################################

This is example is constructed to demonstrate how the ``mach_eval`` module can be used to evaluate multiple criteria of a complicated design problem. To simplify the coding required in this example, analytical scripts are used to evaluate the performance of a representative electrical machine. These scripts are used to create a non-convex optimization problem for the framework to solve and are not representative of actual physics.

The following objectives are assumed for this optimization:

* Maximize efficiency
* Minimize cost
* Minimize torque ripple

Designer
********

The ``Designer`` class of the ``des_opt`` module is extended in the ``mach_eval`` module to the concrete ``MachineDesigner`` class which takes in an ``Architect`` and a ``SettingsHandler``. The ``MachineDesigner`` converts the free variables ``x`` into a ``Design`` object which is made up of both a ``Machine`` and a ``Settings`` object. The ``Machine`` object is representative of a physical machine, while the ``Settings`` object includes information about the operating point and nameplate conditions of the machine.

Architect
=========

The ``Architect`` is a class which is designed to convert free variables ``x`` into a ``Machine`` object. The relevent code for the ``Architect`` used in this example is shown here:

.. code-block:: python

	class Architect(me.Architect):
		"""Converts input tuple x into a machine object"""   
		def __init__(self,mat:'Material'):
			self.mat=mat
		def create_new_design(self,x:tuple)->"me.Machine":
			"""
			converts x tuple into a machine object.

			Args:
				x (tuple): Input free variables.
				
			Returns:
				machine (me.Machine): Machine object
			"""
			r=x[3]
			delta=x[2]
			machine=Machine(r,delta,self.mat)
			return machine

The ``Machine`` and ``Material`` classes used in this example is defined as follows:

.. code-block:: python
	
	class Material:
		"""Material object for holding material properites"""
		def __init__(self,rho,C_e,C_hy,C_omega):
			self.rho=rho
			self.C_e=C_e
			self.C_hy=C_hy
			self.C_omega=C_omega
        
	class Machine:
		"""Class defines a Machine object 
		
		Attributes:
			TODO
		"""
		
		def __init__(self,r,delta,mat):
			"""Creates a machine object.

			Args:
				TODO

			"""
			
			self.r=r
			self.delta=delta
			self.mat=mat
			self.L=NotImplementedError
			
		@property
		def V_r(self):
			return np.pi*self.r**2*self.L
			
		@property
		def V_s(self):
			return np.pi*((1.5*self.r**2)-self.r**2)*self.L
		
		def newMachineFromNewLength(self,L)->'Machine':
			newMachine=deepcopy(self)
			newMachine.L=L
			return newMachine
			
SettingsHandler
===============

The ``SettingsHandler`` class converts free variables ``x`` into a ``Settings`` object. The following code demonstrates how this class is implemented in this example.

.. code-block:: python

	class SettingsHandler(me.SettingsHandler):
		def __init__(self,P_rated):
			self.P_rated=P_rated
		def get_settings(self,x):
			B_hat=x[0]
			A_hat=x[1]
			Omega=x[4]
			settings=Settings(B_hat,A_hat,Omega,self.P_rated)
			return settings

	class Settings:
		def __init__(self,B_hat,A_hat,Omega,P_rated):
			self.B_hat=B_hat
			self.A_hat=A_hat
			self.Omega=Omega
			self.P_rated=P_rated
			
		@property
		def f(self):
			return self.Omega/(2*np.pi)
		
		@property
		def T(self):
			return self.P_rated/self.Omega
			
Evaluator
*********

The ``Evaluator`` class of the ``des_opt`` module is extended in the ``mach_eval`` module to the ``MachineEvaluator`` class. This class takes in a list of ``EvaluationStep`` objects which are iterated through to perform the analysis. The following ``EvaluationSteps`` are performed in this evaluation:

* Tip Speed Constraint
* Length Scaling
* Length to Radius Constraint
* Loss Calculations
* Cost Calculations
* Torque Ripple Calculations

Two types of ``EvaluationStep`` objects are used in this example, the first are standard ``EvaluationStep`` which implement the required ``step`` functionality to check a constraint. An example of this type of evaluation is shown in the tip speed constraint.


.. code-block:: python

	class TipSpeedConstraintEvaluationStep(me.EvaluationStep):
		"""Constraint evaluation step template"""
		def __init__(self,maxTipSpeed):
			self.maxTipSpeed=maxTipSpeed
		def step(self,stateIn):
			"""Checks input state to see if constraint is violated
			
			Raises ConstraintError if violated, otherwise appends values to 
			State conditions and moves forward"""
			r=stateIn.design.machine.r
			omega=stateIn.design.settings.Omega
			v_tip = r*omega 
			if v_tip >=self.maxTipSpeed:
				raise do.InvalidDesign([v_tip,'Tip Speed Violation'])
			else:
				stateOut=deepcopy(stateIn)
				stateOut.conditions.v_tip=v_tip
				return [v_tip,stateOut]
				
In this example the machine radius is extracted from the input state in ``r=stateIn.design.machine.r``. The operating speed is extracted from the input state in the same manner in ``omega=stateIn.design.settings.Omega``. The rotational speed of the machine and the radius are used to calculate the circumferential tip speed of the rotor. If the tip speed is found to exceed a maximum tip speed provided on initialization of the evaluation step, then a ``InvalidDesign`` exception is raised. This exception will exit the evaluation process back to the try\except block in the ``fitness` function of the ``DesignProblem`` as shown in the following code. This exception will cause the optimization to set the objective values to a large number for the design, effectively acting as a death penalty constraint.

.. code-block:: python

	    except Exception as e:
            if type(e) is InvalidDesign:
                temp = tuple(map(tuple, 1E4 * np.ones([1, self.get_nobj()])))
                objs = temp[0]
                return objs

The second type of ``EvaluationStep`` used in this example is the ``AnalysisStep`` of the ``mach_eval`` module. The ``AnalysisStep`` class is an extension of the ``EvaluationStep`` which codifies how the information should be handled during evaluation. Three protocols must be passed into the ``AnalysisStep`` upon initialization:

ProblemDefinition
	Converts the input ``state`` into a ``problem`` class which can be utilized by the ``Analyzer``
Analyzer
	Performs an analysis on an problem. These are designed to handle specific analysis of complex machine design problems.
PostAnalyzer
	Packages the results of the analysis and the initial state back into the the return state
	
.. figure:: /images/getting_started/AnalysisStepExample.png
   :alt: Trial1 
   :align: center
   :width: 800 
   
The following code demonstrates how these three protocols are implemented to evaluate the machine length required to produce the desired torque. The first protocol, the ``ProblemDefinition`` is implemented as shown. This class is designed to convert the input state revived by the ``AnalysisStep`` into a ``Problem`` class which holds in the information required by the analyzer in the correct format.

.. code-block:: python

	class LengthProblemDefinition(me.ProblemDefinition):
		"""Class converts input state into a problem"""
		
		def get_problem(self,state:'me.State')->'me.Problem':
			"""Returns Problem from Input State"""
			T=state.design.settings.T
			B_hat=state.design.settings.B_hat
			A_hat=state.design.settings.A_hat
			r=state.design.machine.r
			problem=LengthProblem(T,B_hat,A_hat,r)
			return problem

	class LengthProblem():
		"""problem class utilized by the Analyzer
		
		Attributes:
			T : required torque of machine
			B_hat : Magnetic loading
			A_hat : Electric loading
			r : Rotor radius
		"""
		def __init__(self,T,B_hat,A_hat,r):
			"""Creates problem class
			
			Args:
				TODO
				
			"""
			#TODO define problem 
			self.T=T
			self.B_hat=B_hat
			self.A_hat=A_hat
			self.r=r


The ``Problem`` class is then passed into the ``analyze`` function of the ``Analyzer`` class. In this class the relevant evaluation calculations are performed and the results are returned.

.. code-block:: python
		
	class LengthAnalyzer(me.Analyzer):
		""""Calculates the required machine length to produce desired torque"""
		
		def analyze(self,problem:'me.Problem'):
			"""Performs Analysis on a problem

			Args:
				problem (me.Problem): Problem Object

			Returns:
				results (Any): 
					Results of Analysis

			"""
			#TODO Define Analyzer
			T=problem.T
			B_hat=problem.B_hat
			A_hat=problem.A_hat
			r=problem.r
			L=T/(B_hat*A_hat*np.pi*r**2)
			return L
		
Finally in the ``PostAnalyzer``, the results from the ``Analyzer`` are packaged back into the ``state`` object and any relevant changes to the ``state`` object are made. The new state now has the information from this analysis stored, and is ready for the next ``EvaluationStep``.

.. code-block:: python
		

	class LengthPostAnalyzer(me.PostAnalyzer):
		"""Converts input state into output state for TemplateAnalyzer"""
		def get_next_state(self,results:Any,stateIn:'me.State')->'me.State':
			stateOut=deepcopy(stateIn)
			newMachine=stateOut.design.machine.newMachineFromNewLength(results)
			stateOut.design.machine=newMachine
			#TODO define Post-Analyzer
			return stateOut
			


DesignSpace
***********

A ``DesignSpace`` object is defined for the optimization as well. This object is used to handle the calculations of objectives from the evaluation results, as well as manage the constraints, number of objectives, and bounds for the optimization. 

.. code-block:: python

	class DesignSpace:
    """Design space of optimization"""
    
    def __init__(self,n_obj,bounds):
        self._n_obj=n_obj
        self._bounds=bounds
    
    def check_constraints(self, full_results) -> bool:
        return True
    @property
    def n_obj(self) -> int:
        return self._n_obj

    def get_objectives(self, valid_constraints, full_results) -> tuple:
        """ Calculates objectives from evaluation results
        

        Args:
            full_results (List): Results from MachineEvaluator

        Returns:
            Tuple: objectives tuple 
        """
        final_state=full_results[-1][-1]
        P_loss=final_state.conditions.P_loss
        C=final_state.conditions.C
        T_r=final_state.conditions.T_r
        P_rated=final_state.design.settings.P_rated
        
        Eff=(P_rated-P_loss)/P_rated
        results=(-Eff,C,T_r) #TODO define objectives
        return results
    @property
    def bounds(self) -> tuple:
        return self._bounds

    

DesignProblem
*************

The ``MachineDesigner``, ``MachineEvaluator``, and ``DesignSpace`` described above along with a ``DataHandler`` object are used to initialize a ``DesignProblem`` class from the ``des_opt`` module. First the ``MachineDesigner`` is created from the ``SettingsHandler`` and ``Architect``.

.. code-block:: python

	#Create Designer
    settingsHandler=SettingsHandler(100E3) #TODO define settings
    material=Material(7850,6.88E-5,.0186,.002)
    arch=Architect(material)
    des=me.MachineDesigner(arch,settingsHandler)

The ``EvaluationSteps`` are initialized inside of an ordered list. This list is then passed to the ``MachineEvaluator`` for initialization, the ``MachineEvaluator`` will iterate through the evaluation steps in the order of the passed list. 

.. code-block:: python

    #Create evaluation steps
    v_tip_max=150
    maxL2r=10
    evalSteps=[TipSpeedConstraintEvaluationStep(v_tip_max),
               me.AnalysisStep(LengthProblemDefinition(),
                               LengthAnalyzer(),
                               LengthPostAnalyzer()),
               L2rConstraintEvaluationStep(maxL2r),
               me.AnalysisStep(LossProblemDefinition(),
                               LossAnalyzer(),
                               LossPostAnalyzer()),
               me.AnalysisStep(CostProblemDefinition(),
                               CostAnalyzer(),
                               CostPostAnalyzer()),
               me.AnalysisStep(TorqueRippleProblemDefinition(),
                               TorqueRippleAnalyzer(),
                               TorqueRipplePostAnalyzer())]
    
    #Create Evaluator
    evaluator=me.MachineEvaluator(evalSteps)
	
A ``DataHandler`` object is not implement for this example, but a dummy object with empty function calls is still provided. The ``DesignSpace`` is provided the number of objectives and the free variable bounds on initialization as shown.

.. code-block:: python
	
    dh=DataHandler()
    
    #set evaluation bounds
    bounds=([.1,10E3,.1E-3,10E-3,1000*2*np.pi/60],
            [1,100E3,10E-3,95.5E-3,15000*2*np.pi/60])

    #set number of objectives
    n_obj=3

Finally the ``MachineDesigner``, MachineEvaluator``, ``DesignSpace``, and ``DataHandler`` objects are passed to the ``DesignProblem``for initialization. The ``DesignProblem`` is now ready for optimization.

.. code-block:: python

    #Create Machine Design Problem
    ds=DesignSpace(n_obj, bounds)
    machDesProb=do.DesignProblem(des,evaluator,ds,dh)
	