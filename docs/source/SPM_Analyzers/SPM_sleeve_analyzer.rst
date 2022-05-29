
.. _sleeve_analyzer:

SPM Sleeve Analyzer
###################

The rotor sleeve analyzer ``SleeveAnalyzer`` is used to design an optimal sleeve which produces the maximum amount of compressive force while being as thin as possible. The ``SleeveAnalyzer`` is designed to use the :doc:`SPM Structural Analyzer <SPM_structural_analyzer>`, however other analyzers which are able to calculate the four required stresses (`See Table VI <https://ieeexplore.ieee.org/document/9595523>`_) could be used as well. 


Model Background
****************

The SPM rotor can be modeled as a series of concentric cylinders as shown in the figure below. In this case the rotor is assumed to have four regions of varying material: a shaft, rotor back iron, magnets, and a sleeve. The sleeve is designed with an undersized fit in order to provide the compressive force on the rotor. This analyzer is designed to calculate the optimal sleeve geometry based on `Section 4.A <https://ieeexplore.ieee.org/document/9595523>`_. 

.. figure:: ./images/RotorConfig.svg
   :alt: Trial1 
   :align: center
   :width: 300 

.. figure:: ./images/SleeveOrientation.svg
   :alt: Trial1 
   :align: center
   :width: 300 


Inputs for SPM Sleeve Analyzers
************************************

The ``SPM_sleeve_analyzer`` requires the following stresses to be defined on initialization of the analyzer through a ``dict`` object. These stress values represent the limits of the critical stresses (`See Table VI <https://ieeexplore.ieee.org/document/9595523>`_) need to design an optimal sleeve.

.. csv-table:: Inputs for structural analyzer -- ``stress_limits``
   :file: inputs_sleeve_stress.csv
   :widths: 70, 70, 30
   :header-rows: 1
   

The ``sleeve_analyzer`` is designed to minimize the sleeve thickness without violating the stress constraints. The analyzer requires the problem object to have a set of methods (``rad_magnet``, ``tan_magnet``, ``rad_sleeve``, ``tan_sleeve``) which take in a tuple of [``d_sl``, ``delta_sl``], representing the sleeve thickness and sleeve undersize, and return back the values for each of the critical stresses. In addition, the problem object is required to have a method ``cost`` which takes in the same tuple and returns back the sleeve thickness ``d_sl``.

The ``sleeve_problem`` by default utilizes the :doc:`SPM Structural Analyzer <SPM_structural_analyzer>`. However, other structural which utilize the same function signature may also be used. The problem class requires a material dictionary ``mat_dict`` to be implemented as well as a set of rotor geometry and operating conditions. The required properties for the problem class are listed in the following tables.

.. csv-table:: Inputs for structural analyzer -- ``mat_dict``
   :file: inputs_mat_dict.csv
   :widths: 70, 70, 30
   :header-rows: 1

.. csv-table:: Inputs for structural analyzer -- Dimensions
   :file: inputs_dimensions_sleeve.csv
   :widths: 70, 70, 30
   :header-rows: 1


The following code block demonstrates how to create both the problem and analyzer objects.
   
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
	
Outputs for SPM Sleeve Analyzers
*********************************

The following code-block demonstrates the usage of the sleeve analyzer. The analyzer returns back a list of optimal sleeve geometry, [``d_sl``, ``delta_sl``].

.. code-block:: python

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