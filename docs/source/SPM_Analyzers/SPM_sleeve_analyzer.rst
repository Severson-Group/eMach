
.. _sleeve_analyzer:

SPM Sleeve Analyzer
###################

This analyzer determines the design of a sleeve with minimum thickness to retain magnets on a surface-mounted permanent magnet (SPM) rotor. 

Model Background
****************
The SPM rotor is assumed to consist of four components, a shaft, rotor back iron, magnets, and a sleeve, shown below. The sleeve utilizes an undersized fit to provide compressive force on the rotor. Whether or not it is possible to design a sleeve that can retain the magnets depends upon the specified rotor geometry, materials, and maximum operating speed and temperature. This analyzer determines if a valid sleeve design exists. If a design does exist, the analyzer determines the undersize and thickness of the thinnest possible sleeve. 

.. figure:: ./Images/RotorConfig.svg
   :alt: Trial1 
   :align: center
   :width: 300 


.. figure:: ./Images/SleeveOrientation.svg
   :alt: Trial1 
   :align: center
   :width: 300 

This analyzer implements the sleeve design approach developed in Section IV-A of `this paper <https://ieeexplore.ieee.org/document/9595523>`_:

- M Johnson, K. Hanson and E. L. Severson, "Normalized Analytical Model of Stresses in a Surface Mounted Permanent Magnet Rotor," `2021 IEEE Energy Conversion Congress and Exposition (ECCE)`, 2021, pp. 3928-3935.


Input from User
************************************

To create the problem object, the user must specify the following dimensions (defined in the drawings above) and the maximum rotor temperature rise (as defined :ref:`here <deltaT>`) and speed: 

.. csv-table:: Input for sleeve problem -- Dimensions and Operating Conditions 
   :file: inputs_dimensions_sleeve.csv
   :widths: 70, 70, 30
   :header-rows: 1

The user must also create a dictionary of material properties. This class uses the same ``mat_dict`` specified in the :ref:`SPM structural analyzer <mat-dict>`.
  
To create the analyzer, the user must specify limits on the critical stresses of the rotor magnets and sleeve material. See Table VI of the `reference paper <https://ieeexplore.ieee.org/document/9595523>`_ for additional information. When defining these stress limits, a safety factor is often used. The safety factor is a ratio of the failure point to the allowable limit, so a safety factor of 2 would mean that the maximum allowable stress is half that of failure stress ``2=stress_failure/stress_allowed``.

.. csv-table:: Critical stress limits to provide to rotor sleeve analyzer -- ``stress_limits``
   :file: inputs_sleeve_stress.csv
   :widths: 70, 70, 30
   :header-rows: 1

Example code to initialize the sleeve analyzer and problem:
   
.. code-block:: python

    import eMach.mach_eval.analyzers.spm.rotor_structural as sta
    
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
    problem = sta.SPM_RotorSleeveProblem(r_sh, d_m, r_ro, deltaT, mat_dict, N)
    ana = sta.SPM_RotorSleeveAnalyzer(stress_limits)

Advanced Analyzer Configuration
""""""""""""""""""""""""""""""""

*Requirements for the Problem Object:* The analyzer requires the problem object have a set of methods (``rad_magnet``, ``tan_magnet``, ``rad_sleeve``, ``tan_sleeve``) which take in a tuple of [``d_sl``, ``delta_sl``], representing the sleeve thickness and sleeve undersize, and return the values for each of the critical stresses. 

*Using a Custom Structural Analyzer:* This analyzer utilizes a structural analyzer to calculate the stresses inside the sleeve and magnets as part of its design process. By default, this analyzer utilizes the :doc:`SPM Structural Analyzer <SPM_structural_analyzer>`. However, the user can configure the problem object to use a different analyzer through the optional problem initializer arguments ``problem_class`` and ``analyzer_class``. Note that the replacement problem and analyzer must have the same function signature as :doc:`SPM Structural Analyzer <SPM_structural_analyzer>`.

    
Output to User
*********************************

The analyzer's return value depends on whether a valid sleeve exists.

- *No valid sleeve design:* The analyzer returns `False`. This means that a sleeve undersize and thickness does not exist that can retain the magnets.
- *Valid sleeve design:* The analyzer returns back a the sleeve geometry dimensions [``d_sl``, ``delta_sl``] in units of m that result in the thinnest possible sleeve.

Example code:

.. code-block:: python

    ######################################################
    #Calculate optimal sleeve geometry
    ######################################################
    sleeve_dim = ana.analyze(problem)
    print(sleeve_dim)


The following results will print on the command line. The first set of lines are diagnostic data that prints to the command line from inside the analyzer and indicates that the analyzer found a valid sleeve. The last line is the returned data and indicates that the sleeve has a thickness of ``1.649E-4`` [m] and optimal undersize of ``-1.211E-4`` [m].

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