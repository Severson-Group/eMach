Winding Factors Analyzer
##########################################

This analyzer determines the winding factors of a stator and winding layout for application in calculations of airgap harmonics.

Model Background
****************

Winding factors :math:`\bar{k}_\text{w}` are a way to quantify the effectiveness of a winding and affect various properties of an electric machine including
harmonics present in the airgap field, electric loading, etc. They can be thought of as a proportion of the geometric vector sum of coil side phases 
in a phase winding over the algebraic sum, or mathematically using the following expression usign a single phase:

.. math::

    \bar{k}_\text{w,v} &= \frac{1}{N} \Sigma_\text{i=1}^N \bar{k}_\text{pi,v} \\
    \bar{k}_\text{pi} &= e^{j n \alpha_\text{u}}

where :math:`N` is the total number of slots filled, :math:`\bar{k}_\text{p,i,v}` is the winding factor of each slot, :math:`n` is the harmonic index, 
and :math:`\alpha_\text{u}` is the angle at which each of the slots resides in radians. The equation for :math:`\bar{k}_\text{w,n}` is found to model 
the relationship between the geometric and algebraic sums as mentioned previously. The equation for :math:`\bar{k}_\text{p,i}` is found to model each individual
winding factor for each coil side at each slot. The winding factor for each :math:`n` should be calculated separately, as geometries within the calculations 
change with each value of :math:`n`. The sum of each of these calculations will result in a table of winding factors, all of which must be considered when 
choosing a design winding layout. This analyzer adds the ability to calculate a winding factor based only on a stator geometry and layout. The addition of this 
analyzer eliminates the need for hand calculations for winding factors within the bfield_outer_stator analyzer.

For example, given the layouts in the figure below, winding factors can be calculated for each of the stator geometries.

.. figure:: ./Images/Stator_Diagram.svg
   :alt: Winding_Layouts
   :align: center
   :width: 500 

The assumptions made going into the development of this model are:

1. Ideal slot fill factors
2. Ideal skew factors

Input from User
***************

Users are utilizing a single `problem` class to interface with this analyzer. This class requires the user to provide the number of harmonnics desired to
be analyzed, the winding layout of the stator, and the location of the first slot. It is assumed that the stator winding is excited with symmetric currents
and that slot fill and skew factors are ideal. The requirements can each be summarized below:

The number of harmonics being tested should be given as an array. The array can be either a specific array of each harmonic (1,2,5,etc.), or it can be a range 
of harmonics of length n (1,2,...,n).

The winding layout should also be given as an array. It should ONLY be provided for a single phase. In the case of this example, it will be using Phase U in the 
stator and winding layout provided. The number of columns in the array should be the number of slots in the stator. The number of rows in the array should be the 
number of layers in the stator. The top layer should be the first row and the bottom layer should be the bottom row. A "-1" should be indicated for a slot with 
windings going into the page, a "0" should be indicated for a slot with no windings present, and a "1" should be indicated for a slot with windings coming out 
of the page. Each winding layer should consume a single row of the winding array. Each slot should consume a single column of the winding array.

The location of the first slot should be indicated in radians from the +x axis. For example, a stator with the first slot at the x-axis will have an 
:math:`\alpha_\text{1}` of 0 radians. The stator geometry in the picture below would have an :math:`\alpha_\text{1}` of :math:`\frac{\pi}{12}` radians.

.. figure:: ./Images/Winding_Diagram.svg
   :alt: Slot_Angles
   :align: center
   :width: 500 

The required input from the user along with the expected units for the `problem` class can be summarized below:

.. csv-table:: `OuterStatorBnfieldProblem1`
   :file: input_winding_factors.csv
   :widths: 70, 70, 30
   :header-rows: 1

Example code initializing the analyzer and problem1 for the stator and winding layout shown is provided below:

.. code-block:: python

    import numpy as np
    from eMach.mach_eval.analyzers.electromagnetic.winding_factors import (
        WindingFactorsProblem,
        WindingFactorsAnalyzer,
        )

    n = np.array([1,2,3,4,5])
    winding_layout = np.array([[-1,-1,0,0,0,0,1,1,0,0,0,0],[0,0,0,0,1,1,0,0,0,0,-1,-1]])
    alpha_1 = 0
    kw_prob = WindingFactorsProblem(n,winding_layout,alpha_1)

    kw_ana = WindingFactorsAnalyzer()

Output to User
***************
The winding factors analyzer returns a `WindingFactors` table. This table has structure that the winding factors are listed for each harmonics_list variable. The 
first value represents the first harmoincs_list variable, the second value represents the second variable, and so on.

Example code using the analyzer to determine the winding factors for each harmonic is provided below (continuation from previous code block):

.. code-block:: python

    k_w = kw_ana.analyze(kw_prob)

.. figure:: ./Images/Winding_Factors.svg
   :alt: Winding_Factors 
   :align: center
   :width: 500

Application to B Field Outer Stator Analyzer
********************************************

In order to plot the current linkage and find the magnetic field of the inner bore of the stator, the winding factor analyzer can be applied to the B Field Outer
Stator Analyzer by adding some code and making some alterations. 

The definitions of the "harmonics of interest" and "winding factors" (variables "k_w" and "n") can be changed and defined below. Note that for plotting the current
linkage, all of the harmonics should be considered. While in reality that is not possible, in practice a number on the scale of :math:`$10^3` should be used:

.. code-block:: python

    from eMach.mach_eval.analyzers.electromagnetic.winding_factors import (
    WindingFactorsProblem,
    WindingFactorsAnalyzer,
    )

    n = np.arange(1,1000)
    winding_layout = np.array([[-1,-1,0,0,0,0,1,1,0,0,0,0],[0,0,0,0,1,1,0,0,0,0,-1,-1]])
    alpha_1 = np.pi/12
    kw_prob = WindingFactorsProblem(n,winding_layout,alpha_1)

    kw_ana = WindingFactorsAnalyzer()

    k_w = kw_ana.analyze(kw_prob)

This block is redefining the harmonics of interset, providing the winding layout and :math:`\alpha_\text{1}`, and actually calculating the winding factors instead
of having them directly provided. From here, the B Field Outer Stator Analyzer code should be entered as existing. After it is written, the following code should 
be implemented to plot the current linkage:

.. code-block:: python

    mmf_comp = stator_Bn_prob.mmf(zq, Nc, n, k_w, I_hat) * np.cos(n * alpha + np.pi/2)
    B_total_radial = np.sum(mmf_comp,axis=1)

    linkage = B_total_radial*delta_e/(4*np.pi*10**(-7)) # <-- ADDED
    fig2 = plt.figure()
    ax = plt.axes()
    fig2.add_axes(ax)
    # plot current linkage
    ax.plot(alpha, linkage)

    ax.set_xlabel(r"$\alpha$ [deg]")
    ax.set_ylabel("$Current Linkage$ [A]")
    ax.set_title("Current Linkage Diagram")
    plt.grid(True, linewidth=0.5, color="#A9A9A9", linestyle="-.")
    plt.show()

This code is taking the MMF function from the B Field Outer Stator Analyzer and calculating the currently linkage directly. Within the B Field Outer Stator Analyzer,
this is then used to calculate the radial and tangential components of the B Field. The applied code should return the following plot for the current linkage of the 
stator and winding layout depicted above:

.. figure:: ./Images/Current_Linkage_Plot.svg
   :alt: Current_Linkage 
   :align: center
   :width: 500