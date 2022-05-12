.. _structural_analyzer:

Structural Analyzer
###################


This page describes how the structural performance of a surface-mounted permanent magnet (SPM) rotor is evaluated using the eMach code base. The structural analyzer implemented is a combination of two analyzers. A base structural analyzer calculates the stress induced in the rotor, and a rotor sleeve analyzer calculates the optimum design of a carbon fiber sleeve. A detailed description of the math and physics for this problem can be found in the `this paper <https://ieeexplore.ieee.org/document/9595523>`_.

..
    The structural analyzer implemented is a combination of two analyzers. A base structural analyzer calculates the stress induced in the rotor, and a rotor sleeve analyzer calculates the optimum design of a carbon fiber sleeve.


    This code implements the ``AnalysisStep`` protocols (ProblemDefinition, Analyzer, PostAnalyzer).

    In addition to the base structural analyzer which calculates the induced stresses in the rotor. A second analyzer which optimizes the design of a carbon fiber rotor sleeve is presented. This second analyzer uses the base structural analyzer to calculate the minimum sleeve thickness which retain the rotor magnets during operation.

Model Background
****************

The SPM rotor can be modeled as a series of concentric cylinders as shown in the figure below. In this case the rotor is assumed to have four regions of varying material: a shaft, rotor back iron, magnets, and a sleeve. The sleeve is designed with an undersized fit in order to provide the compressive force on the rotor.

.. figure:: ./images/Structural/RotorConfig.svg
   :alt: Trial1 
   :align: center
   :width: 600 

.. figure:: ./images/Structural/SleeveOrientation.svg
   :alt: Trial1 
   :align: center
   :width: 600 

Base Structural Analyzer
************************
The base structural analyzer is used to calculate the rotor radial and tangential stress. The base structural analyzer takes in the ``StructuralProblem`` containing ``RotorComponent`` as an input and returns a list of stress values as ``Sigma`` objects for each rotor component. In the current implementation, the base structural analyzer is not called by the user but by the ``SleeveAnalyzer``; therefore does not follow the standard ``get_problem`` function signature of receiving a ``state`` object.
The user is recommended to checkout the ``StructuralProblem,`` and its problem definition ``StructuralProblemDef`` in ``structural_analyzer.py``.

Sleeve Analyzer
***************
The rotor sleeve analyzer described here is used to design an optimal rotor sleeve which minimizes the required sleeve thickness in order to reduce cost, windage loss, and thermal issues. The sleeve analyzer expects a ``SleeveProblem`` in its analyze function signature. The ``SleeveProblemDef`` extracts the relevant information from the input state object to create the required problem object. Unlike the base structural analyzer, the sleeve analyzer is directly called by the ``MachineEvaluator`` object during evaluation. The implementation of ``SleeveProblem`` and ``SleeveProblemDef`` can be found in ``structural_analyzer.py``.


How to use the structural analyzer
**********************************
To use the eMach structural analyzer, the user must import the ``structural_analyzer`` module and call the ``SleeveAnalyzer`` class. The ``SleeveAnalyzer`` class needs a dictionary containing radial and tangential stress limits for the sleeve and magnet as an input. An example of using the structural analyzer is shown in the following snippet.

.. code-block:: python

    from analyzers import structrual_analyzer as sta
    stress_limits = {'rad_sleeve': -100E6,
                 'tan_sleeve': 1300E6,
                 'rad_magnets': 0,
                 'tan_magnets': 80E6} # TODO : ADD Units and show how to create an example plot from paper
    struct_ana = sta.SleeveAnalyzer(stress_limits)


