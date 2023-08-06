.. image:: https://github.com/jlvdb/yet_another_wizz/blob/main/docs/source/_static/logo-dark.png?raw=true
    :width: 1000
    :alt: yet_another_wizz

|

.. image:: https://img.shields.io/pypi/v/yet_another_wizz_cli?logo=pypi&logoColor=blue
    :target: https://pypi.org/project/yet_another_wizz_cli/
.. image:: https://github.com/jlvdb/yet_another_wizz_cli/actions/workflows/run-tests.yml/badge.svg
    :target: https://github.com/jlvdb/yet_another_wizz_cli/actions/workflows/run-tests.yml
.. image:: https://codecov.io/gh/jlvdb/yet_another_wizz_cli/branch/main/graph/badge.svg?token=PC41ME2AR8
    :target: https://codecov.io/gh/jlvdb/yet_another_wizz_cli
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/


Commandline tool
================

*yet_another_wizz_cli* implements a command line interface for the clustering
redshift code `yet_another_wizz <https://github.com/jlvdb/yet_another_wizz>`_:

- code: https://github.com/jlvdb/yet_another_wizz_cli.git
- PyPI: https://pypi.org/project/yet_another_wizz_cli/

The documentation of this commandline tool is part of the official documentation
of *yet_another_wizz* itself, including some usage examples:

- docs: https://yet-another-wizz.readthedocs.io/

Refer especially to the sections **User guide / Usage examples** and
**User guide / Command line tools**.

.. Note::
    When using this code in published work, please cite
    *van den Busch et al. (2020), A&A 642, A200*
    (`arXiv:2007.01846 <https://arxiv.org/abs/2007.01846>`_)


Installation
------------

The *yet_another_wizz* package can be installed directly with pip::

    pip install yet_another_wizz_cli

This will install the python package ``yaw`` as dependency, as well as the
``yaw_cli`` executable command line tool that is shipped with this package.


Usage
-----

After installation, the command line tool can be invoked by typing ``yaw_cli```
on the terminal. The tool is organised into a number subcommands that each
serve a specific purpose. To obtain an overview over the available options,
type::

    $ yaw_cli --help

Each subcommand operates on a single output directly, which organises all
intermediate and output data products for easy access, as well as logging and
a summary of the operations performed in a single YAML configuration file.

The most important subcommand is ``yaw_cli run``, which computes clustering
redshifts from such a YAML configuration file. A template for the configuration
file can be printed to the terminal using::

    $ yaw_cli run --dump

For more details refer to the to *User guide / Command line tools* section in
the documentation of *yet_another_wizz*.

Example
~~~~~~~

An example of the extended logging messages generated when running
``yaw_cli run``:

.. image:: https://raw.githubusercontent.com/jlvdb/asciinema_editor/main/examples/yaw_cli_small.gif
    :width: 800
    :alt: yet_another_wizz_cli example run

The automatically generated check plots of the clustering redshift estimates:

.. image:: https://raw.githubusercontent.com/jlvdb/yet_another_wizz_cli/main/data/nz_estimate.png
    :width: 800
    :alt: yet_another_wizz_cli example output


Reporting bugs and requesting features
--------------------------------------

For bug reports or requesting new features, please use the github issue page:

https://github.com/jlvdb/yet_another_wizz_cli/issues


**Maintainers:**

- Jan Luca van den Busch
  (*author*, Ruhr-Universität Bochum, Astronomisches Institut)


Acknowledgements
----------------

Jan Luca van den Busch acknowledges support from the European Research Council
under grant numbers 770935. The authors also thank Hendrik Hildebrandt,
Benjamin Joachimi, Angus H. Wright, and Chris Blake for vital feedback and
support throughout the development of this software.
