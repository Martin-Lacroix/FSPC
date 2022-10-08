from . import criterion
from . import tools

# %% Create and Runs an FSI computation

class Master(object):
    def __init__(self,param,com):
        input = dict()

        # Creates the external solver objects

        if com.rank == 0:

            log = param['log'] = tools.Log('pfem.log')
            input['solver'] = log.exec(self.getFluid,param)

        if com.rank == 1:

            log = param['log'] = tools.Log('metafor.log')
            input['solver'] = log.exec(self.getSolid,param)

        # Initialize the time step and convergence manager

        input['step'] = criterion.TimeStep(param)
        input['converg'] = criterion.Convergence(param)

        # Initialize the interface mesh intrepolator

        if param['interp']=='NNS':

            from source.interpolator.nearNeigh import NNS
            input['interp'] = NNS(input,com)

        elif param['interp']=='RBF':

            from source.interpolator.radialBasis import RBF
            input['interp'] = RBF(input,param,com)

        # Initialize the fluid-structure coupling algorithm

        if param['algo']=='BGS_ADR':

            from source.algorithm.blockGauss import BGS_ADR
            self.algo = BGS_ADR(input,param,com)

        elif param['algo']=='IQN_ILS':
            
            from source.algorithm.leastSquares import IQN_ILS
            self.algo = IQN_ILS(input,param,com)

        elif param['algo']=='IQN_MVJ':
            
            from source.algorithm.multiVector import IQN_MVJ
            self.algo = IQN_MVJ(input,param,com)

# %% Initialize Metafor and Pfem3D

    def getSolid(self,param):
        
        import fwkw
        self.redirect = fwkw.StdOutErr2Py()
        from source.solver.Metafor import Metafor
        return Metafor(param)

    def getFluid(self,param):

        import pfem3Dw
        self.redirect = pfem3Dw.PythonCerrCout()
        from source.solver.Pfem3D import Pfem3D
        return Pfem3D(param)
