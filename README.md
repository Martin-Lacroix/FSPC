## Introduction

This code is intended to be used as a Python package providing fluid-structure interaction tools for partitioned coupling between the solid solver [Metafor](http://metafor.ltas.ulg.ac.be/dokuwiki) and the fluid solver [PFEM3D](https://github.com/ImperatorS79/PFEM3D). The doc folder contains a brief documentation written in markdown. The examples folder contains some working 2D and 3D test-cases.

## Installation

First, make sure to work with Python 3 and the scientific packages. Then, add the main repository folder to your Python path environment variables. Another possibility is to add the path to FSPC in your Python script. It is important to note that FSPC assumes the paths to the external solvers Metafor and PFEM3D are available in your Python environment.
```sh
export PYTHONPATH=path-to-fspc
```
```python
from sys import path
path.append('path-to-fspc')
import FSPC
```
