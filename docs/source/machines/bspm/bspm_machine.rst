BSPM Machine
########################################################################

This analyzer enables the 2-D transient FEA evaluation of select bearingless surface permanent magnet machine topologies with DPNV 
windings in JMAG.

Machine Background
*************************

Bearingless motors are electric machines capable of simultaneously creating both torque and forces. FEA tools are generally required to 
evaluate the performance capabilities of these machines. The analyzer does everything that is required for evaluating a BPSM design from
drawing the machine geometry to solving the magnetic vector potential matrices. The motor shaft and magnets are assumed to be conductive,
and therefore, eddy current losses are enabled in these components. As there are several configurations that can be modifies for any FEA
evaluation, a `JMAG_2D_Config` is provided to work alongside this analyzer. A description of the configurations users have control over
from within this class is provided below.

Time Step Size 
------------------

A key enabling factor of FEA is that it discretizes machine evaluation both in time and in space. The control users have over time step size 
with this analyzer is elaborated below.

The BSPM FEA analyzer has been setup such that it has 2 distinct time steps. The underlying concept behind having 2 distinct time steps is
to allow artificially created transient effects during FEA solver initialization to dampen out before using FEA data to evaluate the motor's 
performance. Both time steps have 2 variables, number of revolutions and number of steps per revolution. Users should change these
values based on what makes the most sense for their machine. Generally, the step size should be the same across both time steps, with the
1st time step running for lesser number of revolutions. It is recommended that the 2nd time step should last for atleast a half 
revolution to get reliable information on the motor's performance capabilities.

Mesh Size 
------------------

Meshing is the methob by which FEA tools discretize the motor geometry. In this analyzer, we use the slide mesh feature of JMAG. In addition
to a generic mesh size setting for the model, separate handles are provided for the magnet and airgap meshes in the `JMAG_2D_Config` class.
It is recommended that both the airgap and magnet mesh be significantly denser than that of other components for obtaining accurate results.
Users should balance mesh density with result accuracy to get reliable results as quickly as possible. Figures showing the mesh layout of
an example motor design are provided below.

.. list-table:: 

    * - .. figure:: ./Images/mesh_ex.PNG
           :alt: Complete machine mesh
           :width: 300 

      - .. figure:: ./Images/zoom_mesh_ex.png
          :alt: Zoomed mesh
          :width: 300 

Other configurations
---------------------------

In addition to time step and mesh size, several other changes can be made to the BSPM JMAG analyzer. Most of these configurations are self
explanatory and are descirbed using comments withing the `JMAG_2D_Config` class. For example: by setting the `jmag_visible` to `True` or 
`False`, users can control whether the JMAG application will be visible while a FEA evaluation is running.

Input from User
*********************************

To use the JMAG BSPM FEA analyzer, users must pass in a `BSPM_EM_Problem` object. An instance of the `BSPM_EM_Problem` class can be created
by passing in a `machine` and an `operating_point`. The machine must be a `BSPM_Machine` and the `operating_point` must be of type
`BSPM_EMAnalyzer_Settings`. More information on both these classes is available here. 

Example code initializing both the analyzer and problem is shown below:

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

