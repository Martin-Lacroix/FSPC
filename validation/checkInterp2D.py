from scipy import interpolate
import numpy as np
import os

# %% Compute the Error

def computeError(file,name):

    dataS = np.loadtxt('S_'+file+'.dat')
    dataF = np.loadtxt('F_'+file+'.dat')

    xS = np.linspace(0,1,dataS.shape[1])
    xF = np.linspace(0,1,dataF.shape[1])

    error = np.zeros(dataF.shape[0])

    plotS = np.transpose([xS,dataS[index]])
    plotF = np.transpose([xF,dataF[index]])

    np.savetxt('plot/S_'+file+'.dat',plotS)
    np.savetxt('plot/F_'+name+'.dat',plotF)

    # Interpolate F on S and integrate the error

    for i,load in enumerate(dataF):

        IF = interpolate.interp1d(xF,load,kind='linear')
        ES = np.power(IF(xS)-dataS[i],2)

        load = np.power(load,2)
        error[i] = np.trapz(ES,xS)/np.trapz(load,xF)

    mean = np.mean(error)
    std = np.std(error)
    return mean,std

# %% Change the Folder

workspace = os.getcwd()+'/workspace/'
folder = os.listdir(workspace)[0]
workspace += folder+'/interp'
os.chdir(workspace)

try: os.mkdir('plot')
except: pass

try: os.mkdir('error')
except: pass

# List the output files

file = os.listdir(workspace)
file = [F for F in file if os.path.isfile(F)]
file = np.unique([F[2:-4] for F in file])

# %% Computes and Print the Error

index = -1
key = None
std = dict()
mean = dict()

for F in file:

    if 'stress' in F: name = 'stress'
    elif 'force' in F: name = 'force'
    elif 'equiv' in F: name = 'equiv'
    elif 'disp' in F: name = 'disp'
    else: continue

    M,S = computeError(F,name)

    if(key != F[:F.rfind('_')]): print('')
    val = F[F.rfind('_')+1:]
    key = F[:F.rfind('_')]

    if key not in mean: mean[key] = list()
    if key not in std: std[key] = list()

    mean[key].append([val,M])
    std[key].append([val,S])

    M = '{:.2e}'.format(M).ljust(10)
    S = '{:.2e}'.format(S).ljust(10)
    print(F.ljust(20),M,S)

# %% Computes the Minimum Mean

print('\nMin Error --------------------------')
interp = None

for key,val in mean.items():

    val = np.array(val).astype(float)
    idx = np.argmin(val[:,1])

    K,M = val[idx]
    S = std[key][idx][1]

    if(interp != key[:key.rfind('_')]): print('')
    interp = key[:key.rfind('_')]

    K = str(K).ljust(7)
    M = '{:.2e}'.format(M).ljust(10)
    S = '{:.2e}'.format(S).ljust(10)
    print(key.ljust(12),K,M,S)

# %% Computes the Minimum Std

print('\nMin Std ----------------------------')
interp = None

for key,val in std.items():

    val = np.array(val).astype(float)
    idx = np.argmin(val[:,1])

    K,S = val[idx]
    M = mean[key][idx][1]

    if(interp != key[:key.rfind('_')]): print('')
    interp = key[:key.rfind('_')]

    K = str(K).ljust(7)
    S = '{:.2e}'.format(S).ljust(10)
    M = '{:.2e}'.format(M).ljust(10)
    print(key.ljust(12),K,M,S)

# %% Normalized (Disp + Force) Error

print('\nMin Disp - Force -------------------\n')

for key,val in mean.items():

    if 'force' in key:

        fun = key[key.rfind('_'):]
        disp = 'disp'+key[key.rfind('_'):]

        valF = np.array(val).astype(float)
        valD = np.array(mean[disp]).astype(float)
        
        resF = valF[:,1]/np.min(valF[:,1])
        resD = valD[:,1]/np.min(valD[:,1])
        idx = np.argmin(resF+resD)

        K,F = valF[idx]
        K,D = valD[idx]

        K = str(K).ljust(7)
        D = '{:.2e}'.format(D).ljust(10)
        F = '{:.2e}'.format(F).ljust(10)
        print('D_F'+fun.ljust(12),K,D,F)

# %% Radius Error Plot

for key,val in mean.items():

    data = np.array(val).astype(float)
    index = np.argsort(data[:,0])
    data = np.transpose(data[index])
    data[0] = np.arange(data[0].size)

    np.savetxt('error/'+key+'.dat',data.T)

print('\n')