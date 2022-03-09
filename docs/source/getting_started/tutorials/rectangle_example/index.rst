.. _rectangle_example:

Rectangle Example
=================

This example demonstrates how the ``des_opt`` module can be used to preform a simple optimization of a rectangle. The goal of this optimization is to maximize the area while minimizing the perimeter. Although this example is extremely simple and can be solved analytically, it allows for the primary protocols and classes of the the ``des_opt`` module to be demonstrated and the flow of information between classes to be easily visualized.

.. figure:: /images/RectangleExample.png
   :alt: Trial1 
   :align: center
   :width: 800 

The implementation of the following protocols will be discussed in this document:

Designer
	The ``Designer`` protocol converts an input tuple into a ``design`` object.
Evaluator
	The ``Evaluator`` evaluates the ``design`` object for a set of criteria defined in the ``evaluate`` function
DesignSpace
	The ``DesignSpace`` handles converting the results of the evaluation into the objective variables.
	
The final protocol of the ``des_opt`` modules, the ``DataHandler`` is not implemented for this example. The general flow of information in the ``des_opt`` module is shown in the following flow chart. The optimization algorithm will pass a set a free variables to the ``DesignProblem`` object, which in turn will be provided to the ``Designer``. The ``Designer`` will convert the free variables into a ``design`` object which is then passed to the ``Evaluator``. The ``Evaluator`` is responsible for evaluating the ``design`` object. The results of the evaluation, are then handed to the ``DesignSpace`` which converts the results of the evaluation into objective values in a form that the optimization algorithm can handle.

.. figure:: /images/DesOptlFlowChart.svg
   :alt: Trial1 
   :align: center
   :width: 300
   
des_opt Protocols
----------------- 
	
Designer
~~~~~~~~

The ``Designer`` class of ``des_opt`` is implemented here by the ``RectDesigner`` class. Again this protocol is used to define the conversion of the free variable tuple ``x`` into a ``design`` object. In this example the ``design`` object is replaced by the ``Rectangle`` object, and is used to store the information of the design. The following code block demonstrates how the ``RectDesigner`` class implements the required ``create_design`` function of the ``Designer`` class.

.. code-block:: python

	class RectDesigner(do.Designer):
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


The details of the ``Rectangle`` object, which is an extension of the empty ``Design`` class are shown in the following snip it. In this example the design object is extremely simple, as we are only modeling a rectangle, however for more complex design optimization it is useful to have this object as a single source of truth for details of the design.

.. code-block:: python

	class Rectangle(do.Design):
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

Evaluator
~~~~~~~~~

The ``Evaluator`` protocol is implemented in this example by the ``RectEval`` class. This object has an ``evaluate`` function which takes in a ``Rectangle`` object and returns the Area and Perimeter as a list. 

.. code-block:: python

	class RectEval(do.Evaluator):
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
		
Again this example is extremely simple, however it demonstrates how the ``design`` object from the ``Designer`` interacts with the ``evaluate`` function of the ``Evaluator``. The ``Evaluator`` must be able to return the results of an evaluation using only the information contained in the ``design`` object or information which is supplied during initialization. 

DesignSpace
~~~~~~~~~~~
The ``DesignSpace`` protocol is implemented by the ``RectDesignSpace`` class. This class handles the exchange of information between the optimization algorithm and the rest of the ``des_opt`` module. In order to fulfill the ``DesignSpace`` protocol contract four functions must be implemented: ``get_objectives``, ``check_constraints``, ``n_obj``,and ``bounds``. 

The ``get_objectives`` function is responsible for converting the results of the ``Evaluator`` into a tuple of objective values which can be used by the optimization algorithm. The ``check_constraints`` function is not utilized in this example, however it can be used to perform any final constraint checks on the results of the evaluation. The ``n_obj`` and ``bounds`` functions are implemented as properties and return the number of objectives and bounds of the free variables respectively. These functions are required by ``Pygmo``. 


.. code-block:: python

	class RectDesignSpace(do.DesignSpace):
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
			return (-full_results[0],full_results[1])
		
		def check_constraints(self, full_results) -> bool:
			return True
		
		@property
		def n_obj(self) -> int:
			return self._n_obj
		
		@property
		def bounds(self) -> tuple:
			return self._bounds

The ``get_objectives`` function takes the results from the evaluator as the ``full_results`` object, and parses out the objective functions. In this example, the objective functions are simply to maximize the area, and to minimize the perimeter. These values are stored as the first and second entry in the ``full_results`` list from the evaluator. The optimization algorithm expects that the objective values be returned as a ordered tuple, of values to minimize. For this reason, a negative sign is added to the front of the area value from ``full_results`` which will cause the algorithm to find the largest negative number (i.e. -1<-.1) effectively converting the problem to maximize the area.
DesignProblem
-------------

The ``DesignProblem`` class of the ``des_opt`` module, is a concrete class in which the custom implementations of the protocols described above are injected into in order to utilize the optimization framework. The following code snip it demonstrates how the rectangle optimization is performed once the required protocols are implemented

.. code-block:: python

    des=RectDesigner()
    evaluator=RectEval()
    dh=DataHandler()
    bounds=([0,0],[1,1])
    n_obj=2
    ds=RectDesignSpace(bounds,n_obj)
    machDesProb=do.DesignProblem(des,evaluator,ds,dh)
	
The ``DesignProblem`` object can the be utilized by a ``Pygmo`` optimization. The code to perform a MOEAD optimization in ``Pygmo``  has been implemented by the ``DesignOptimizationMOEAD`` class of ``des_opt``. This class takes in the ``machDesProb`` and is then used to perform the optimization. As long as the required protocol functions are correctly implemented by the injected ``machDesProb``, then the optimization class will be able to successfully optimize the problem.

.. code-block:: python
	
	opt=do.DesignOptimizationMOEAD(machDesProb)
    pop_size=50
    pop=opt.initial_pop(pop_size)
    gen_size=10    
    pop=opt.run_optimization(pop,gen_size)

The resulting Pareto plot of this optimization is shown here. Note that area is plotted as a negative value, this is due to the fact the objective is to maximize area, but the optimization software is designed to minimize.

.. figure:: /images/Pareto.svg
   :alt: Trial1 
   :align: center
   :width: 600
