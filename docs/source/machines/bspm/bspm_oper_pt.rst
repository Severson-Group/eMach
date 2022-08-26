BSPM Machine Operating Point
####################################

This class represents the operating point of a bearingless surface permanent magnet machine.

Input from User
*********************************

The required input from the user to instantiate this class is provided below:

.. csv-table:: `BSPM Operating Point`
   :file: bspm_op_pt.csv
   :widths: 70, 70, 30
   :header-rows: 1


Creating a ``BSPM_Machine_Oper_Pt`` object
*************************************************

Finally, the below ``Python`` code block shows how to create a ``BSPM_Machine_Oper_Pt`` object. The arguments are provided to replicate the
rated operating conditions of the optimized BSPM design discussed in this `paper <https://ieeexplore-ieee-org.ezproxy.library.wisc.edu/document/9236181>`_.

.. code-block:: python

   from eMach.mach_eval.machines.bspm.bspm_oper_pt import BSPM_Machine_Oper_Pt

   ecce_2020_op_pt = BSPM_Machine_Oper_Pt(
                  Id=0,
                  Iq=0.975,
                  Ix=0,
                  Iy=0.025,
                  speed=160000,
                  ambient_temp=25,
                  rotor_temp_rise=55,
               )
