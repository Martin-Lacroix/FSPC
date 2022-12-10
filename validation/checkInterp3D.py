import os
import parula
import numpy as np
parula = parula.colour()
from scipy import interpolate

# %% Interpolate Data on Solid Mesh

def interpS(y,z,data):

    pts = np.transpose([y,z])
    interp = interpolate.griddata(pts,data,(Y,Z),method='linear')
    return interp

def double_Integral(A):

    AI = A[1:-1,1:-1]
    dS = 1/(Ly-1)/(Lz-1)

    A_u,A_d,A_l,A_r = (A[0,1:-1],A[-1,1:-1],A[1:-1,0],A[1:-1,-1])
    A_ul,A_ur,A_dl,A_dr = (A[0,0],A[0,-1],A[-1,0],A[-1,-1])

    result = (np.sum(A_u)+np.sum(A_d)+np.sum(A_l)+np.sum(A_r))/2
    result += np.sum(AI)+(A_ul+A_ur+A_dl+A_dr)/4
    return dS*result

# %% Print Figure Stress

def computeError(file,name):

    dataS = np.loadtxt('S_'+file+'.dat')
    dataF = np.loadtxt('F_'+file+'.dat')

    error = np.zeros(dataF.shape[0])
    EF = np.zeros((dataS.shape))

    # Interpolate F on S and compute the error

    for i in range(dataS.shape[0]):

        LS = interpS(yS,zS,dataS[i])
        IF = interpS(yF,zF,dataF[i])
        EF[i] = np.abs(IF-LS).flatten()

        # Integrate the least square error
        
        num = double_Integral(np.square(IF-LS))
        den = double_Integral(np.square(IF))
        error[i] = num/den

    # Print for LaTeX scatter plot

    plotS = np.transpose([yS,zS,dataS[index]])
    plotF = np.transpose([yF,zF,dataF[index]])
    plotE = np.transpose([yS,zS,EF[index]])

    np.savetxt('plot/F_'+name+'.dat',plotF)
    np.savetxt('plot/S_'+file+'.dat',plotS)
    np.savetxt('plot/E_'+file+'.dat',plotE)

    mean = np.mean(error)
    std = np.std(error)
    return mean,std

# %% Change the Folder

workspace = os.getcwd()+'/workspace/'
folder = os.listdir(workspace)[0]
os.chdir(workspace+folder)

yS = np.loadtxt('yS.dat')
zS = np.loadtxt('zS.dat')
yF = np.loadtxt('yF.dat')
zF = np.loadtxt('zF.dat')

# Rescale the coordinates within (0,1)

yS -= np.min(yS); yS /= np.max(yS)
zS -= np.min(zS); zS /= np.max(zS)
yF -= np.min(yF); yF /= np.max(yF)
zF -= np.min(zF); zF /= np.max(zF)

# Transform the solid coordinates into indices

dy = np.unique(yS.round(decimals=6)).size-1
Iy = np.round(yS*dy+1e-6).astype(int)

dz = np.unique(zS.round(decimals=6)).size-1
Iz = np.round(zS*dz+1e-6).astype(int)

Lz = len(np.unique(Iz))
Ly = len(np.unique(Iy))

# Make a grid for the error computation

Y = np.linspace(0,1,Ly)
Z = np.linspace(0,1,Lz)
Y,Z = np.meshgrid(Y,Z)
Z = np.flip(Z,axis=0)

yE = Y.flatten()
zE = Z.flatten()

# %% Change the Folder

index = -1
key = None
std = dict()
mean = dict()

workspace += folder+'/interp'
os.chdir(workspace)

try: os.mkdir('plot')
except: pass

try: os.mkdir('error')
except: pass

np.savetxt('plot/yS.dat',yS)
np.savetxt('plot/zS.dat',zS)
np.savetxt('plot/yF.dat',yF)
np.savetxt('plot/zF.dat',zF)
np.savetxt('plot/yE.dat',yE)
np.savetxt('plot/zE.dat',zE)

# List the output files

file = os.listdir(workspace)
file = [F for F in file if os.path.isfile(F)]
file = np.unique([F[2:-4] for F in file])

# %% Computes and Print the Error

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