.. _structural_analyzer:

SPM Rotor Structural Analyzer
##############################


This page describes how the structural performance of a surface-mounted permanent magnet (SPM) rotor is evaluated using the eMach code base. The structural analyzer implemented is a combination of two analyzers. A base structural analyzer calculates the stress induced in the rotor, and a rotor sleeve analyzer calculates the optimum design of a carbon fiber sleeve. A detailed description of the math and physics for this problem can be found in the `this paper <https://ieeexplore.ieee.org/document/9595523>`_.

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
   
Inputs for SPM Structural Analyzers
******************************************
The current implementation of the structural analyzer requires a material dictionary (``mat_dict``), temperature coefficient, and dimensions of the shaft, rotor core, magnet, and sleeve. The following table shows the list of required inputs for the structural analyzer.

.. csv-table:: Inputs for structural analyzer -- ``mat_dict``
   :file: inputs_mat_dict.csv
   :widths: 70, 70, 30
   :header-rows: 1

.. csv-table:: Inputs for structural analyzer -- Dimensions
   :file: inputs_dimensions.csv
   :widths: 70, 70, 30
   :header-rows: 1

.. csv-table:: Inputs for structural analyzer -- ``stress_limits``
   :file: inputs_sleeve_stress.csv
   :widths: 70, 70, 30
   :header-rows: 1


Base Structural Analyzer
************************
    
The base structural analyzer uses the ``SPM_RotorStructuralProblem`` to calculate the stress distribution in the rotor components. The base analyzer ``SPM_RotorStructuralAnalyzer`` takes in a ``SPM_RotorStructuralProblem`` in its ``analyze`` method and returns a list of ``Sigma`` objects, one for each of the rotor components. The ``Sigma`` objects are used to calculate the radial and tangential stress at a radial position ``r`` in the component via their methods ``sigma.radial(r)`` and ``sigma.tangential(r)`` respectively. The core functionality of the base analyzer is demonstrated in the following code block:

.. code-block:: python

    import numpy as np
    from matplotlib import pyplot as plt
    from eMach.mach_eval.analyzers import spm_rotor_structrual_analyzer as sta
    ######################################################
    # Creating the required Material Dictionary 
    ######################################################
    mat_dict = {
        'core_material_density': 7650,  # kg/m3
        'core_youngs_modulus': 185E9,  # Pa
        'core_poission_ratio': .3,
        'alpha_rc' : 1.2E-5,

        'magnet_material_density'    : 7450, # kg/m3
        'magnet_youngs_modulus'      : 160E9, # Pa
        'magnet_poission_ratio'      :.24,
        'alpha_pm'                   :5E-6,

        'sleeve_material_density'    : 1800, # kg/m3
        'sleeve_youngs_th_direction' : 125E9,  #Pa
        'sleeve_youngs_p_direction'  : 8.8E9,  #Pa
        'sleeve_poission_ratio_p'    :.015,
        'sleeve_poission_ratio_tp'   :.28,
        'alpha_sl_t'                :-4.7E-7,
        'alpha_sl_r'                :0.3E-6,

        'sleeve_max_tan_stress': 1950E6,  # Pa
        'sleeve_max_rad_stress': -100E6,  # Pa

        'shaft_material_density': 7870,  # kg/m3
        'shaft_youngs_modulus': 206E9,  # Pa
        'shaft_poission_ratio': .3,  # []
        'alpha_sh' : 1.2E-5
    }
    ######################################################
    #Setting the machine geometry and operating conditions
    ######################################################
    r_sh = 5E-3 # [m]
    d_m = 2E-3 # [m]
    r_ro = 12.5E-3 # [m]
    deltaT = 0 # [K]
    N = 100E3 # [RPM]
    d_sl=1E-3 # [m]
    delta_sl=-2.4E-5 # [m]

    ######################################################
    #Creating problem and analyzer class
    ######################################################
    problem = sta.SPM_RotorStructuralProblem(r_sh, d_m, r_ro, d_sl, delta_sl, deltaT, N,mat_dict)
    analyzer=sta.SPM_RotorStructuralAnalyzer()
    ######################################################
    #Analyzing Problem
    ######################################################
    sigmas=analyzer.analyze(problem)
    
    ######################################################
    #Creating vectors of radius used for plotting
    ######################################################
    r_vect_sh=np.linspace(r_sh/10000,r_sh,100)
    r_vect_rc=np.linspace(r_sh,r_ro-d_m,100)
    r_vect_pm=np.linspace(r_ro-d_m,r_ro,100)
    r_vect_sl=np.linspace(r_ro,r_ro+d_sl,100)
    
    ######################################################
    #Plotting Stress distribution in rotor
    ######################################################
    fig,ax=plt.subplots(2,1)
    ax[0].plot(r_vect_sh,sigmas[0].radial(r_vect_sh))
    ax[0].plot(r_vect_rc,sigmas[1].radial(r_vect_rc))
    ax[0].plot(r_vect_pm,sigmas[2].radial(r_vect_pm))
    ax[0].plot(r_vect_sl,sigmas[3].radial(r_vect_sl))
    ax[0].set_xticks([])
    ax[0].set_ylabel('Radial Stress [Pa]')
    ax[1].plot(r_vect_sh,sigmas[0].tangential(r_vect_sh))
    ax[1].plot(r_vect_rc,sigmas[1].tangential(r_vect_rc))
    ax[1].plot(r_vect_pm,sigmas[2].tangential(r_vect_pm))
    ax[1].plot(r_vect_sl,sigmas[3].tangential(r_vect_sl))
    ax[1].set_ylabel('Tangential Stress [Pa]')
    ax[1].set_xlabel('Radial Position [m]')
        
        
        
