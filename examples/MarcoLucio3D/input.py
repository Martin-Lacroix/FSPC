# %% Input Parameters

def getParam(path):

    # Metafor and PFEM solvers
    
    param = dict()
    param['inputS'] = 'input_meta'
    param['inputF'] = path+'/input_pfem.lua'
    
    # Algorithm parameters

    param['algo'] = 'IQN_MVJ'
    param['retainStep'] = 0
    param['omega'] = 0.5
    param['maxIt'] = 25
    param['tol'] = 1e-6

    # Time Parameters

    param['dt'] = 0.001
    param['dtWrite'] = 0.001
    param['tTot'] = 1

    return param