## Introduction

Code developed for obtaining the **Doctor of Philosophy in Engineering**. The code is a Python package providing fluid-structure interaction tools for partitioned coupling between the solid solver [Metafor](http://metafor.ltas.ulg.ac.be/dokuwiki) and the fluid solver [PFEM3D](https://github.com/ImperatorS79/PFEM3D). The examples and doc folders contain some test-cases as well as a documentation.

## Installation

First, make sure to work with Python 3 and the scientific packages. Then, add the main repository folder to your Python path environment variables. Another possibility is to add the path to FSPC in your Python script. It is important to note that FSPC assumes the external solvers are also in your Python path.
```css
export PYTHONPATH=path-to-fspc
```
```css
from sys import path
path.append('path-to-fspc')
import FSPC
```

## Author

* Martin Lacroix
