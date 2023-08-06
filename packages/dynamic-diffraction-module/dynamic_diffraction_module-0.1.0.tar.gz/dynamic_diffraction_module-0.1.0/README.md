# Dynamic Diffraction Module

[![pypi](https://img.shields.io/pypi/v/dynamic-diffraction-module.svg)](https://pypi.org/project/dynamic-diffraction-module/)
[![python](https://img.shields.io/pypi/pyversions/dynamic-diffraction-module.svg)](https://pypi.org/project/dynamic-diffraction-module/)

A repository meant for (python based) functions on the dynamic diffraction theory. It is closely related to the Matlab written <https://gitlab.desy.de/patrick.rauer/MatlabDiffractionStuff>.
The structure, however, is based on the Dynamic Diffraction submodule of the [pXCP](https://gitlab.desy.de/patrick.rauer/Xgeno_mpi) framework.

* Documentation: <https://patrick.rauer.github.io/dynamic-diffraction-module>
* GitLab: <https://gitlab.desy.de/patrick.rauer/dynamic-diffraction-module>
* PyPI: <https://pypi.org/project/dynamic-diffraction-module/>

## Features

Currently, the scope of the package is rather rudimentary.
It includes:

* computing the (modified) Bragg energy for any given plane H for a specific micro- and macroscopic crystal orientation
* computing the (approximative) energy width for any given plane H for a specific micro- and macroscopic crystal orientation in the two beam approximation
* Selecting the number of reflecting planes in the vicinity of a given photon energy + crystal orientation configuration
* computing reflectivity/transmissivity vs energy for a specified crystal plane H0 can be computed in the two beam approximation
* Rocking curve scans in the two beam approximation

However, further functionality is to follow soon:

* n-beam diffraction
* diffraction at strained crystals
* ...

## External packages

* numpy (required)
* [xraylib](https://github.com/tschoonj/xraylib) (prospectively optional,currently required)
* matplotlib
* pandas

## Usage

There is no documentation for the API yet. However, you can find some tutorial *.ipynb scripts in the [playgrounds folder](playgrounds/README.md)

## LICENSE

* Free software: GNU GENERAL PUBLIC LICENSE Version 3

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.