Running the code above should produce the follow plot of radial and tangential stress in the example rotor.

.. figure:: ./images/Structural/ExampleStress.svg
   :alt: Trial1 
   :align: center
   :width: 600 


Sleeve Analyzer
***************

The rotor sleeve analyzer ``SleeveAnalyzer`` is used to design an optimal sleeve which produces the maximum amount of compressive force while being as thin as possible. The ``SleeveAnalyzer`` is designed to use the base structural analyzer, however other analyzers which are able to calculate the four required stresses (`See Table VI <https://ieeexplore.ieee.org/document/9595523>`_) could be used as well. The following code snipit demonstrates how to initialize the problem and analyzer to calculate the optimal sleeve geometry. 

.. code-block:: python

    from eMach.mach_eval.analyzers import spm_rotor_structrual_analyzer as sta
    
    ######################################################
    # Creating the required Material Dictionary 
    ######################################################
    mat_dict = {
        'core_material_density': 7650,  # kg/m3
        'core_youngs_modulus': 185E9,  # Pa
        'core_poission_ratio': .3,
        'alpha_rc' : 1.2E-5,

        'magnet_material_density'    : 7450, # kg/m3
        'magnet_youngs_modulus'      : 160E9, # Pa
        'magnet_poission_ratio'      :.24,
        'alpha_pm'                   :5E-6,

        'sleeve_material_density'    : 1800, # kg/m3
        'sleeve_youngs_th_direction' : 125E9,  #Pa
        'sleeve_youngs_p_direction'  : 8.8E9,  #Pa
        'sleeve_poission_ratio_p'    :.015,
        'sleeve_poission_ratio_tp'   :.28,
        'alpha_sl_t'                :-4.7E-7,
        'alpha_sl_r'                :0.3E-6,

        'sleeve_max_tan_stress': 1950E6,  # Pa
        'sleeve_max_rad_stress': -100E6,  # Pa

        'shaft_material_density': 7870,  # kg/m3
        'shaft_youngs_modulus': 206E9,  # Pa
        'shaft_poission_ratio': .3,  # []
        'alpha_sh' : 1.2E-5
    }
    ######################################################
    #Setting the machine geometry and operating conditions
    ######################################################
    r_sh = 5E-3 # [m]
    d_m = 2E-3 # [m]
    r_ro = 12.5E-3 # [m]
    deltaT = 0 # [K]
    N = 100E3 # [RPM]
    ######################################################
    #Defining required stress limits
    ######################################################
    stress_limits = {'rad_sleeve': -100E6,
                     'tan_sleeve': 1300E6,
                     'rad_magnets': 0,
                     'tan_magnets': 80E6}
                     

    ######################################################
    #Create problem and analyzer
    ######################################################
    problem = sta.SleeveProblem(r_sh, d_m, r_ro, deltaT, mat_dict, N)
    ana = sta.SleeveAnalyzer(stress_limits)
    ######################################################
    #Calculate optimal sleeve geometry
    ######################################################
    sleeve_dim = ana.analyze(problem)
    print(sleeve_dim)

The above code will output the following results to the command line. Line of the output shows the analyzer found a optimal sleeve thickness of 1.649E-4 [m] and optimal undersize of -1.211E-4 [m].

.. code-block::

    True
         fun: 0.00016490326908354797
         jac: array([1., 0.])
     message: 'Optimization terminated successfully'
        nfev: 26
         nit: 6
        njev: 5
      status: 0
     success: True
           x: array([ 0.0001649, -0.0001211])
    [ 0.0001649 -0.0001211]
