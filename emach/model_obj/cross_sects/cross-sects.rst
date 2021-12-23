Specifications for ``Crosssect`` class implementation
==========================================================

The ``Crosssect`` class implements cross-sections of standard geometry shapes that are commonly encountered in electric machine 
design. This document specifies the rules to be followed to add a new cross-section to eMach.


Creating a new cross-section
----------------------------------------------------------

Although eMach currently supports several cross-sections and can draw most common geometries, there can be occassional need to 
add new cross-sections. The following guidelines must be adhered to when adding a new cross-section:

- **Naming:** The name of the cross-section should be self descriptive and always begin with ``CrossSect``. The name should 
  start with upper case and move to camel case. Eg: ``CrossSectOuterRotor``.
- **Function description:** A short one line description should be provided at the beginning of the function to describe the 
  cross-section being implemented.
- **Variable names:** Clear and self-descriptive variable names should be chosen for the input dimensions to the function. The 
  variable names should be abbreviated and use ``_`` to denote subscripts. For example, designate a variable that denotes the 
  stator yoke thickness as ``t_sy`` rather than ``t_syoke`` or ``t_statoryoke``. 
- **Drawings:** A vectorized (``.svg``) drawing of the geometry should be provided. This drawing should clearly indicate the 
  location of the origin and coordinate axes. More details are provided `below <#Drawings>`_

Location and expected content
----------------------------------------------------------

When adding a new cross-section, a new folder must be created in `<eMach/model_obj/crosssects(./)>`. 
The folder specifications are as follows:

- **Folder Name:** The folder name should be same as the cross-section name without the ``CrossSect`` prefix, and must follow 
  camel case. For example, ``CrossSectOuterRotor`` will be in a folder named ``outerRotor``.
- **Folder Content:** The folder should contain the following files:

  - The __init__.py file containing the cross-section class.
  - A vectorized drawing of the cross-section in ``.svg`` format. The drawing filename should be identical to the cross-section 
    class name.
  - Source code used to create the drawings if not directly created from an ``.svg`` editor (i.e., if created using TikZ, Python,
    etc).
  - ``README.md`` file that has a header of ``[class name] Cross Section`` and renders the image (to facilitate browsing the 
    repository through GitHub)

Drawings
----------------------------------------------------------

Clear drawings are essential for the end user to understand how to use the cross-sections. The following guidelines must be 
adhered to:

- **Dimension names:** 

  - All dimensions that the function takes as an input should be indicated in the drawings. 
  - The dimension names should be the same as the variable names in the function.
  - Italicized ``Times New Roman`` font should be used.
  - Variable names containing an ``_`` character should be rendered with all text following the ``_`` as a subscript.
  - Greek characters should be used where appropriate. For example, an angular dimension maybe called ``alpha_m`` in the function. 
    However, it should be denoted as <img src="https://latex.codecogs.com/gif.latex?\alpha_\text{m}" title="\alpha_m" /> in the drawing.
  - Occassionally, some cross-sections may have variables that aren't dimensions. For example, the ``innerNotchedRotor`` has ``p`` 
    (number of pole pairs) as a variable. Such variables should also be indicated in the drawing.

- **Coordinate Axes:** The drawing origin and the coordinate axes should be clearly indicated in the drawing using a red 
  coordinate system indicating the positive ``x`` and ``y`` directions. The origin of the coordinate system is the origin of the drawing, as interpretted by the cross-section class.

As an example, the ``CrossSectTrapezoid.svg`` file is shown below:


.. figure:: trapezoid/CrossSectTrapezoid.svg
   :alt: TrapezoidCross 
   :align: center
   :scale: 50 %
   