import numpy as np

name = "99.4ps_0.1ps"

x_array = np.loadtxt('x_{}.dat'.format(name))
y_array = np.loadtxt('y_{}.dat'.format(name))
z_array = np.loadtxt('z_{}.dat'.format(name))

Position = np.concatenate((x_array, y_array, z_array), axis=0)

print(Position.shape)

shape = Position.shape
print(shape[0])
print(shape[1])