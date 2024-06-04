import numpy as np
from numpy.linalg import eig
import matplotlib.pyplot as plt





# Position array (Np, Ns)

# framestep
fs = 1
name = "10002ps_100ps"

# protein n dimension
x_array = np.loadtxt('x_{}.dat'.format(name))
y_array = np.loadtxt('y_{}.dat'.format(name))
z_array = np.loadtxt('z_{}.dat'.format(name))
#x_array = np.loadtxt('x_{}.dat'.format(fs))
#y_array = np.loadtxt('y_{}.dat'.format(fs))
#z_array = np.loadtxt('z_{}.dat'.format(fs))
Position_array = z_array
#Position_array = np.concatenate((x_array, y_array, z_array), axis=0)

# shape of position array
Shape = Position_array.shape
Np = Shape[0]
Ns = Shape[1]


print("Position array: \n {} \n".format(Position_array))


# mean_array (Np)
mean_array = np.mean(Position_array, axis =1)
print("Mean for each axis: \n {} \n".format(mean_array))



# deviation matrix (Np, Ns)
deviation_array = np.zeros((Np, Ns))
for i in np.arange(Np):
    deviation_array[i] = Position_array[i] - mean_array[i]
    #print(deviation_array[i])

print("deviation for each axis: \n {} \n".format(deviation_array))


 
# covariance matrix (Np,Np)
Cov_matrix = np.zeros((Np,Np))
ij_cov_deviation_array = np.zeros(Ns)

for i in np.arange(Np):
    for j in np.arange(Np):
        for t in np.arange(Ns):
            ij_cov_deviation_array[t] = deviation_array[i,t] * deviation_array[j,t]
        print( "{}-i {}-j Covariance deviation: \n {} \n".format(i,j,ij_cov_deviation_array))
        
        Cov_matrix[i,j] = np.mean(ij_cov_deviation_array)
        
        #reset
        ij_cov_deviation_array = np.zeros(Ns)


print("Cov matrix: \n {} \n".format(Cov_matrix))



# eigenvalue and eigenvector

E_value_array, E_vector_matrix = eig(Cov_matrix)

print("Eigenvalue: \n {} \n".format(E_value_array))
print("Eigenvector:\n {} \n".format(E_vector_matrix))


# diagonal matrix | checking
Diag = np.matmul(np.matmul(E_vector_matrix.T, Cov_matrix), E_vector_matrix)

print("diagonal matrix with eigenvalue: \n {} \n".format(Diag))



# PCA projection
# deviation array = x-<x>
transformed_position_array = np.matmul(E_vector_matrix.T, deviation_array) 


# save array for plotting
np.save("{}_{}Np_{}Ns_PCA_projection.npy".format(name, Np, Ns), transformed_position_array)
np.save("{}_{}Np_{}Ns_E_value.npy".format(name, Np, Ns), E_value_array)
np.save("{}_{}Np_{}Ns_position.npy".format(name, Np, Ns), Position_array)

#np.save("{}Np_{}Ns_PCA_projection.npy".format(Np, Ns), transformed_position_array)
#np.save("{}Np_{}Ns_E_value.npy".format(Np, Ns), E_value_array)
#np.save("{}Np_{}Ns_position.npy".format(Np, Ns), Position_array)