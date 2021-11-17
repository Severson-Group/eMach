.. _rectangle_example:

Rectangle Example
=================

This example demonstrates how the ``des_opt`` module can be used to preform a simple optimization of a rectangle. The goal of this optimization is to maximize the area while minimizing the perimeter. 

.. figure:: /images/RectangleExample/RectangleExample.png
   :alt: Trial1 
   :align: center
   :width: 800 

This document will highlight how each of the ``des_opt`` protocols is implemented for this simple example.

Designer
--------

The ``Designer`` class of ``des_opt`` is implemented here by the ``RectDesigner`` class.

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


The ``RectDesigner`` implements the required ``create_design`` function to return a ``rect`` object. This object is a container for the information of the rectangle to be evaluated as is defined here:

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
---------

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

Optimization
------------
The ``Optimization`` protocol is implemented by the ``RectOpt`` class. This class takes in the results from the ``RectEval`` evaluation and returns them as a tuple of objectives: Maximize area, and minimizing perimeter.


.. code-block:: python

	class RectOpt(do.Optimization):
		"""Class defines objectives of rectangle optimization"""

		def getObjectives(self,results:"List[float,float]"):
			""" Calculates objectives from evaluation results
			
			Args:
				results (List(float,float)): Results from RectEval
			Returns:
				Tuple[float,float]: Maximize Area, Minimize Perimeter
			"""
			return (-results[0],results[1])
