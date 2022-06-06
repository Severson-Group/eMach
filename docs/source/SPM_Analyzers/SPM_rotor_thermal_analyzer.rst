.. _rotor_therm_analyzer:

SPM Rotor Thermal Analyzer
##########################


This page describes how the thermal performance of a surface-mounted permanent magnet (SPM) rotor is evaluated using the eMach code base. This analyzer utilized the :doc:`Thermal Resistance Network Analyzer <../general_analyzers/thermal_res_net_analyzer>` to solve for the temperature distribution in the rotor.


Model Background
****************

The SPM rotor is modeled using a thermal resistance network as shown in the figure. The implementation of the resistances and nodal locations can be found in the source code of the ``create_resistance_network`` method of ``SPM_RotorThemalAnalyzer``.


.. figure:: ./Images/Resistance_Network.svg
   :alt: Trial1 
   :align: center
   :width: 600 
   
The required geometric dimensions and operating conditions needed to implement this model are shown in the following figure.

.. _therm-geo:
.. figure:: ./Images/Resistance_Network_Dim.svg
   :alt: Trial1 
   :align: center
   :width: 600 

Inputs to Rotor Thermal Analyzer
********************************

The ``SPM_RotorThemalAnalyzer`` takes in a ``SPM_RotorThemalProblem`` with inputs listed in the following tables.

.. _mat-dict-therm:
.. csv-table:: Material dictionary for rotor thermal problem -- ``mat_dict``
   :file: inputs_mat_dict_rotor_thermal.csv
   :widths: 70, 70, 30
   :header-rows: 1
   
.. csv-table:: Input losses for rotor thermal problem
   :file: Inputs_losses.csv
   :widths: 70, 70, 30
   :header-rows: 1     
   
.. csv-table:: Input dimensions and operating conditions for rotor thermal problem
   :file: inputs_dimensions_rotor_thermal.csv
   :widths: 70, 70, 30
   :header-rows: 1

   
   
The following code-block demonstrates how to create a ``SPM_RotorThemalProblem`` and ``SPM_RotorThemalAnalyzer``.


.. code-block:: python

    import numpy as np
    from eMach.mach_eval.analyzers.spm_rotor_thermal import SPM_RotorThermalProblem,SPM_RotorThermalAnalyzer
    from eMach.mach_eval.analyzers.spm_rotor_thermal import AirflowProblem,AirflowAnalyzer
    # Example Machine Dimensions
    r_sh=5E-3 # [m]
    d_m=3E-3 # [m]
    r_ro=12.5E-3 # [m]
    d_ri=r_ro-r_sh - d_m # [m]
    d_sl=1E-3 # [m]
    l_st=50E-3 # [m]
    l_hub=3E-3 # [m]
    r_si=r_ro+d_sl+1E-3 # [m]

    # Define Material Dictionary
    mat_dict= {'shaft_therm_conductivity': 51.9, # W/m-k ,
               'core_therm_conductivity': 28, # W/m-k
               'magnet_therm_conductivity': 8.95, # W/m-k ,
               'sleeve_therm_conductivity': 0.71, # W/m-k,
               'air_therm_conductivity'     :.02624, #W/m-K
               'air_viscosity'              :1.562E-5, #m^2/s
               'air_cp'                     :1, #kJ/kg
               'rotor_hub_therm_conductivity':205.0} #W/m-K}
    # Operating Conditions
    T_ref=25 # [C]
    omega=120E3*2*np.pi/60 # [rad/s]
    losses={'rotor_iron_loss':.001,'magnet_loss':135}
    u_z=0

    prob=SPM_RotorThermalProblem(mat_dict,r_sh,d_ri,r_ro,d_sl,r_si,l_st,l_hub,T_ref,u_z,losses,omega)
    ana=SPM_RotorThermalAnalyzer()


Outputs from Rotor Thermal Analyzer
***********************************
The ``SPM_RotorThemalAnalyzer``'s analyze method returns back the temperature at each node for the solution to the resistance network. (``T=ana.analyze(prob)``). The location of each numbered node in the machine is visualized in the figure below: 

.. figure:: ./Images/Resistance_Network_Full.svg
   :alt: Trial1 
   :align: center
   :width: 600 


