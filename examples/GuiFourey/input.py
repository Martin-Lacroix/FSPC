# %% Input Parameters

def getParam(path):

    # Metafor and PFEM solvers
    
    param = dict()
    param['inputS'] = 'input_meta'
    param['inputF'] = path+'/input_pfem.lua'

    # Algorithm parameters

    param['interp'] = 'MM_CNS'
    param['algo'] = 'IQN_MVJ'
    param['omega'] = 0.5
    param['maxIt'] = 25
    param['tol'] = 1e-12

    # Time Parameters

    param['dt'] = 5e-4
    param['dtWrite'] = 5e-4
    param['tTot'] = 0.15

    return param