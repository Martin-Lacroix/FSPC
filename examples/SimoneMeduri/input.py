# %% Input Parameters

def getParam(path):

    # Metafor and PFEM solvers
    
    param = dict()
    param['inputS'] = 'input_meta'
    param['inputF'] = path+'/input_pfem.lua'
    
    # Algorithm parameters

    param['algo'] = 'IQN_MVJ'
    param['omega'] = 0.5
    param['maxIt'] = 100
    param['tol'] = 1e-6

    # Time Parameters

    param['dt'] = 0.001
    param['dtWrite'] = 0.01
    param['tTot'] = 10

    return param