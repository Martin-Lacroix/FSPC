from .Toolbox import setStep
from .Toolbox import setInterp
from .Toolbox import setSolver
from .Toolbox import printClock
from .Toolbox import setConvMecha
from .Toolbox import setConvTherm

# Import the partitioned coupling algorithms

from .algorithm.BlockGauss import BGS
from .algorithm.LeastSquare import ILS
from .algorithm.MultiVector import MVJ

# Import the mesh interpolation methods

from .interpolator.ElemTransfer import ETM 
from .interpolator.NearestNeigh import KNN
from .interpolator.BasisFunction import RBF

# Try adding init.py in the folder to create a sub-namespace ???