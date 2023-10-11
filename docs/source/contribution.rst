
*eMach* Contribution Guidelines
==========================================

This guide is intended to provide guidelines for contributors to *eMach*. All contributors are expected to follow these 
guidelines with exceptions allowed only in cases as specified within the references. 

Code Style
-------------------------------------------

Using a consistent writing style makes shared code more maintainable, useful, and understandable. Contributors to *MachEval*
should follow the `Google Python Style Guidelines for naming <https://google.github.io/styleguide/pyguide.html#s3.16-naming>`_ 
and code documentation. More information on code documentation will be provided in a later section.

A brief summary of guidelines for names in Python includes:

* Avoid using excessively short names: instead, favor full words to convey meaning
* File, function, and variable names: lowercase with words separated by underscores as necessary to improve readability
* Class names: start upper case and then move to camel case
* Keep in mind that certain characters add special functionality: for instance, prepending class methods and variable names with double underscore (__) make them private to that class

Naming guidelines derived from PEP 8, used in the Google format as well, are provided below:

.. figure:: images/pep8.PNG
   :alt: Trial1 
   :align: center
   :scale: 80 %
   

Docstrings in Python
--------------------------------------------

A Python docstring is a string literal that occurs as the first statement in a module, function, class, or method definition.
Such a docstring becomes the __doc__ special attribute of that object which can be easily accessed outside the module, 
greatly improving code readability, especially in projects like *MachEval* with multiple module interdependencies.

For the purposes of *MachEval*, contriubutors are expected to follow the `Google Comments and Docstrings guidelines for code
documentation <https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings>`_. A general guideline which 
helps in greatly improving the usefulness of code documentation is to ensure that docstrings are provided for functions / 
methods and give enough information for users to write a call to any function without having to read the function’s code.

In addition to the benefits mentioned above, the Google docstrings format is also compatible with the Python Documentation 
Generator tool `Sphinx <https://www.sphinx-doc.org/en/master/>`_. As a result, maintaining the above suggested format also 
results directly in the automatic creation of pretty, well indexed documentation of the code base. These documents can be 
hosted online on the Read the Docs platform which supports real-time document updation, or on Github pages via HTML files. It 
should be noted that free document hosting with Read the Docs is supported only for public Git repositories.


Git/GitHub Usage
-------------------------------------------

All code development should occur within the Git version control environment. When code is ready to be contributed back 
to eMach, users should open a Pull Request (PR) on GitHub which explains their contribution.

The branch naming conventions are as follows:

- **User branch:** ``user/my_user_name/foo_bar`` -- "private" development sandbox per user
- **Feature branch:** ``feature/foo_bar`` -- shared feature development

**Hint:** Most development will occur in user branches! If multiple users are working on an eMach feature concurrently, use a feature branch.

Contributors can expect that their user branches will not be commited to by other users---this is "private" space. On the other hand,
feature branches are "public" space and should be treated as such---at any time, another developer can commit new code onto the branch.

For example, if a big feature is being developed by several developers, a common feature branch will be created. Then, developers can
branch from this common feature branch to their own private user branch. Once they are ready to share their code back with the other
developers of the new feature, they can open a PR (or simply merge) their user branch back to the feature branch.

Valid branch name examples: ``user/johndoe/motor_tests``, ``user/janestil2/issue_652``, ``feature/regression_tests``, ``feature/tutorial_femm``

Reviewer Checklists
-------------------------------------------

All PRs on GitHub must be reviewed by multiple separate parties prior to being integrated into the mainn ``develop`` branch of ``eMach``. A 
minimum of two reviews are required, with more being preferred. When making a PR, the contributor must request a Level 1 and Level 2 reviewer,
whose responsibilities for reviewing can be seen in the following subsections.

Level 1 Review Requirements
++++++++++++++++++++++++++++++++++++++++++++

A Level 1 reviewer should be someone with a minimal-to-adequate understanding of the review material. This reviewer must accomplish the
following tasks:

1. Pull/fetch the branch being reviewed onto their device
2. Verify code works
3. Edit language of the documentation if necessary
4. Ensure proper python coding practices
5. Add a preliminary review of eMach architecture and subject matter
6. Request changes/give approval to pass to a Level 2 reviewer

Level 1 reviewers as of 10/10/2023: Dante Newman, Anson Chan, Takahiro Noguchi

Level 2 Review Requirements
++++++++++++++++++++++++++++++++++++++++++++

A Level 2 reviewer should be someone with a adequte-to-expert understanding of the review material. This reviewer must accomplish the
following tasks:

1. Pull/fetch the branch being reviewed onto their device
2. Ensure code displays expected result
3. Add an in depth review on eMach architecture and subject matter
4. Request changes/give final approval for merge into ``develop``

Level 2 reviewers as of 10/10/2023: Nathan Petersen, Anvar Khamitov, Eric Severson

Documentation
-------------------------------------------

The ``eMach`` repository uses both ``Sphinx`` and ``Read the Docs`` for generating and hosting documentation online. The link to 
this documentation is provided `here <https://emach.readthedocs.io/en/latest/>`_. This section provides guidelines on practices
contributors are expected to follow to make edits / add to ``eMach`` documentation.

How it Works
++++++++++++++++++++++++++++++++++++++++++++

All of ``eMach``'s documentation resides within the ``docs\source`` folder. This folder contains all the information required by 
``Sphinx`` to generate HTML files in the manner we desire. The workflow currently used in ``eMach`` off-loads the actual generation
of the HTML to the ``Read the Docs`` platform. Contributors, therefore, need to only make changes to the files within the 
``docs\source`` folder and ``Read the Docs`` will take care of actually running ``Sphinx`` and generating the HTML files. A push to the 
``develop`` branch acts as a trigger for ``Read the Docs`` to re-generate HTML files. Therefore, the onus falls on contributors to
ensure everything is in order, documentation wise, prior to merging changes to ``develop``.

Recommended Workflow
++++++++++++++++++++++++++++++++++++++++++++

For small changes involving just edits to exisiting documents and such, contributors can simply push the edits directly to ``develop``. 
For more involved changes, such as adding figures or entirely new files, it is recommended that contributors ensure everything looks
as expected locally before attempting to merge changes. The steps involved in generating HTML files locally are as follows:

1. Ensure the required Python packages are installed (they will be if you followed the pre-reqs document)
2. Navigate to the ``eMach\docs`` folder from within ``Anaconda Prompt``
3. Ensure the ``eMach`` environment is activated (run ``conda activate eMach`` if not certain)
4. Run ``make clean`` followed by ``make html`` command to generate the docs
5. Open up the ``index.html`` file from within ``docs\build\html`` folder and make sure everything is in order

``eMach`` also supports ``Sphinx`` autodocs feature, by which ``Sphinx`` is able to automatically generate documentation
from Python docstrings. Modifications to exisiting Python files will be reflected on ``Read the Docs`` by default. However, if new 
Python files whose docstrings should be included on ``Read the Docs`` are created, contributors will have to run a sequence of 
commands to create the .rst files required to autogenerate the Python docstring HTML file, or manually create / make modifications to 
exisitng .rst files themselves. For more information, please refer to this `link <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`__.
