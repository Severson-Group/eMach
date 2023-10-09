SynR Machine Operating Point
####################################

This class represents the operating point of a synchronous reluctance machine.

Input from User
*********************************

The required input from the user to instantiate this class is provided below:

.. csv-table:: `SynR Operating Point`
   :file: SynR_op_pt.csv
   :widths: 70, 70, 30
   :header-rows: 1


Creating a ``SynR_Machine_Oper_Pt`` object
*************************************************

Finally, the below ``Python`` code block shows how to create a ``SynR_Machine_Oper_Pt`` object.

.. code-block:: python

   from eMach.mach_eval.machines.SynR.SynR_oper_pt import SynR_Machine_Oper_Pt

   Machine_Op_Pt = SynR_Machine_Oper_Pt(
      speed=1800,
      speed_ratio=1,
      phi_0 = 0,
      ambient_temp=25,
      rotor_temp_rise=0,
   )
