
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23264745.svg)](https://doi.org/10.5281/zenodo.23264745)
![PyPI License](https://img.shields.io/pypi/l/pytheas_simulator)
![GitHub last commit](https://img.shields.io/github/last-commit/mtomasini/PytheasSimulator)

# Pytheas Simulator - a flexible and agile simulator of ancient seafaring

Current research in the [Maritime Encounters project](https://www.gu.se/en/research/maritime-encounters), at the University of Gothenburg, has been led by using and developing the software [Voyager](https://github.com/mtomasini/voyager). While this software is very complete and thorough, it can be difficult to maintain and develop due to the many components that it uses. I decided to write a version of the code that is more flexible and less complex to use, based on my own experiences in simulating seafaring in ancient times. This software is an improvement on the work by Alvaro Montenegro (Ohio State University) and Victor Wåhlstrand Skärström (University of Gothenburg, now at Chalmers University of Technology). The code is written in Python.

The package is now available on PyPI and can be installed via

```bash
python -m pip install pytheas_simulator
```

## Tutorial

To use the tutorial on this repository (in the folder `./tutorial/`), it will be enough to install `pyhteas_simulator`, after downloading this repository on your computer. When installing the package, all the dependencies will be downloaded along with it. You can easily set up an environment using your favorite virtual environment manager, e.g.

```bash
mamba create -n pytheasenvironment python==3.14 
mamba activate pytheasenvironment
python -m pip install pytheas_simulator
```

and all should be ready to go. I wrote two types of tutorial: 
- `./tutorial/vignette.ipynb`: a Jupyter notebook explaining step by step how to build a simulation
- `./tutorial/simulation.py` : a script showing how to launch a larger simulation with multiple dates

For the tutorial I made available data from the Copernicus Data Center, using July 1996 as an example. Additionally I made available scripts (`/.tutorial/data/import_currents-waves.py` and `/.tutorial/data/import_winds.py`) so that you can download data directly on your computer from Copernicus (you will need a login for this, please see the tutorial notebook, or find information on Copernicus website directly). 

## Development philosophy

The code for Voyager was documented but had no tests. In the development of this new software, it is my intention to have even better documentation as well as unit testing. This follows from years of working in an academic context where tests are an afterthought and are seldom developed. But when using a software developed over years, by developers who have since quit the workplace, and that has required quick developments to respond to publication deadlines, the lack of testing in particular has proven deleterious, leading to bad mistakes at the production stage.

## Name of the software

I decided to name this new iteration of the Voyager software "Pytheas". As a software engineer, this is of course a (bad) pun on the fact that the software was developed in Python. But as an archaeologist, Pytheas was an ancient Greek navigator from Massalia (modern Marseille) who in around 330 BCE went on a sailing travel to the far North of Europe, reaching the British Isles and travelling further north to _Ultima Thule_ (which may be, according to Barry Cunliffe[^1], most probably Iceland, but possibly Norway or Shetland). Pytheas' travel has been source of inspiration and marvel for more than 2000 years.

## License

This software is packaged with a MIT License.

[^1]: The Extraordinary Voyage of Pytheas the Greek, Barry Cunliffe (2001), Chapter 6.
