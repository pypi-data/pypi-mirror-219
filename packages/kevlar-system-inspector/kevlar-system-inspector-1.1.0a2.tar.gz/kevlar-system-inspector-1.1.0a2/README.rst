.. image:: https://inspector.starlab.io/kevlar-system-inspector-logo.svg
   :align: center
   :width: 75%

======================================================================
Star Lab Kevlar System Inspector: A Security Scanner for Linux Systems
======================================================================

Kevlar System Inspector is an embedded security test suite that grew out of
`Star Lab's`_ extensive experience assessing and protecting mission-critical
systems for the U.S. Government.  These test have been made available for
public use to help identify security issues in a variety of Linux systems.  The
set of tests present in Kevlar System Inspector will be expanded as adversary
techniques and tactics change, and as we continue development of `Kevlar
Embedded Security`_.

These tests are generally more aggressive than other security scanning tools: We
prefer to probe behavior rather than check configurations values. However, we
do not include any actual exploit code or include any tests that could
destabilize the system. (And of course, we check configuration values too.)

.. _Star Lab's: https://www.starlab.io
.. _Kevlar Embedded Security: https://www.starlab.io/kevlar-embedded-security


System Requirements
===================

Kevlar System Inspector requires Python 3.8 or higher.

It is designed to be run in an embedded Linux test environment, but it is a
Python project that can run on most modern Linux distros, including desktop
distributions.


Installation
============

We provide several methods for installation:


Install from PyPI
-----------------

If your system is capable of installing packages from PyPI, Kevlar System
Inspector may be installed using ``pip``. Because Kevlar System Inspector is
designed to be run as root in a test environment, we suggest using ``pip`` to
install to a virtual environment. (Note that running as root is not required.)

.. code-block:: console

   $ python3 -m venv kevlar-venv
   $ ./kevlar-venv/bin/pip install kevlar-system-inspector
   $ sudo ./kevlar-venv/bin/kevlar-system-inspector

You can also install Kevlar System Inspector system wide:

.. code-block:: console

   $ sudo python3 -m pip install kevlar-system-inspector
   $ sudo kevlar-system-inspector


Standalone Tarball
------------------

For systems that cannot easily install from PyPI, we provide a `standalone
tarball`_ with all dependencies bundled into a single package. Once you have
copied this tarball to your device, you can simply extract and run:

.. code-block:: console

   $ tar xf ./kevlar-system-inspector-standalone.tar.gz
   $ sudo ./kevlar-system-inspector-standalone/kevlar-system-inspector

.. _standalone tarball: https://inspector.starlab.io/kevlar-system-inspector-standalone-v1.1.01a.tar.gz


Running as Root
===============

Although running as root is not necessary, Kevlar System Inspector is designed
to be run as root in a embedded test environment for two reasons:

* Some tests (for example, kernel module loading) require root permissions to
  perform.
* The Kevlar Embedded Security threat model is a defense in depth model that
  includes compromised root processes and malicious insiders.

Kevlar System Inspector does not include any malicious code or tests that would
destabilize the system. It uses root access to:

* Probe kernel features and configurations in different ways.
* Test the reaction of the system to (benign) files dropped in privileged
  locations.
* Inspect logical volume mangement configuration.


HTML Report Output
==================

Kevlar System Inspector may be run with the option
``--output-html=<filename.html>`` to produce a self-contained HTML report.


Uninstalling
============

If installed through ``pip``, Kevlar System Inspector may be uninstalled using
the command ``pip uninstall``. If it was installed in a virtual environment, or
if the standalone tarball version was used, simply deleting the directory
removes Kevlar System Inspector from the system. It does not permanently leave
files anywhere else on the system.
