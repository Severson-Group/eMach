.. _rectangle_example:

Rectangle Tutorial 
==================
* **Goal:** Understand base ``mach_opt`` classes
* **Complexity** 2/5
* **Estimated Time** 20 min

This tutorial demonstrates how to run a simple optimization of a rectangle using ``eMach``. By the end of this tutorial you will:

* Understand the use/function of the core ``mach_opt`` classes.
* Be able to run simple optimizations using ``eMach``.

In this tutorial a rectangle will be optimized to maximize its area while minimizing its perimeter.

.. figure:: ./images/RectangleExample.svg
   :alt: Trial1 
   :align: center
   :width: 800 

Tutorial Requirements 
---------------------

This is the first tutorial so the only requirement is:

#. All required Python packages are installed on system

Step 1: Create new repository
------------------------------------------

First a personal repository for this tutorial will be created. Open a new empty folder and input the following code into git-bash to initialize the repository.

.. code-block:: 
	
	git init


Step 2: Clone eMach as a sub-module
------------------------------------------

In order to utilize the eMach codebase, it must first be installed as a sub-module in your repository. In the root folder of your repository open a git bash and input the following command line:

.. code-block:: 
	
	git submodule add https://github.com/Severson-Group/eMach.git

This should add the current develop branch of ``eMach`` as a folder in the base layer of your personal repository.

Step 3: Create main optimization file
------------------------------------------

In the root folder of your repository, create a python file named ``main.py``. All the code used in this example will be written in this file. At the top of ``main.py`` add the following import statements:

.. code-block:: python

	from matplotlib import pyplot as plt
	import pygmo as pg
	from eMach import mach_opt as mo

Step 4: Create Designer and Design classes
------------------------------------------

Copy the following code into your ``main.py`` file. These two classes fulfill the ``Designer`` and ``Design`` protocols specified in the ``mach_opt`` repository. This code will convert the free variable tuple ``x`` provided by ``pygmo`` into a ``Rectangle`` object to be evaluated.

.. code-block:: python

	class RectDesigner(mo.Designer):
		"""Class converts input tuple x into a Rectangle object"""
		
		def create_design(self,x:tuple)->"Rectangle":
			"""
			converts x tuple into a Rectangle object.

			Args:
				x (tuple): Input free variables.
				
			Returns:
				rect (Rectangle): Rectangle object
			"""
			
			L=x[0]
			W=x[1]
			rect=Rectangle(L,W)
			return rect
		
.. code-block:: python

	class Rectangle(mo.Design):
		"""Class defines a rectangle object of Length and width
		
		Attributes:
			L (float): Length of Rectangle.
			W (float): Width of Rectangle.
		"""
		
		def __init__(self,L:float,W:float):
			"""Creates Rectangle object.

			Args:
				L (float): Length of Rectangle
				W (float): Width of Rectangle

			"""
			self.L=L
			self.W=W
		
Step 5: Create Evaluator class
------------------------------------------

Copy the following code block into the ``main.py`` file. This code defines the ``Evaluator`` class which will be used to evaluate the rectangle for its Area and Perimeter.

.. code-block:: python

	class RectEval(mo.Evaluator):
		""""Class evaluates the rectangle object for area and perimeter"""
		
		def evaluate(self,rect):
			"""Evalute area and perimeter of rectangle

			Args:
				rect (Rectangle): Rectangle Object

			Returns:
				[A,Per] (List[float,float]): Area and Perimeter of rectangle

			"""
			A=rect.L*rect.W
			Per=2*rect.L+2*rect.W 
			return [A,Per]

Step 6: Create DesignSpace class
------------------------------------------

Once again copy the following code section into the ``main.py`` file. This code defines the ``DesignSpace`` class which will be utilize by the optimization. The ``DesignSpace`` protocol is responsible for converting information back into a form usable by ``pygmo``. The primary method on interest in this example is the ``get_objectives`` method. For this tutorial, the ``full_results`` object returned by the ``Evaluator`` class is a list of the area and perimeter of the rectangle. The goal of the optimization is to maximize the area and minimize the perimeter, however ``pygmo`` will always attempt to minimize the objective values. To circumvent this, the ``DesignSpace`` class returns a negative area.

