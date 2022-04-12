Tutorials
==========================================

Users introduced to ``eMach`` for the first time can find it daunting to work with. The module has 3 sub-modules, each of which
can work as standalone modules by themselves or can be interfaced with one another to get a neat implementation of what the overarching
goal of the repository is -- electric machine optimization. 

The goal of the tutorials section is to help users understand the code base one layer at a time, and gradually move to problems of
increasing difficulty with each example.  First, tutorials for individual ``submodules`` are provided after which examples involving
interfaces between multiple ``eMach`` functions are discussed. At the end of each tutorial, users are expected to understand how
to use the different functionalities of ``eMach`` and understand what is happening under the hood to a certain extent as well.
All tutorials have been wrtting in a manner that assumes users treat the ``eMach`` repo as a Python package and ``import`` into 
their own custom scripts for using its functionalities.

+---------------+-----------------------------------+---------------------+
| eMach Module  | Tutorial Name                     | Goal                |
+===============+===================================+=====================+
| mach_cad      |                                   |                     |
+---------------+-----------------------------------+---------------------+
| mach_eval     | Analytical machine design tutorial|                     |
+---------------+-----------------------------------+---------------------+
| mach_opt      | Rectangle optimization            |                     |
+---------------+-----------------------------------+---------------------+


.. toctree::
    :hidden:

	draw_spm/index
    rect_opti/index
    toy_opti/index
	