
Pre-requisites
============================================

This document goes through the pre-requisites required for using ``eMach`` and also guides users on setting up their systems to get
started. 

Python
---------------------------------------------

The first, and perhaps most obvious, requirement is for users to install Python on their systems. Version upwards of Python 3.8
are required for ``eMach``. Furthermore, it is highly recommended that users install Python via `Anaconda <https://www.anaconda.com/products/individual>`_ 
or `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ as the conda package manager is required in subsequent steps for
installing ``eMach`` dependencies. In general, new users of Python are recommended to install ``Anaconda`` as it comes with adittional
auxillary packages, the Spyder IDE (integrated development environment), Jupyter, and other features which make it very easy to get 
started with Python out of the box. Users who are comfortable with Python, know exactly which IDE they want to use, and wish to 
selectively install only the packages they require can go with the ``Miniconda`` installation. This `link 
<https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html#anaconda-or-miniconda>`_ succintly summarizes when
either installer should be used.

After installing Python, please ensure that paths to the Python and conda installations are included in the ``Path`` ``User 
Variables`` (for Windows systems). This is required for your system to know how to run Python scripts, find relavent Python packages, 
run ``conda`` commands etc. To verify this, 

1. Search ``environment variables`` in the Windows search bar.
2. Select ``Edit the system environment variables``.
3. Now click on the ``Environment Variables...`` button from the ``System Properties`` window
4. Within ``User Variables``, double click on ``Path``.
5. A list of directories should now be visible, among which the directories where the newly install ``python.exe`` and
   ``conda.exe`` files reside should be included. It will most likely be in the folder ``C:\Users\YourName\anaconda3`` and 
   ``C:\Users\YourName\anaconda3\Scripts`` respectively.
6. If the directories are not included, manually add them by clicking the ``New`` button and adding the above mentioned 
   installation paths to the ``Path`` ``User Variable``.

.. warning:: Be very careful when modifying ``Environment Variables``. Inadvertent modifications can potentially 
   destroy your system.
   

IDEs for Python
----------------------------------------------

There are a large number of IDEs available out there for Python. Spyder, which comes along with the ``Anaconda`` installation,
is most likely the path of least resistance for new users looking to quickly get started with Python. Spyder is however limited in 
a lot of ways, its biggest disadvantage being the lack of flexibility to switch between different Python interpreters (versions) 
and virtual environments. More information on Python virtual environments is provided below. Beginners will most likely not be 
employing these features of Python anytime soon and therefore can continue with Spyder. 

Other, more flexible IDEs for Python include `Visual Studio Code <https://code.visualstudio.com/>`_ and `PyCharm 
<https://www.jetbrains.com/help/pycharm/installation-guide.html>`_. These IDEs have a lot of additional features, including syntax 
highlighting, auto-formatting, debugging capabilities, git integration, seamless transfer between virtual environments etc. However, 
there is definitely a learning curve associated with these platforms.

.. note:: It is recommended that users switch to VS Code or PyCharm as soon as they are comfortable with Python as these IDEs 
   enable much improved workflows.


Packages
------------------------------------------------

The final step involved before one can beging using ``eMach`` is to install the Python packages employed by the module. Prior to 
this stage, users should clone the ``eMach`` git repository to their local system. A ``environment.yml`` file has been provided at 
the root directory of the repo. This file enables the re-creation of a Python conda environment which has been proven to work with 
``eMach``. Users are recommended to open this file and briefly glance through it to get an idea of the additional packages required
for ``eMach`` apart from what comes standard with Python. 

The below steps are provided for users looking to add packages to their global Python installation in Windows.

1. Launch Windows ``Command Prompt`` 
2. Navigate to the location of the ``environment.yml`` file within ``Command Prompt`` 
3. Run the following command : ``conda env update --name base --file environment.yml --prune``
4. Wait for the packages to install, enter ``y`` if required
5. Run the ``rectangle_example.py`` file from ``examples//mach_opt_examples`` to confirm everything is in order 

.. warning:: ``Anaconda`` comes with a **large** Python ``base``. Updating such environments can take a very long time. If you are 
   running into this issue, consider installing each package individually using ``conda install``. 

Alternatively, each package provided in the ``environment.yml`` can be installed individually. The steps for doing so are,

1. Launch Windows ``Command Prompt`` 
2. Begin installing the ``pygmo`` package by running ``conda install -c conda-forge pygmo=2.18.0``
3. Try running the ``rectangle_example.py`` script from ``examples//mach_opt_examples`` folder
4. Run ``conda install pkg_name`` on the missing packages, if there are any

Congratulations! You have successfully completed all installations required to start using ``eMach``. You can now try running other 
examples provided within the ``examples`` folder to confirm everything is working as expected.


Using Conda Environments with eMach (Optional)
----------------------------------------------------

This optional section has been added for users who wish to be more "Python savvy". This section gives an overview of Python virtual
environments and provides necessary links to enable users to work with virtual environments using VS code.
 
Virtual environments are isolated environments for Python projects. These environments become extremely useful when users start 
dealing with multiple Python projects, each of which might have different, and at times, confilcting dependencies. For eg: if one 
project requires ``numpy=0.13`` whereas another requires ``numpy=1.22``, we would have to re-install the desired version of ``numpy`` 
each time we switch between projects. Python overcomes this problem quite elegantly with virtual environments. By using different 
environments for different projects, users can not only change the packages used, but can even change the very version of Python 
employed between projects. This `link <https://realpython.com/python-virtual-environments-a-primer/>`_ provides a more in-depth 
exaplaination of Python virtual environments. 

Harnessing the power of virtual environments can be very cumbersome with the defualt ``Anaconda`` IDE Spyder. As a result, while 
virtual environments themselves are IDE agnostic, using IDEs such as Visual Studio Code or PyCharm makes it far easier to 
leverage their potential than using others. This `video <https://www.youtube.com/watch?v=-nh9rCzPJ20>`_ provides a great, easy to 
understand, step-by-step guide of using VS Code with Python. After following this tutorial, you should be able to:

1. Run Python scripts on VS Code
2. Create virtual environments in Python using the standard ``venv`` module
3. Easily switch between different virtual environments from within VS Code

Finally, coming back to ``eMach`` and employing virtual environments with ``eMach``. As mentioned previously, the root directory
of the repository holds a ``environment.yml`` file. The primary purpose of this file is to enable users create identical conda 
environments across different systems to rule out potential run-time errors due to differences in package dependecies or Python
versions. The steps involved in creating a new ``eMach`` conda environment using the ``environment.yml`` file are provided below:

1. Open the ``environment.yml`` and uncomment the ``- python=3.8`` line
2. Launch Windows ``Command Prompt`` 
3. Navigate to the location of the ``environment.yml`` file within ``Command Prompt`` 
4. Run command ``conda env create -f environment.yml``
5. Wait for the packages to install, enter `y` wherever required

Congratulations! You have successfully created a new conda environment for ``eMach`` that houses all the required packages. Please 
switch to the new environment, and try running one among the many examples provided within the ``examples`` folder to confirm 
everything is working as expected.

.. tip:: When using virtual environments, it is always a good idea to confirm which paths your scripts are looking at to run Python
   and access packages. This can be done by importing the ``sys`` package and running ``print(sys.path)``. Make sure that all paths 
   agree with your expectations based on the location of your virtual environment.