.. code-block:: python

	class RectDesignSpace(mo.DesignSpace):
		"""Class defines objectives of rectangle optimization"""

		def __init__(self,bounds,n_obj):
			self._n_obj=n_obj
			self._bounds=bounds
			
		def get_objectives(self, valid_constraints, full_results) -> tuple:
			""" Calculates objectives from evaluation results
			

			Args:
				results (List(float,float)): Results from RectEval

			Returns:
				Tuple[float,float]: Maximize Area, Minimize Perimeter
			"""
			Area = full_results[0]
			Perimeter = full_results[1]
			return (-Area,Perimeter)
		
		def check_constraints(self, full_results) -> bool:
			return True
		
		@property
		def n_obj(self) -> int:
			return self._n_obj
		
		@property
		def bounds(self) -> tuple:
			return self._bounds
			
Step 7: Create dummy DataHandler class
------------------------------------------
for this example, we will not be implementing a ``DataHandler`` class to save the optimization results. However ``eMach`` still requires a class with the functions calls to be created. The following code block should be copied into ``main.py`` as a dummy ``DataHandler`` class.

.. code-block:: python

	class DataHandler:
		def save_to_archive(self, x, design, full_results, objs):
			"""dummy data handler"""
			pass
		def save_designer(self, designer):
			pass

Step 8: Initialize custom classes
------------------------------------------

Copy the following code into the bottom of ``main.py``. This code will create instances of the defined ``Designer``, ``Evaluator``, and ``DesignSpace`` classes from earlier steps. 

.. code-block:: python

	###############################
	### Create mach_opt objects ###
	###############################
	des=RectDesigner()
	evaluator=RectEval()
	dh=DataHandler()
	## Define optimization bounds and number of objectives
	bounds=([0,0],[1,1])
	n_obj=2
	## Inject bounds and number of objectives into DesignSpace
	ds=RectDesignSpace(bounds,n_obj)

Step 9: Inject custom classes into DesignProblem
------------------------------------------------

Copy the following code into the bottom of ``main.py``. In this step the instances of the the defined ``Designer``, ``Evaluator``, and ``DesignSpace`` classes are injected into the ``DesignProblem`` class of the ``mach_opt`` module. This class is designed to interface directly with ``pygmo`` optimization algorithms.

.. code-block:: python

	machDesProb=mo.DesignProblem(des,evaluator,ds,dh)

Step 10: Set up optimization code
------------------------------------------------

In ``mach_opt`` the ``DesignOptimizationMOEAD`` class is provided to run a MOEAD optimization problem. This class is simply a container for ``pygmo`` optimization code. Using the following code block, an optimization can be run using the user created ``DesignProblem`` object from the previous step.

.. code-block:: python

	opt=mo.DesignOptimizationMOEAD(machDesProb)
	pop_size=50
	pop=opt.initial_pop(pop_size)
	gen_size=10    
	pop=opt.run_optimization(pop,gen_size)

Step 11: Extracting and plotting results
------------------------------------------------

The following code block will extract results from the optimization and plot the Pareto front for this optimization. The ``pop.get_f()`` method returns a vector of the objective values for the optimization, while the ``pop.get_x()`` method returns the free variable tuples for the optimized population. 

.. code-block:: python

	fig1=plt.figure()   
	plot1=plt.axes()
	fig1.add_axes(plot1)
	fits, vectors = pop.get_f(), pop.get_x()
	ndf, dl, dc, ndr = pg.fast_non_dominated_sorting(fits) 
	plot1.plot(fits[ndf[0],0],fits[ndf[0],1],'x')
	plot1.set_xlabel('Area')
	plot1.set_ylabel('Perimeter')
	plot1.set_title('Pareto Front')
	
``pygmo`` provides a method to extract the Pareto in the method ``fast_non_dominated_sorting(fits)``, the returned ``ndf`` object is a list of the indexes for the Pareto fronts. If the code was correctly implemented, then the results of the optimization should look similar to the following plot.

.. figure:: ./images/Pareto.svg
   :alt: Trial1 
   :align: center
   :width: 600
	

Conclusion
----------

You have successfully completed your first optimization using ``eMach``. This code can be modified to perform other simple optimizations, the following list of optimizations can be created by simply modifying the provided code:

* Optimize a circle for maximum area and minimum perimeter
* Optimize a cuboid for maximum volume and minimum surface area
* Optimize a sphere for maximum volume and minimum surface area 
