.. _thermal_res_net_analyzer:

Thermal Resistance Network Analyzer
#######################################


This page describes how the thermal performance of a surface-mounted permanent magnet (SPM) rotor is evaluated using the eMach code base. The thermal analyzer implemented is a combination of two analyzers. A base thermal analyzer is used to solve a thermal resistance network for steady state temperatures, and an airflow analyzer calculates the the required additional axial airflow needed to properly cool the rotor. A detailed description of the math and physics for this problem can be found in Chapter 3 of Martin Johnson's Master's Thesis (TODO add this when the thesis is finished...)

Model Background
****************

The SPM rotor is modeled using a thermal resistance network as shown in the figure. The implementation of the resistances and nodal locations can be found in the source code of the ``RotorThemalProblemDef``. The thermal resistance network is used in conjunction with losses from electromagnetic FEA found by the EM analyzer to estimate the steady state temperature of the rotor.

.. figure:: ./images/Thermal/Resistance_Network.svg
   :alt: Trial1 
   :align: center
   :width: 600 


Base Thermal Analyzer
************************
The base thermal analyzer is designed to take in a ``problem`` object which describes the thermal resistance network. The ``analyzer`` takes the information provided in the ``problem`` and creates the required matrices to solve the steady state temperature distribution for the nodes of the resistance network. The analyzer returns back a list of the steady state temperatures at every nodal position in the resistance network.

Airflow Analyzer
****************
The ``AirflowAnalyzer`` is designed to determine how much supplemental axial airflow is needed to cool the rotor to a specified ``max_temp``. The problem class for the ``AirflowAnalyzer`` contains the base thermal analyzer which is used to calculate the magnet temperature as a function of the axial airflow. The ``AirflowAnalyzer`` solve a single objective minimization problem subject to a constraint that the magnet temperature is less than ``max_temp``.


How to use the structural analyzer
**********************************
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

	# Analyze problem for required airflow
	results=ana.analyze(afp)
	print(results)
	
The ``results`` object returned by the analyzer are a dictionary with the following form:

.. code-block:: python

    {'message': True,
     'magnet Temp': array([73.43703021]),
     'Required Airflow': array([1.23618711e-08])}


