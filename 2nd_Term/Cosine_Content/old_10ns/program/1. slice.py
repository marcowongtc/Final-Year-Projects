import numpy as np
from numpy.linalg import eig
import matplotlib.pyplot as plt
import sys

# Parameter input
if len(sys.argv) > 1:
    # Retrieve the parameter value
    filename = sys.argv[1]    #0 contain the name of python script         
    print("data filename:", filename)
else:
    print("filename not provided.")



# Position array (Np, Ns)

# protein n dimension
x_array = np.loadtxt('x_{}.dat'.format(filename))
y_array = np.loadtxt('y_{}.dat'.format(filename))
z_array = np.loadtxt('z_{}.dat'.format(filename))

data_array = np.concatenate((x_array, y_array, z_array), axis=0)
data_array = data_array[:,2:]

# shape of position array
data_shape = data_array.shape
Np = data_shape[0]
Ns = data_shape[1]

print("Data array: \n {} \n".format(data_array))
print("Shape: {} \n".format(data_shape))




#Slicing
##################################################
#Time Length Slicing
print("Time length Slicing Start!! \n------------------------------")

# Variable
TL_incr = 1000  #time length increment of slicing: 1000ps = 1ns
ST = 0

# change TL with increment
for TL in range(TL_incr, Ns+1, TL_incr): 
    print("Time length:{}".format(TL))

    #slicing
    new_data_array = data_array[:, :TL]
    new_data_shape = new_data_array.shape 
    print("New Shape: {}".format(new_data_shape))

    #save to .npy for further access
    np.save("data_{}ns_1ps_{}TL_{}ST.npy".format(int(Ns/1000), int(TL/1000), int(ST/1000)), new_data_array)
    print("Data Saved! | {}\n".format("data_{}ns_1ps_{}TL_{}ST.npy".format(int(Ns/1000), int(TL/1000), int(ST/1000))))

##################################################
#Start Time Slicing
# Variable
TL = 1000  
ST_incr = 1000  #start length increment of slicing: 1000ps = 1ns

# change TL with increment
for ST in range(0, Ns, ST_incr): 
    print("Start length:{}".format(ST))

    #slicing
    new_data_array = data_array[:, ST:ST+TL]
    new_data_shape = new_data_array.shape 
    print("New Shape: {}".format(new_data_shape))

    #save to .npy for further access
    np.save("data_{}ns_1ps_{}TL_{}ST.npy".format(int(Ns/1000), int(TL/1000), int(ST/1000)), new_data_array)
    print("Data Saved! | {}\n".format("data_{}ns_1ps_{}TL_{}ST.npy".format(int(Ns/1000), int(TL/1000), int(ST/1000))))