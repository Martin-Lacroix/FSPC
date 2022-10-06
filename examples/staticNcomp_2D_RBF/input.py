# %% Input Parameters

def getParam(path):

    # Metafor and PFEM solvers
    
    param = dict()
    param['inputS'] = 'input_meta'
    param['inputF'] = path+'/input_pfem.lua'

    # Algorithm parameters

    param['RBF'] = 'MQ'
    param['radius'] = 1
    param['interp'] = 'NM_RBF'
    param['algo'] = 'IQN_ILS'
    param['omega'] = 0.5
    param['maxIt'] = 25
    param['tol'] = 1e-8

    # Time Parameters

    param['dt'] = 0.01
    param['dtWrite'] = 0.05
    param['tTot'] = 20

    return param