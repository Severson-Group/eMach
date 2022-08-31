BSPM Optimization Tutorial
===========================================

* **Goal:** Leverage capabilites of ``mach_opt`` and ``mach_eval`` to perform multi-objective, multi-physics optimization of
  bearingless surface permamanent magnet machines
* **Complexity** 4/5
* **Estimated Time** 30 - 60 min

This tutorial demonstrates how to perform a multi-objective, multi-physics optimization of BSPM machines using ``eMach``. By the end of this 
tutorial you will be able to:

* optmize BSPM designs for desired objectives
* post-proccess optimization archive data to understand design space and select candidate designs


Requirements 
---------------------

#. Python packages installed as discussed in :doc:`Pre-requisites <../../pre_reqs>`
#. Installation of JMAG v19 or above
#. Personal repo using ``eMach`` as submodule established (see :doc:`Rectangle Tutorial <../rectangle_tutorial/index>`)
#. :doc:`BSPM evaluation tutorial <../bspm_eval_tutorial/index>` completed


Step 1: Create BSPM ``Designer``
----------------------------------------------------------------------

In the root folder of your repository, create a Python file named ``ecce_2020_bspm.py``. The code required to create an example BSPM design will
reside within this file. Users can create this file by simply referring to the code snippets provided in :doc:`BSPM Machine <../../../machines/bspm/bspm_machine>`
and :doc:`BSPM Machine Operating Point <../../../machines/bspm/bspm_oper_pt>`. Readers can also refer to the ``ecce_2020_bspm.py`` file 
provided within ``mach_eval_examples/bspm_eval`` instead, although the structure of the ``import`` statements will be different.

Step 2: Create BSPM Optimization Design Space
--------------------------------------------------------------------

One of the major purposes of this tutorial is to showcase how multi-physics evaluations can be handled within ``eMach`` using the analyzers
provided by the repository. To demonstrate this, the structural, electromagnetic, and thermal performance of the example BSPM design created 


Simply merge all the ``AnalysisStep``s in the order in which they were defined above to create the ``Evaluator``. The code provided below
assumes each ``AnalysisStep`` was defined in a separate Python file / module. Readers are advised to name this file ``bspm_evaluator.py``.

.. code-block:: python

    from mach_eval import MachineEvaluator
    from structural_step import struct_step
    from electromagnetic_step import em_step
    from rotor_thermal_step import rotor_therm_step
    from stator_thermal_step import stator_therm_step
    from windage_loss_step import windage_step

    ############################ Create Evaluator ########################
    bspm_evaluator = MachineEvaluator(
        [
            struct_step,
            em_step,
            rotor_therm_step,
            stator_therm_step,
            windage_step,
        ]
    )

Step 3: Update ``mach_opt`` ``DataHandler`` (if required)
--------------------------------------------------------------------
	
To evaluate the BSPM machine created in step 1 at the defined operating point, we need to define a ``MachineDesign`` and pass it as an 
argument to the ``evaluate`` method of the ``bspm_evaluator`` created in the preceding step. The code below is provided in a manner such

.. note:: Getting the evaluator to work can be challenging as it involves the integration of multiple analyzers and ``mach_eval`` classes. 
    Reviewing the ``examples/mach_eval_examples/bspm_eval`` folder and running the  ``bspm_evaluator.py`` script herewith can help debug
    issues you may run into.


Step 4: Run Optimization
--------------------------------------------------------------------
	
To evaluate the BSPM machine created in step 1 at the defined operating point, we need to define a ``MachineDesign`` and pass it as an 
argument to the ``evaluate`` method of the ``bspm_evaluator`` created in the preceding step. The code below is provided in a manner such


Step 5: Process Optimization Archive
--------------------------------------------------------------------
	
To evaluate the BSPM machine created in step 1 at the defined operating point, we need to define a ``MachineDesign`` and pass it as an 
argument to the ``evaluate`` method of the ``bspm_evaluator`` created in the preceding step. The code below is provided in a manner such


Conclusion
----------------

Congratulations! You have successfully used ``eMach`` to create a digital BSPM design and a multi-physics BSPM evaluator as well! You can now
attempt evaluating other BSPM designs using this evaluator and see what results you end up with.

