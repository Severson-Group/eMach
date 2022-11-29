Winding Factors Analyzer
##########################################

This analyzer determines the winding factors of a stator and winding layout for application in calculations of airgap harmonics.

Model Background
****************

Winding factors :math:`\bar{k}_\text{w}` are a way to quantify the effectiveness of a winding and affect various properties of an electric machine including
harmonics present in the airgap field, electric loading, etc. They can be thought of as a proportion of the geometric vector sum of coil side phases 
in a phase winding over the algebraic sum, or mathematically using the following expression usign a single phase:

.. math::

    \bar{k}_\text{w,n} &= \frac{1}{N} \Sigma \bar{k}_\text{p,i,v} \\
    \bar{k}_\text{p,i} &= e**(j n \alpha_\text{u})

where :math:`N` is the total number of slots filled, :math::`\bar{k}_\text{p,i,v}` is the winding factor of each slot, :math::`n` is the harmonic index, 
and :math::`\alpha_\text{u}` is the angle at which each of the slots resides in radians. The equation for :math::`\bar{k}_\text{w,n}` is found to model 
the relationship between the geometric and algebraic sums as mentioned previously. The equation for :math::`\bar{k}_\text{p,i}` is found to model each individual
winding factor for each coil side at each slot. The winding factor for each :math::`n` should be calculated separately, as geometries within the calculations 
change with each value of :math::`n`. The sum of each of these calculations will result in a table of winding factors, all of which must be considered when 
choosing a design winding layout. This analyzer adds the ability to calculate a winding factor based only on a stator geometry and layout. The addition of this 
analyzer eliminates the need for hand calculations for winding factors within the bfield_outer_stator analyzer.

For example, given the layouts in the figure below, winding factors can be calculated for each of the stator geometries.

.. figure:: ./Images/WindingLayouts.PNG
   :alt: Winding_Layouts
   :align: center
   :width: 500 

The assumptions made going into the development of this model are:

1. Ideal slot fill factors
2. Ideal skew factors

Input from User
*********************************

Users are utilizing a single `problem` class to interface with this analyzer. This class requires the user to provide the number of harmonnics desired to
be analyzed, the winding layout of the stator, and the location of the first slot. It is assumed that the stator winding is excited with symmetric currents
and that slot fill and skew factors are ideal. The number of harmonics being tested should be given as an array (1,2,5,etc.). The winding layout should also be
given as an array (1,0,-1,1,etc.). A 1 should be indicated for a slot with windings going into the page, a 0 should be indicated for a slot with no windings
present, and a -1 should be indicated for a slot with windings coming out of the page. Each winding layer should consume a row of the winding array. For example,
a double layer winding should be a 2 x Q array, where there are 2 layers of Q slots. Lastly, the location of the first slot should be indicated in radians from
the +x axis. For example, a stator with the first slot at the x-axis will have an :math::`\alpha_\text{1}` of 0 radians. The stator geometry in the picture below
would have an :math::`\alpha_\text{1}` of :math::`\frac{\pi}{12}` radians.

.. figure:: ./Images/SlotAngles.PNG
   :alt: Slot_Angles
   :align: center
   :width: 500 

The required input from the user along with the expected units for the `problem` class is provided below:

.. csv-table:: `OuterStatorBnfieldProblem1`
   :file: input_winding_factors.csv
   :widths: 70, 70, 30
   :header-rows: 1

Example code initializing the analyzer and problem1 is shown below:

.. code-block:: python

    import numpy as np
    from eMach.mach_eval.analyzers.electromagnetic.winding_factors import (
        WindingFactorsProblem,
        WindingFactorsAnalyzer,
        )

    n = np.array([1,2,3,4,5])
    winding_layout = np.array([[1,-1,0,0,0,0,0,0,0,0,1,-1]])
    alpha_1 = 0
    kw_prob = WindingFactorsProblem(n,winding_layout,alpha_1)

    kw_ana = WindingFactorsAnalyzer()

Output to User
**********************************
The winding factors analyzer returns a `WindingFactors` table. This table has structure that the winding factors are listed for each harmonics_list variable. The 
first value represents the first harmoincs_list variable, the second value represents the second variable, and so on.

Example code using the analyzer to determine the winding factors for each harmonic is provided below (continuation from previous code block):

.. code-block:: python

    k_w = kw_ana.analyze(kw_prob)

.. figure:: ./Images/WindingFactors.PNG
   :alt: Winding_Factors 
   :align: center
   :width: 500