..
    Base Structural Analyzer
    ************************

    The code for calculating rotor stresses using the base structural analyzer is discussed here.

    ProblemDefinition
    =================

    The structural analyzer expects a ``StructuralProblem`` of the following form. ``RotorComponent`` objects contain all the relevant material and geometric properties for the four rotor sections.

    .. code-block:: python

        class StructuralProblem:
            """Problem class for StructuralAnalyzer.

            Attributes:
                sh (RotorComponent): Shaft RotorComponent object.
                rc (RotorComponent): Rotor core RotorComponent object.
                pm (RotorComponent): Magnets RotorComponent object.
                sl (RotorComponent): Sleeve RotorComponent object.
                deltaT (float): Temperature rise in deg C.
                omega (float): rotational speed in rad/s.

            """
            def __init__(self, sh, rc, pm, sl, deltaT, omega):
                """StructuralProblem __init__ method.

                Args:
                    sh (RotorComponent): Shaft RotorComponent object.
                    rc (RotorComponent): Rotor core RotorComponent object.
                    pm (RotorComponent): Magnets RotorComponent object.
                    sl (RotorComponent): Sleeve RotorComponent object.
                    deltaT (float): Temperature rise in deg C.
                    omega (float): rotational speed in rad/s.

                """
                self.sh=sh
                self.rc=rc
                self.pm=pm
                self.sl=sl
                self.deltaT=deltaT
                self.omega=omega


    A ``ProblemDefinition`` is written here to convert input values to the required problem definition form. A dictionary object is passed into this class on initialization which contains the relevant material properties. Note that this class does not follow the standard ``get_problem`` function signature of receiving a ``state`` object. The reason for this change is that this analyzer is not being directly utilized as an ``AnalysisStep``, instead it is being called by the sleeve analyzer step described later in this document.

    .. code-block:: python

        class StructuralProblemDef:
            """ProblemDefinition class for StructuralAnalyzer.

            Attributes:
                mat_dict (dict): material parameters dictionary.

            """
            def __init__(self,mat_dict: dict)->'StructuralProblemDef':
                """StructuralProblemDef __init__ method.

                Args:
                    mat_dict (dict): material parameters dictionary.

                """
                self.mat_dict=mat_dict

            def get_problem(self,r_sh: float,d_m: float,r_ro: float,d_sl : float,
                           delta_sl: float, deltaT: float,N: float)->'StructuralProblem':
                """Creates StructuralProblem object from input

                Args:
                    r_sh (float): Shaft outer radius.
                    d_m (float): Shaft outer radius.
                    r_ro (float): Shaft outer radius.
                    d_sl (float): Shaft outer radius.
                    delta_sl (float): Shaft outer radius.
                    deltaT (float): Shaft outer radius.
                    N (float): Shaft outer radius.

                Returns:
                    problem (StructuralProblem): StructuralProblem

                """
                R1=r_sh
                R2=r_ro-d_m
                R3=r_ro
                R4=r_ro+d_sl
                # print('R1:',R1,'R2:',R2,'R3:',R3)
                ##############################
                #    Load Operating Point
                ##############################
                omega=N*2*np.pi/60
                ##############################
                #   Load Material Properties
                ##############################
                rho_sh=self.mat_dict['shaft_material_density']
                E_sh=self.mat_dict['shaft_youngs_modulus']
                nu_sh=self.mat_dict['shaft_poission_ratio']
                alpha_sh=self.mat_dict['alpha_sh']#1.2E-5

                rho_rc=self.mat_dict['core_material_density']
                E_rc=self.mat_dict['core_youngs_modulus']
                nu_rc=self.mat_dict['core_poission_ratio']
                alpha_rc=self.mat_dict['alpha_rc']#1.2E-5

                rho_pm=self.mat_dict['magnet_material_density']
                E_pm=self.mat_dict['magnet_youngs_modulus']
                nu_pm=self.mat_dict['magnet_poission_ratio']
                alpha_pm=self.mat_dict['alpha_pm']#5E-6

                rho_sl=self.mat_dict['sleeve_material_density']
                E_t_sl=self.mat_dict['sleeve_youngs_th_direction']
                E_p_sl=self.mat_dict['sleeve_youngs_p_direction']
                nu_p_sl=self.mat_dict['sleeve_poission_ratio_p']
                nu_tp_sl=self.mat_dict['sleeve_poission_ratio_tp']
                alpha_t=self.mat_dict['alpha_sl_t']#-4.7E-7
                alpha_r=self.mat_dict['alpha_sl_r']#.3E-6
                MaxRadialSleeveStress=self.mat_dict['sleeve_max_rad_stress']
                MaxTanSleeveStress=self.mat_dict['sleeve_max_tan_stress']
                ##############################
                #   Make Rotor Materials
                ##############################
                ShaftMaterial=Material_Isotropic(rho_sh,E_sh,nu_sh,alpha_sh)
                RotorCoreMaterial=Material_Isotropic(rho_rc,E_rc,nu_rc,alpha_rc)
                MagnetMaterial=Material_Isotropic(rho_pm,E_pm,nu_pm,alpha_pm)
                SleeveMaterial=Material_Transverse_Isotropic(rho_sl,E_t_sl,E_p_sl,nu_tp_sl,
                                                             nu_p_sl,alpha_r,alpha_t)
                sh=RotorComponent(ShaftMaterial,0,R1)
                rc=RotorComponent(RotorCoreMaterial,R1,R2)
                pm=RotorComponent(MagnetMaterial,R2,R3)
                pm.set_MaxRadialStress(0)
                sl=RotorComponent(SleeveMaterial,R3,R4)
                sl.set_MaxRadialStress(MaxRadialSleeveStress)
                sl.set_MaxTanStress(MaxTanSleeveStress)
                sl.set_th(d_sl)
                sl.set_delta_sl(delta_sl)

                problem=StructuralProblem(sh,rc,pm,sl,deltaT,omega)
                return problem

    Analyzer
    ========

    The following code snip shows the ``analyze`` function for the base structural analyzer. As noted earlier, the details of the performed calculations are not provided in this document. The analyzer returns a list of ``Sigma`` objects for each rotor component, these objects contain functions for calculating the radial and tangential stress at any point in the component.

    .. code-block:: python

        class StructuralAnalyzer:

            def analyze(self,problem: 'StructuralProblem')->['Sigma','Sigma','Sigma','Sigma']:
                """Analyze structural problem

                Args:
                    problem (StructuralProblem): problem for analyzer.

                Returns:
                    results (['Sigma','Sigma','Sigma','Sigma']): Sigma objects

                """
                sh=problem.sh
                rc=problem.rc
                pm=problem.pm
                sl=problem.sl
                deltaT=problem.deltaT
                omega=problem.omega

                A=self.DetermineCoeff(sh,rc,pm,sl,deltaT,omega)
                sigma_sh=Sigma(sh,[A[0],0],omega,deltaT)
                sigma_rc=Sigma(rc,[A[1],A[2]],omega,deltaT)
                sigma_pm=Sigma(pm,[A[3],A[4]],omega,deltaT)
                sigma_sl=Sigma(sl,[A[5],A[6]],omega,deltaT)

                return [sigma_sh,sigma_rc,sigma_pm,sigma_sl]


    Rotor Sleeve Analyzer
    *********************

    The rotor sleeve analyzer described here is used to design an optimal rotor sleeve which minimizes the required sleeve thickness in order to reduce cost, windage loss, and thermal issues. This analyzer set is presented as ``AnalysisStep`` classes, and is directly called by the ``MachineEvaluator`` object during an optimization. The base structural analyzer is used here to calculate the stress distribution, however this can be substituted for a different structural analyzer provided it has the same return values.

    Problem Definition
    ==================

    The sleeve analyzer expects a ``SleeveProblem`` in its ``analyze`` function signature. The ``SleeveProblemDef`` extracts the relevant information from the input ``state`` object to create the required ``problem`` object.

    The ``SleeveProblem`` has a set of four functions, each corresponding to one of the structural failure criteria of the rotor. Each of these functions calls the base structural analyzer to calculate the associated stress value.

    .. code-block:: python

        class SleeveProblem:
            def __init__(self, r_sh: float, d_m: float, r_ro: float,
                           deltaT: float, mat_dict: dict, N: float):
                """__init__ definition for SleeveProblem class

                Args:
                    r_sh (float): shaft radius.
                    d_m (float): Magnet thickness.
                    r_ro (float): Outer rotor radius.
                    deltaT (float): Temperature rise.
                    mat_dict (dict): Material Dictionary.
                    N (float): Rotational speed RPM.
                """

                self.r_sh=r_sh
                self.d_m=d_m
                self.r_ro=r_ro
                self.deltaT=deltaT
                self.mat_dict=mat_dict
                self.N = N

            def tan_sleeve(self,x):
                """Calculate sigma_t_sl_max for given sleeve design"""
                d_sl = x[0]
                delta_sl = x[1]
                R_ro=self.r_ro
                N=self.N
                r_sh=self.r_sh
                d_m=self.d_m
                deltaT=self.deltaT
                struc_prob_def=StructuralProblemDef(self.mat_dict)
                problem=struc_prob_def.get_problem(r_sh,d_m,R_ro,d_sl,delta_sl,deltaT,N)
                analyzer=StructuralAnalyzer()
                sigmas=analyzer.analyze(problem)
                x_sl=np.linspace(R_ro,R_ro+d_sl,50)
                sigma_t_sl=sigmas[3].tangential(x_sl)
                stress=sigma_t_sl[0]
                return stress

            def rad_sleeve(self,x):
                """Calculate P_sl for given sleeve design"""
                d_sl=x[0]
                delta_sl=x[1]
                R_ro=self.r_ro
                N=self.N
                r_sh=self.r_sh
                d_m=self.d_m
                deltaT=self.deltaT
                struc_prob_def=StructuralProblemDef(self.mat_dict)
                problem=struc_prob_def.get_problem(r_sh,d_m,R_ro,d_sl,delta_sl,deltaT,N)
                analyzer=StructuralAnalyzer()
                sigmas=analyzer.analyze(problem)
                x_sl=np.linspace(R_ro,R_ro+d_sl,50)
                sigma_r_sl=sigmas[3].radial(x_sl)
                stress=sigma_r_sl[0]
                return stress
            def rad_magnet(self,x):
                """Calculate P_pm for given sleeve design"""
                d_sl=x[0]
                delta_sl=x[1]
                R_ro=self.r_ro
                N=self.N
                r_sh=self.r_sh
                d_m=self.d_m
                deltaT=self.deltaT
                struc_prob_def=StructuralProblemDef(self.mat_dict)
                problem=struc_prob_def.get_problem(r_sh,d_m,R_ro,d_sl,delta_sl,deltaT,N)
                analyzer=StructuralAnalyzer()
                sigmas=analyzer.analyze(problem)
                x_pm=np.linspace(R_ro-d_m,R_ro,50)
                sigma_r_pm=sigmas[2].radial(x_pm)
                stress=sigma_r_pm[0]
                return stress

            def tan_magnet(self, x):
                """Calculate sigma_t_pm_max for given sleeve design"""
                d_sl = x[0]
                delta_sl = x[1]
                R_ro = self.r_ro
                N = self.N
                r_sh = self.r_sh
                d_m = self.d_m
                deltaT = self.deltaT
                struc_prob_def = StructuralProblemDef(self.mat_dict)
                problem = struc_prob_def.get_problem(r_sh, d_m, R_ro, d_sl, delta_sl, deltaT, N)
                analyzer = StructuralAnalyzer()
                sigmas = analyzer.analyze(problem)
                x_pm = np.linspace(R_ro-d_m, R_ro, 50)
                sigma_t_pm = sigmas[2].tangential(x_pm)
                stress = sigma_t_pm[0]
                return stress

            def cost(self, x):
                return x[0]


        class SleeveProblemDef:
            def get_problem(state) -> 'StructuralProblem':
                design = state.design
                material_dict = {}
                for key, value in design.machine.rotor_iron_mat.items():
                    material_dict[key] = value
                for key, value in design.machine.magnet_mat.items():
                    material_dict[key] = value
                for key, value in design.machine.rotor_sleeve_mat.items():
                    material_dict[key] = value
                for key, value in design.machine.shaft_mat.items():
                    material_dict[key] = value

                material_dict['alpha_sh'] = 1.2E-5
                material_dict['alpha_rc'] = 1.2E-5
                material_dict['alpha_pm'] = 5E-6
                material_dict['alpha_sl_t'] = -4.7E-7
                material_dict['alpha_sl_r'] = 0.3E-6

                r_sh = design.machine.r_sh
                r_ro = design.machine.r_ro
                # print('rotor radius is ', r_ro)
                d_m = design.machine.d_m
                # print('magnet thickness is ', d_m)
                N = design.settings.speed
                deltaT = design.settings.rotor_temp_rise

                problem = SleeveProblem(r_sh, d_m, r_ro, deltaT, material_dict, N)
                return problem

    Analyzer
    ========

    The ``SleeveAnalyzer`` contains a single objective optimization problem to minimize the sleeve thickness subject to the nonlinear constraints of the four structural failure criteria. When a ``SleeveProblem`` is passed into the ``analyze`` function, the single objective optimization uses the stress functions defined in the problem object to calculate the constraints. If there exists an optimal sleeve geometry, these dimensions are returned as results of the analyzer, if no valid sleeve geometry is found, then the analyzer returns a ``False`` value.

    .. code-block:: python

        class SleeveAnalyzer:
            def __init__(self, stress_limits):
                self.stress_limits = stress_limits

            def analyze(self, problem: 'SleeveProblem'):
                nlc1 = op.NonlinearConstraint(problem.rad_sleeve,
                                              self.stress_limits['rad_sleeve'], 0)
                nlc2 = op.NonlinearConstraint(problem.tan_sleeve, -np.inf,
                                              self.stress_limits['tan_sleeve'])
                nlc3 = op.NonlinearConstraint(problem.rad_magnet, -np.inf,
                                              self.stress_limits['rad_magnets'])
                nlc4 = op.NonlinearConstraint(problem.tan_magnet, -np.inf,
                                              self.stress_limits['tan_magnets'])
                const = [nlc1, nlc2, nlc3, nlc4]
                sol = op.minimize(problem.cost, [1E-3, -1E-3], tol=1E-4, constraints=const, bounds=[[0, 1], [-.01, 0]])
                print(sol.success)
                print(sol)
                if sol.success:
                    return sol.x
                else:
                    return False

