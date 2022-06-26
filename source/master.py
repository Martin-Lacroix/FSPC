from . import interpolator
from . import criterion

# %% Create and Runs an FSI computation

class Master(object):
    def __init__(self,param,com):
        
        input = dict()

        if com.rank == 0: input['solverF'] = self.getFluidSolver(param)
        if com.rank == 1: input['solverS'] = self.getSolidSolver(param)

        # Check the dimension of the solvers

        if com.rank == 0: param['dim'] = input['solverF'].dim
        if com.rank == 1: param['dim'] = input['solverS'].dim

        # Initialize some FSPC objects
        
        input['step'] = criterion.TimeStep(param)
        if com.rank == 1: input['converg'] = criterion.Convergence(param)
        input['interp'] = interpolator.Matching(input,param,com)

        # Initialize the FSI algorithm

        if param['algo']=='BGS_ADR':

            from source.algorithm.blockGauss import BGS_ADR
            self.algo = BGS_ADR(input,param,com)

        elif param['algo']=='IQN_ILS':
            
            from source.algorithm.leastSquares import IQN_ILS
            self.algo = IQN_ILS(input,param,com)

        elif param['algo']=='IQN_MVJ':
            
            from source.algorithm.multiVector import IQN_MVJ
            self.algo = IQN_MVJ(input,param,com)

    # Metafor must be loadad within a function

    def getSolidSolver(self,param):

        from source.wraper.Metafor import Metafor
        return Metafor(param)

    # Pfem3D must be loadad within a function

    def getFluidSolver(self,param):

        from source.wraper.Pfem3D import Pfem3D
        return Pfem3D(param)
