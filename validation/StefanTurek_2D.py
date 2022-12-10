from matplotlib import pyplot as plt
from scipy import interpolate
from Externals import tools
import numpy as np
import os

# %% Print the Mass

workspace = os.getcwd()+'/workspace'
os.chdir(workspace)

# Reads the results

mass = np.loadtxt('mass.txt',delimiter=',').T
mass[1] = 100*mass[1]/mass[1,0]

# Save Results

plt.figure(1)
plt.gca().set_title('Total Mass')
np.savetxt('mass.dat',np.transpose(mass),fmt=['%.6f','%.6f'])
plt.plot(*mass)
plt.grid()
plt.show()

# %% Print the Output

workspace = os.getcwd()+'/metafor'
os.chdir(workspace)

# Reads the results

dt = 1e-3
tag = tools.getIndex([0.6,0.2,0])
time,disp = tools.readNode(tag)

# Quadratic piecewise interpolation

interp = interpolate.interp1d(time,disp[:,1],kind='quadratic')
time = np.arange(0,time[-1],dt)
results = [time,interp(time)]
disp = interp(time)

# Moves to main folder

workspace = os.path.split(workspace)[0]
os.chdir(workspace)

# Relative amplitude and frequency

A = (np.max(disp)-np.min(disp))/2
fourier = np.fft.fft(disp)[range(len(disp)//2)]
freq = np.arange(len(disp)//2)/time[-1]
F = freq[np.argmax(abs(fourier))]

# Print some global results

print('\nMaximum amplitude : {:.6f}'.format(A))
print('Main frequency : {:.6f}\n'.format(F))

# %% Save Results

plt.figure(1)
plt.gca().set_title('Output Data')
np.savetxt('output.dat',np.transpose(results),fmt=['%.6f','%.6f'])
plt.plot(*results)
plt.grid()
plt.show()

plt.figure(2)
plt.gca().set_title('Fourier Transform')
plt.plot(freq,abs(fourier))
plt.grid()
plt.show()