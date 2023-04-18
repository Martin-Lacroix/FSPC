from matplotlib import pyplot as plt
import matplotlib
import pickle
import os

# %% Read the Output File

os.chdir('workspace')
out = pickle.load(open('out.pickle','rb'))

color = dict()
color['ETM'] = '#a5be6b'
color['RBF'] = '#127dd8'
color['KNN'] = '#b46478'

font = {'size':16}
matplotlib.rc('font',**font)
plt.rcParams["font.family"] = ["Latin Modern Roman"]

# %% Print the Current Result

width = 2
fig,ax = plt.subplots(1,figsize=[10,5])

for key,val in out['recvLoad'].items(): 
    plt.plot(out['recvPos'],val,label=key,color=color[key])

for key,val in out['curvLoad'].items():
    plt.plot(out['curvPos'],val,'--',label=key,color='black')
    plt.plot(out['curvPos'],val,'o',markersize=7,color='black',mfc='none')

plt.legend(loc='upper left')
plt.ylabel('Stress Tensor $\sigma_{\,11}$ (Pa)')
plt.xlabel('Interface Curvilinear Position')
plt.grid()
plt.show()

# %% Print the Current Result

width = 0.4
key = list(out['error'].keys())
val = list(out['error'].values())

fig,ax = plt.subplots(1,figsize=[9,4])
plt.bar(key,val,color=color.values(),width=width,log=1,zorder=3)
plt.ylabel('Average Error on $\sigma_{\,11}$ [-]')
ax.grid(zorder=0)
plt.show()