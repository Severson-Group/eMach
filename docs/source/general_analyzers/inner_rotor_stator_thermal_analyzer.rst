

Inner Rotor Stator Thermal Analyzer
###################################

This analyzer is designed to evaluate the temperature distribution in the stator of an inner rotor machine. This analyzer does not utilize the thermal resistance network analyzer, and is a set of stand alone equations for solving the coil temperature.


Model Background
****************

This analyzer is based on the solution of coupled 1-dimension temperature distribution for an inner rotor stator. A detailed description of the math can be found in Chapter III Section 3.3 of Martin Johnson's Masters Thesis:

* M. W. Johnson, “Multi-Physics Design Sizing of High-Speed Surface Mounted Permanent Magnet Motors to Improve Design Ratings,” MS. Thesis, University of Wisconsin-Madison, 2022

.. figure:: ./Images/SlotGeometry.svg
   :alt: Trial1 
   :align: center
   :width: 600 

The presented analyzer is designed to operate under the following assumptions:

* **The temperature distribution is symmetric about the stator slots.** Provided there is uniform loading and cooling of the machine, there should not be any difference in the temperature distribution from one slot to another.
* **The temperature of the coil is uniform in the slot.** The insulation paper used to prevent shorts has a much lower thermal conductivity than the coils in the slot, allowing for the temperature distribution of the coil to be neglected.
* **There is no heat transfer on the surface of the inner tooth of the stator.** However, note that the air on the inner surface of the machine may actually provide additional cooling. By neglecting it, an upper bound for the stator temperatures is found.
* **Heat can only flow in the radial and tangential direction.** there is no cooling on the top or bottom surface of the stator or in the end-winding regions of the coils. Again there may be additional cooling on these surfaces, but the stator core has a lower thermal conductivity through the laminations in the axial direction compared to the radial direction. This reduces the effectiveness of the any cooling on these surfaces.




Inputs from User
*********************************

The required inputs to initializes the ``StatorThermalProblem`` are summarized in the table below and the geometric inputs are visualized in the cross section shown above.

.. csv-table:: Inputs for stator thermal problem 
   :file: inputs_stator_thermal_analyzer.csv
   :widths: 70, 70, 30
   :header-rows: 1
   
The analyzer takes in convection coefficients ``h`` and ``h_slot``. The ``h`` convection coefficient represents the convection rate on the exterior of the stator at ``r_so``. The analyzer is capable of modeling direct coil cooling though the ``h_slot`` which models a convection rate directly on the coil as discussed in Chapter V Section 5.4.2 of Martin Johnson's Masters Thesis. The following papers provide general ranges of convection coefficients which may assumed:

* F. Nishanth; Martin Johnson; Eric L. Severson: “A Review of Thermal Analysis and Management of Power Dense Electric Machines”, 2021 IEEE International Electric Machines & Drives Conference, 2021, pp. 1-8.
* K. Bennion and G. Moreno, “Convective heat transfer coefficients of automatic transmission fluid jets with implications for electric machine thermal management,” in ASME 2015 International Technical Conference and Exhibition on Packaging and Integration of Electronic and Photonic Microsystems, vol. 3, 2015.
* P. Kosky, R. T. Balmer, W. D. Keat, and G. Wise, Exploring engineering: an introduction to engineering and design. Academic Press, 2015.
* W. Sixel, M. Liu, G. Nellis, and B. Sarlioglu, “Ceramic 3d printed direct winding heat exchangers for improving electric machine thermal management,” in 2019 IEEE Energy Conversion Congress and Exposition (ECCE), 2019, pp. 769–776.
* W. Sixel, M. Liu, G. Nellis, and B. Sarlioglu, “Cooling of windings in electric machines via 3-d printed heat exchanger,” IEEE Transactions on Industry Applications, vol. 56, no. 5, pp. 4718–4726, 2020.
* F. Nishanth; Martin Johnson; Eric L. Severson: “A Review of Thermal Analysis and Management of Power Dense Electric Machines”, 2021 IEEE International Electric Machines & Drives Conference, 2021, pp. 1-8.

The following code block demonstrates how to initialize the stator thermal problem and analyzer:

.. code-block:: python

    import numpy as np
    import eMach.mach_eval.analyzers.general.thermal_stator as sta
    from matplotlib import pyplot as plt
    
    Q= 6 #Number of Slots
	g_sy = 10000 #Volumetric losses in yoke [W/m^3]
	g_th = 100000 #Volumetric losses in tooth [W/m^3]
	w_tooth = 0.02 #Tooth width [m]
	l_st = 0.05 #Stack length
	alpha_q = np.pi/Q #slot span [rad]
	r_si =0.03 #Inner stator radius [m]
	r_so = 0.1 #Outer stator radius [m]
	r_sy = .08 #Inner stator yoke radius [m]
	k_ins = 1 #Insulation thermal conductivity [W/m-K]
	w_ins =.001 #Insulation Thickness [m]
	k_fe = 38 #Stator iron thermal conductivity [W/m-k]
	h = 100 #Exterior convection coefficient [W/m^2-k]
	alpha_slot = .7 *alpha_q # back of slot span [rad]
	Q_coil = 40 # Coil losses [W]
	h_slot =0 #Inslot convection coefficient [W/m^2-K]

	problem = sta.StatorThermalProblem(
				g_sy,
				g_th,
				w_tooth,
				l_st,
				alpha_q,
				r_si,
				r_so,
				r_sy,
				k_ins,
				w_ins,
				k_fe,
				h,
				alpha_slot,
				Q_coil,
				h_slot,
			)
	ana = sta.StatorThermalAnalyzer()


Outputs to User
************************************

The ``StatorThermalAnalyzer`` outputs a dictionary object with the following keys:

* ``Coil temperature``: Mean temperature of the stator coil in Celsius
* ``Stator yoke temperature``: Temperature on exterior surface of the stator in Celsius


The following code-block demonstrates how the results are returned by the analyzer:

.. code-block:: python

    results = ana.analyze(problem)
    print(results)
    
    {'Coil temperature': 196.31038291260649, 'Stator yoke temperature': 184.06667848224436}
    
The analyzer can be utilized in to examine the effect of changing stator geometry as demonstrated in the following code-block. The stator tooth length is swept over ``l_tooth_vect``, and the coil temperature is collected for each entry. The following code will produce the plot shown below, provided the rest of the inputs to the ``StatorThermalProblem`` are used from the previous section.

.. code-block:: python

    l_tooth_vect=np.linspace(.01,.8,100)
	T_coil_vect=np.zeros_like(l_tooth_vect)
	for ind,l_tooth in enumerate(l_tooth_vect):
		r_sy= l_tooth+r_si
		r_so= r_sy+.2
		problem = sta.StatorThermalProblem(
				g_sy,
				g_th,
				w_tooth,
				l_st,
				alpha_q,
				r_si,
				r_so,
				r_sy,
				k_ins,
				w_ins,
				k_fe,
				h,
				alpha_slot,
				Q_coil,
				h_slot,
			)
		ana = sta.StatorThermalAnalyzer()
		results = ana.analyze(problem)  
		T_coil_vect[ind]=results['Coil temperature']

	fig,ax=plt.subplots(1,1)
	ax.plot(l_tooth_vect,T_coil_vect)
	ax.set_xlabel('Stator tooth length [m]')
	ax.set_ylabel('Coil temperature [C]')


.. figure:: ./Images/ToothLength_CoilTemp.svg
   :alt: Just do it TM 
   :align: center
   :width: 600 
