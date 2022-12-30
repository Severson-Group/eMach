Stator Winding Resistance Analyzer
##########################################

This analyzer determines stator winding resistance, considering effects of end windings.

Model Background
****************

The following equation is used to calculate stator winding resistance:

.. math::

    R_\text{wdg} &= \frac{z_Q z_C l_\text{coil}}{\sigma_\text{cond} A_\text{cond}}\\

where :math:`z_Q` is a number of turns per coil, :math:`z_C` is a number of coils per phase, :math:`l_\text{coil}` is a length of a coil including coil ends, and :math:`\sigma_\text{cond}` and :math:`A_\text{cond}` are conductor conductivity and cross-section area. 
Conductor area is found as :math:`A_\text{cond} = K_\text{Cu}A_\text{slot}/z_Q`, where :math:`A_\text{slot}` is a stator slot area and :math:`K_\text{Cu}` is a slot fill factor. The length of a coil consists of two main parts:

.. math::

    l_\text{coil} &= 2(l_\text{st} + l_\text{end wdg})\\

Here, :math:`l_\text{st}` is a length of a coil along the axial length of a motor and :math:`l_\text{end wdg}` is an end winding length. A factor of two is included to take into account a returning coil side.

Equation that is used to estimate :math:`l_\text{end wdg}` is shown below:

.. math::

    l_\text{end wdg} &= \frac{1}{2} \pi \frac{\tau_u + w_\text{st}}{2} + \tau_u K_\text{ov} (y - 1)\\

This equation consists of two main parts.
The first part is a length of bent parts of a coil end, which is evaluated as a length of a half-circle with a diameter :math:`(\tau_u + w_\text{st})/2`. 
Here, :math:`w_\text{st}` is a stator tooth width and :math:`\tau_u` is an arc length between adjacent slots evaluated at a median depth of a slot:

.. math::

    \tau_u &= \frac{2 \pi}{Q} (r_\text{si} + d_\text{sp} + d_\text{st})\\

where :math:`r_\text{si},~d_\text{sp},~d_\text{st}` are stator dimensions in a radial direction (described more in the next section).
The second part in the equation of :math:`l_\text{end wdg}` is a length of a coil end that appears in distributed windings where coil pitch :math:`y > 1`. :math:`K_\text{ov}` is a coil overlength factor.


Input from User
*********************************

User is required to provide the following parameters.

.. csv-table:: `Input to stator winding resistance problem`
   :file: input_stator_wdg_res.csv
   :widths: 50, 70, 50
   :header-rows: 1

For the definition of dimensions, please refer :doc:`here <../machines/bspm/bspm_machine>`.


Output to User
**********************************

Stator winding resistance analyzer returns the following scalar values:

.. csv-table:: `Output of stator winding resistance analyzer`
   :file: output_stator_wdg_res.csv
   :widths: 50, 70, 50
   :header-rows: 1

Here, the total winding resistance `R_wdg` is the sum of `R_wdg_coil_ends` and `R_wdg_coil_sides`.


Example code using resistance analyzer is provided below.

.. code-block:: python

    import numpy as np
    from eMach.mach_eval.analyzers.electromagnetic.stator_wdg_res import (
        StatorWindingResistanceProblem,
        StatorWindingResistanceAnalyzer
        )

    # define problem and analyzer
    res_prob = StatorWindingResistanceProblem(
        r_si=34.45/1000,
        d_sp=3.95/1000,
        d_st=20.75/1000,
        w_st=5.38/1000,
        l_st=50/1000,
        Q=24,
        y=9,
        z_Q=16,
        z_C=4,
        Kcu=0.5,
        Kov=1.8,
        sigma_cond=5.7773*1e7,
        slot_area=251*1e-6,
        )
    res_analyzer = StatorWindingResistanceAnalyzer()

    # analyze the problem
    R_wdg, R_wdg_coil_ends, R_wdg_coil_sides = res_analyzer.analyze(res_prob)

The output of the code is `R_wdg = 0.07 Ohms`, `R_wdg_coil_ends = 0.056 Ohms`, and `R_wdg_coil_sides = 0.014 Ohms`.