import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt

# Make the points and values

points = list()
points.append([2, 1])
points.append([1.5, 1+np.sqrt(3)/2])
points.append([0.5, 1+np.sqrt(3)/2])
points.append([0, 1])
points.append([0.5, 1-np.sqrt(3)/2])
points.append([1.5, 1-np.sqrt(3)/2])
points = np.array(points)

values = list()
values.append(1)
values.append(2)
values.append(3)
values.append(4)
values.append(5)
values.append(6)
values = np.array(values)

# Make the KNN interpolation

def compute_KNN(position):

    dist = np.linalg.norm(position-points, axis=1)
    weight = list()

    for j in range(len(dist)):

        val = [R for k, R in enumerate(dist) if k != j]
        weight.append(np.prod(val))

    weight = np.array(weight)/np.sum(weight)
    return np.dot(values, weight)

# Make the BELL interpolation

def compute_BELL(position):

    dist = np.linalg.norm(position-points, axis=1)
    weight = list()

    # h = Size of the initial Gaussian
    # ??? Influence unknown

    h = 1
    W = lambda r: np.exp(-np.square(r/h))

    # h = Size of the fix Gaussian (make interp exact at nodes)
    # Larger for smoother transition between the nodes
    
    c = 3
    B = lambda r: 1/np.exp(-np.square(r/c))-1

    for i, radius in enumerate(dist):

        init_weight = W(radius)
        weight_coef = list()

        for k, neigh_pos in enumerate(points):

            if(k == i): continue
            neigh_r = np.linalg.norm(position-neigh_pos)
            weight_coef.append(B(neigh_r))

        init_weight *= np.prod(weight_coef)
        weight.append(init_weight)

    weight = np.array(weight)/np.sum(weight)
    return np.dot(values, weight)

# Make the interpolation grid

step = 0.01
grid = np.arange(0, 2+step, step)
X, Y = np.meshgrid(grid, grid)

Z1 = np.zeros((grid.size, grid.size))
Z2 = np.zeros((grid.size, grid.size))

for i, y in enumerate(grid):
    for j, x in enumerate(grid):

        position = np.array([x, y])
        Z1[i, j] = compute_KNN(position)
        Z2[i, j] = compute_BELL(position)

# Plot the KNN result in 3D

ax = plt.figure().add_subplot(projection='3d')
ax.plot_surface(X, Y, Z1, cmap=cm.viridis)
ax.scatter(*points.T, values, c='k', alpha=1, s=30)
plt.show()

# Plot the BELL result in 3D

ax = plt.figure().add_subplot(projection='3d')
ax.plot_surface(X, Y, Z2, cmap=cm.viridis)
ax.scatter(*points.T, values, c='k', alpha=1, s=30)
plt.show()
