===========
idem-random
===========

.. image:: https://img.shields.io/badge/made%20with-pop-teal
   :alt: Made with pop, a Python implementation of Plugin Oriented Programming
   :target: https://pop.readthedocs.io/

.. image:: https://img.shields.io/badge/made%20with-python-yellow
   :alt: Made with Python
   :target: https://www.python.org/


An Idem plugin that provides randomness.

About
=====
Idem Random provides us with logical states like random password,
random integer, random string which can be used in conjunction with
other idem plugins. This plugin in itself doesn't interact with the
any cloud provider.

An example use-case where this plugin can be used is -
AWS RDS database instance needs a password when its created.
We can use AWS's RDS state along with Idem random password state
in order to generate a random password at runtime and help create
the RDS instance.


Random ID
------------
The resource random_id generates random numbers that are intended to be used as unique identifiers for other resources.
This resource does use a cryptographic random number generator in order to minimize the chance of collisions, making the
results of this resource when a 16-byte identifier is requested of equivalent uniqueness to a type-4 UUID.

What is POP?
------------

This project is built with `pop <https://pop.readthedocs.io/>`__, a Python-based
implementation of *Plugin Oriented Programming (POP)*. POP seeks to bring
together concepts and wisdom from the history of computing in new ways to solve
modern computing problems.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`__
* `pop-awesome <https://gitlab.com/saltstack/pop/pop-awesome>`__
* `pop-create <https://gitlab.com/saltstack/pop/pop-create/>`__

Getting Started
===============

Prerequisites
-------------

* Python 3.6+
* git *(if installing from source, or contributing to the project)*

Installation
------------

.. note::

   If wanting to contribute to the project, and setup your local development
   environment, see the ``CONTRIBUTING.rst`` document in the source repository
   for this project.

If wanting to use ``idem-random``, you can do so by either
installing from PyPI or from source.

Install from PyPI
+++++++++++++++++

If package is available via PyPI, include the directions.

.. code-block:: bash

    pip install idem-random

Install from source
+++++++++++++++++++

.. code-block:: bash

   # clone repo
   git clone git@gitlab.com/vmware/idem/idem-random.git
   cd idem-random

   # Setup venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .

Roadmap
=======

Reference the `open issues <https://gitlab.com/vmware/idem/idem-random/issues>`__ for a list of
proposed features (and known issues).

Acknowledgements
================

* `Img Shields <https://shields.io>`__ for making repository badges easy.
