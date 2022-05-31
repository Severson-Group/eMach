SPM Airflow Analyzer
####################
The ``AirflowAnalyzer`` is designed to determine how much supplemental axial airflow is needed to cool the rotor to a specified ``max_temp``. The problem class for the ``AirflowAnalyzer`` contains the :doc:`Rotor Thermal Analyzer <SPM_rotor_thermal_analyzer>` which is used to calculate the magnet temperature as a function of the axial airflow. The ``AirflowAnalyzer`` solve a single objective minimization problem subject to a constraint that the magnet temperature is less than ``max_temp``.

Model Background
****************

The SPM rotor is modeled using a thermal resistance network as shown in the figure. The implementation of the resistances and nodal locations can be found in the source code of the ``create_resistance_network`` method of ``SPM_RotorThemalAnalyzer``. In this analyzer, the axial airflow is varied to increase the convection rate on the rotor in order to improve cooling.

.. figure:: ./images/Resistance_Network.svg
   :alt: Trial1 
   :align: center
   :width: 600 

Inputs to the Rotor Airflow Analyzer
************************************
The airflow analyzer requires the following inputs to be defined for its problem class:

.. csv-table:: Material dictionary for rotor thermal analyzer -- ``mat_dict``
   :file: inputs_mat_dict_rotor_thermal.csv
   :widths: 70, 70, 30
   :header-rows: 1
   
.. csv-table:: Input dimensions for rotor thermal analyzer 
   :file: inputs_dimensions_rotor_airflow.csv
   :widths: 70, 70, 30
   :header-rows: 1
 

The following code demonstrates how the eMach thermal analyzer for the rotor can be used to calculate the required airflow to cool a rotor. 

.. code-block:: python

    import numpy as np
	from eMach.mach_eval.analyzers.thermal_analyzer import AirflowProblem,AirflowAnalyzer

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
	max_temp=80

	# Create an AirflowProblem object
	afp=AirflowProblem(r_sh, d_ri, r_ro, d_sl, r_si, l_st, l_hub, T_ref, losses,
					   omega, max_temp, mat_dict)
	# Create an Airflow Analyzer
	ana=AirflowAnalyzer()

Outputs from the Rotor Airflow Analyzer
****************************************
 
The following code demonstrates how to use the airflow analyzer to solve the airflow problem. The ``results`` object is a dictionary which contains the magnet temperature and the required airflow needed to cool the machine. If the rotor can not be cooled by axial airflow, then the ``message`` key of the dictionary will return ``False``.

.. code-block:: python


	# Analyze problem for required airflow
	results=ana.analyze(afp)
	print(results)
	
The ``results`` object returned by the analyzer for this example are in the following form:

.. code-block:: python

    {'message': True,
     'magnet Temp': array([73.43703021]),
     'Required Airflow': array([1.23618711e-08])}

