Linear Superbubble Detector
===========================

.. image:: https://raw.githubusercontent.com/Fabianexe/Superbubble/master/logo.png

Introduction
------------
This project gives the reference implementation of the Linear Superbubble Dector (LSD).

.. _`NetworkX`: https://networkx.github.io
.. _`NetworkX can load`: https://networkx.github.io/documentation/stable/reference/readwrite/index.html

Features
--------
- Detect superbubbles in linear time
- Uses `NetworkX`_  as graph library
- Can load plenty file formats (everything that `NetworkX can load`_ )
- Have different ways to report the superbubbles
- Simple and clean code
- Simple to understand and reimplement

Documentation
=============
The documentation can be found at:
https://fabianexe.github.io/Superbubble

Installation
------------
The simples way to install is using pip::

   pip install LSD-Bubble

.. _`setuptools`: https://pypi.python.org/pypi/setuptools

You can also download the source from https://github.com/Fabianexe/Superbubble and run the make script to install the package.
These needs that `setuptools`_ are installed.

Usage
-----
The programms needs only a path to a graph file to work:

   lsd *path*

If as input format not edgelist is used give the format with the -f parameter

   lsd *path* -f gml

If you want a different reporting format use -r

   lsd *path* -r count

If you want not to detect superbubbles but week superbubbles use --week:

   lsd *path* --week
