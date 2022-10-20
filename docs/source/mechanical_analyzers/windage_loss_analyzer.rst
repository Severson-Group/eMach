
Windage Loss Analyzer
#####################

This analyzer determines windage loss in a rotating machine with an inner rotor.

Model Background
****************

The analyzer assumes the simple motor structure shown below. This consists of a rotor inside of a stator and a forced axial airflow in the airgap of velocity u\ :sub:`z`\. 

.. figure:: ./Images/WindageLossDiagram.svg
   :alt: Windy 
   :align: center
   :width: 600 

The following losses occur in this system:

1. *Radial Losses:* Losses on the radial airgap surfaces due to rotation.
2. *Endface Losses:* Losses on the axial surfaces of the shaft due to rotation.
3. *Axial Losses:*  Losses on the radial airgap surfaces due to axial airflow through the airgap.

This analyzer determines the windage losses by implementing the model presented in the following papers:

* J. An, A. Binder and C. R. Sabirin, "Loss measurement of a 30 kW high speed permanent magnet synchronous machine with active magnetic bearings," `2013 International Conference on Electrical Machines and Systems` (ICEMS), 2013, pp. 905-910.
* B. Riemer, M. Leßmann and K. Hameyer, "Rotor design of a high-speed Permanent Magnet Synchronous Machine rating 100,000 rpm at 10kW," `2010 IEEE Energy Conversion Congress and Exposition`, Atlanta, GA, 2010, pp. 3978-3985.


Inputs from User
*********************************

The following inputs are required to create a `WindageLossProblem` object (with dimensions defined in the figure above):
 
.. csv-table:: Inputs for windage loss problem 
   :file: inputs_windage_loss_analyzer.csv
   :widths: 70, 70, 30
   :header-rows: 1

Example code initializing the windage loss analyzer and problem:

.. code-block:: python

    import numpy as np
    import eMach.mach_eval.analyzers.mechanical.windage_loss as wla
    from matplotlib import pyplot as plt

    Omega=1000
    R_ro=0.1
    axial_length=0.05
    R_st=0.105
    u_z=0.01
    T_air=25

    problem=wla.WindageLossProblem(Omega,R_ro,axial_length,R_st,u_z,T_air)
    ana=wla.WindageLossAnalyzer

Outputs to User
**********************************
The windage analyzer returns a list of windage losses in Watts in the following order:

1. ``windage_loss_radial``
2. ``windage_loss_endface`` (The endface losses are split evenly between the two rotor axial surfaces)
3. ``windage_loss_axial`` 

The total windage loss is the sum of all these losses.

Example code using the windage loss analyzer to determine losses as over a range of rotational speed ``Omega`` and plotting the results.

.. code-block:: python

    results=ana.analyze(problem)
    print(results)

    Omega_vect=np.linspace(1,1000,100)
    loss_vect=np.zeros([3,100])
    total_loss_vect=np.zeros_like(Omega_vect)
    for ind,Omega in enumerate(Omega_vect):
        problem=wla.WindageLossProblem(Omega,R_ro,axial_length,R_st,u_z,T_air)
        [windage_loss_radial,windage_loss_endface,windage_loss_axial]=ana.analyze(problem)
        loss_vect[:,ind]=[windage_loss_radial,windage_loss_endface,windage_loss_axial]
        total_loss_vect[ind]=sum([windage_loss_radial,windage_loss_endface,windage_loss_axial])
    fig,ax=plt.subplots(1,1)   
    ax.plot(Omega_vect,loss_vect.T)
    ax.plot(Omega_vect,total_loss_vect)
    ax.legend(['Radial','Endface','Axial','Total'])
    ax.set_xlabel('Rotational Speed [rad/s]')
    ax.set_ylabel('Windage Loss [W]')
    fig.savefig('WindageLossPlot.svg')
    
    
.. figure:: ./Images/WindageLossPlot.svg
   :alt: Windy 
   :align: center
   :width: 600 