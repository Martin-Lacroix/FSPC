from matplotlib import pyplot as plt
import pickle
import os

# %% Print the Current Result

print('\n')
os.chdir('workspace')
out = pickle.load(open('out.pickle','rb'))
for key,val in out['error'].items(): print(key,':',val)
print('\n')

# Plot a graph of the saved result

color = dict()
color['KNN'] = 'firebrick'
color['RBF'] = 'darkorange'
color['ETM'] = 'forestgreen'

plt.figure(1)

for key,val in out['recvLoad'].items(): 
    plt.plot(out['recvPos'],val,'--',label=key,color=color[key])
    plt.plot(out['recvPos'],val,'.',markersize=7,color=color[key])

for key,val in out['curvLoad'].items():
    plt.plot(out['curvPos'],val,label=key,color='black')

plt.legend()
plt.grid()
plt.show()
