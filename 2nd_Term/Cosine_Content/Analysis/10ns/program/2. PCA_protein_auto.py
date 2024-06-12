import numpy as np
from numpy.linalg import eig
import matplotlib.pyplot as plt
import sys

# Parameter input
if len(sys.argv) > 3:
    # Retrieve the parameter value
    N = int(sys.argv[1])
    TL = int(sys.argv[2])
    ST = int(sys.argv[3])       
    print("Ns:{}ps TL:{}ps ST:{}ps".format(N, TL, ST))
else:
    print("parameters are not fully provided.")




# Position array (Np, Ns)
data_array = np.load("data_{}ns_1ps_{}TL_{}ST.npy".format(int(N/1000), int(TL/1000), int(ST/1000)))
Position_array = data_array


#shape of position array
data_shape = Position_array.shape
Np = data_shape[0]
Ns = data_shape[1]
print("Data array: \n {} \n".format(data_array))
print("Shape: {} \n".format(data_shape))



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
    print( "{}-i Covariance deviation Done!".format(i))
    for j in np.arange(Np):
        for t in np.arange(Ns):
            ij_cov_deviation_array[t] = deviation_array[i,t] * deviation_array[j,t]
        #print( "{}-i {}-j Covariance deviation: \n {} \n".format(i,j,ij_cov_deviation_array))
        #print( "{}-i {}-j Covariance deviation Done!".format(i,j))
        
        Cov_matrix[i,j] = np.mean(ij_cov_deviation_array)
        
        #reset
        
        ij_cov_deviation_array = np.zeros(Ns)


print("\n Cov matrix: \n {} \n".format(Cov_matrix))



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
np.save("PCA_{}ns_1ps_{}TL_{}ST.npy".format(int(N/1000), int(TL/1000), int(ST/1000)), transformed_position_array)
np.save("Evalue_{}ns_1ps_{}TL_{}ST.npy".format(int(N/1000), int(TL/1000), int(ST/1000)), E_value_array)

print("Data Saved! | {}".format("PCA_{}ns_1ps_{}TL_{}ST.npy".format(int(N/1000), int(TL/1000), int(ST/1000))))
print("Data Saved! | {}\n".format("Evalue_{}ns_1ps_{}TL_{}ST.npy".format(int(N/1000), int(TL/1000), int(ST/1000))))
print("-----------------------------------------------------------------------")