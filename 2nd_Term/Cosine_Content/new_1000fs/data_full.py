import numpy as np
from numpy.linalg import eig
import matplotlib.pyplot as plt
import sys

# Parameter input
# 1st argument: filename of dat
# 2nd argyment: total lenght in fs
# 3rd argument: step size in fs
if len(sys.argv) > 3:
    # Retrieve the parameter value
    filename = sys.argv[1]    #0 contain the name of python script
    totallength = sys.argv[2]
    stepsize = sys.argv[3]         
    print("data filename:", filename)
else:
    print("filename not provided.")



# Position array (Np, Ns)

# protein n dimension
x_array = np.loadtxt('x_{}.dat'.format(filename))
y_array = np.loadtxt('y_{}.dat'.format(filename))
z_array = np.loadtxt('z_{}.dat'.format(filename))

data_array = np.concatenate((x_array, y_array, z_array), axis=0)
data_array = data_array[:,:data_array.shape[1]]

# shape of position array
data_shape = data_array.shape
Np = data_shape[0]
Ns = data_shape[1]

print("Data array: \n {} \n".format(data_array))
print("Shape: {} \n".format(data_shape))


np.save("data_full_{}ps_{}ps.npy".format(totallength, stepsize), data_array)
print("Data Saved! | {}\n".format("data_full_{}ps_{}ps.npy".format(totallength, stepsize)))