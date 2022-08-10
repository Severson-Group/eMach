Bearingless Surface Permananet Magnet Motor JMAG 2D FEA Analyzer
########################################################################

This analyzer enables the 2d FEA evaluation of select bearingless surface permanent magnet (BSPM) topologies with DPNV windings in JMAG.

Model Background
****************

Typically, normal :math:`B_n` and tangential :math:`B_{tan}` fields created in the airgap of an electric machine are analytically determined
using the following equations:

.. math::

    \hat{B}_\text{n} &= \frac{\mu_0 \hat{A} r_\text{si}}{p \delta}  \\
    \hat{B}_\text{tan} &= -\mu_0 \hat{A}

where :math:`\hat{A}` is the electric loading, :math:`r_{si}` is the inner stator bore radius, :math:`p` is the number of pole pairs of the
winding, and :math:`\delta` is the airgap. The equation for :math:`B_{tan}` is found to model the actual stator winding tangential 
fields fairly accurately, provided the iron is not saturated. The equation for :math:`B_{n}` however varies greatly from actual 
radial fields in the airgap, especially as the airgap gets significantly large, even when the machine is operating well within the linear 
region of the magnetic steel. This analyzer improves upon the accuracy of the stator winding radial field equation by considering stator slot 
opening and motor airgap curvature effects. The assumed motor 2D-cross-section for this analyzer is shown below. The direction along which 
:math:`B_n` and :math:`B_{tan}` are taken to be positive has also been indicated in the figure. The analyzer can be extended to machines with 
permanent magnets on the rotor surface by considering an airgap of equivalent remanence.

.. figure:: ./Images/OuterStatorBFieldsFig.svg
   :alt: Stator_Bn 
   :align: center
   :width: 500 

The assumptions that have gone into the developement of this model are:

1. Electric steel has infinite permeability.
2. Both the rotor and stator have negligible eddy currents.
3. The rotor is non-salient.

This analyzer implements the model(s) provided in the following references:

* G. Bergmann and A. Binder, “Design guidelines of bearingless PMSM with two separate poly-phase windings,” in 2016 XXII International 
  Conference on Electrical Machines (ICEM), Lausanne, Switzerland, Sep. 2016
* Z. Q. Zhu and D. Howe, “Instantaneous magnetic field distribution in brushless permanent magnet DC motors. II. Armature-reaction field,” 
  IEEE Trans. Magn., vol. 29, no. 1

Input from User
*********************************

The figure below provides the convention used to determine the MMF waveform, and thereafter, the MMF harmonics.

.. figure:: ./Images/MMF_convention.svg
   :alt: Stator_Bn 
   :align: center
   :width: 500 

The required input from the user along with the expected units for both `problem` classes are provided below:

.. csv-table:: `OuterStatorBnfieldProblem1`
   :file: input1_stator_b_field_analyzer.csv
   :widths: 70, 70, 30
   :header-rows: 1
 

Example code initializing the analyzer and problem1 is shown below:

.. code-block:: python

    import numpy as np
    from matplotlib import pyplot as plt
    from eMach.mach_eval.analyzers.electromagnetic.outer_stator_bfields import (
        OuterStatorBFieldAnalyzer,
        OuterStatorBnfieldProblem1,
    )

    m = 3  # number of phases
    zq = 20  # number of turns
    Nc = 2  # number of coils per phase
    k_w = np.array(
        [
            0.5 * np.exp(1j * np.pi / 3),
            0.866 * np.exp(-1j * np.pi / 5),
            0,
            0.866 * np.exp(-1j * 0),
            0.5 * np.exp(1j * np.pi / 6),
        ]
    )  # winding factors
    I_hat = 30  # peak current
    n = np.array([1, 2, 3, 4, 5])  # harmonics of interest
    delta_e = 0.002  # airgap
    r_si = 0.025  # inner stator bore radius
    r_rfe = r_si - delta_e  # rotor back iron outer radius
    alpha_so = 0.1  # stator slot opening in radians

    # define problem
    stator_Bn_prob = OuterStatorBnfieldProblem1(
        m=m,
        zq=zq,
        Nc=Nc,
        k_w=k_w,
        I_hat=I_hat,
        n=n,
        delta_e=delta_e,
        r_si=r_si,
        r_rfe=r_rfe,
        alpha_so=alpha_so,
    )

    # define analyzer
    stator_B_ana = OuterStatorBFieldAnalyzer()

Output to User
**********************************
The outer stator B field analyzer returns a `OuterStatorBField` object. This object has methods such as `radial` and `tan` which can be 
leverage to determine B fields across the airgap of the machine.

Example code using the analyzer to determine and plot :math:`B_n` and :math:`B_{tan}` at the inner bore of the stator is provide below
(continuation from previous code block):

