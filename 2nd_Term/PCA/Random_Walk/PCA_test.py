import numpy as np
from numpy.linalg import eig
import matplotlib.pyplot as plt


Np = 2
Ns = 5

Plot_N = 2

# position array

# Position array (Np, Ns)
# Position_array = np.load("{}D_{}Np_{}Ns_position.npy".format(D, Np, Ns))

# x = np.random.rand(Ns)
# y = np.random.rand(Ns)

x = [1,4,5,8,9]
y = [9,7,4,2,1]

Position_array = np.array([x, y])
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


# original position plotting

plt.figure()
plt.title("Position on original coordinate")
plt.xlabel("time")
plt.ylabel("original coordinate")
for i in np.arange(Plot_N):
    plt.plot(Position_array[i, :], label = "x{}".format(i+1))
plt.legend()
#plt.savefig("{}D_{}Ns_OriCoordinate_time_plot.png".format(D*Np, Ns))
plt.show()




# Transformed position plotting

# deviation array = x-<x>
transformed_position_array = np.matmul(E_vector_matrix.T, deviation_array) 


plt.figure()
plt.title("Projection on Principal Component")
plt.xlabel("time")
plt.ylabel("Principal component")
for i in np.arange(Plot_N):
    plt.plot(transformed_position_array[i, :], label = "PC{}".format(Plot_N-i))
plt.legend()
#plt.savefig("{}D_{}Ns_PCA_time_plot.png".format(D*Np, Ns))
plt.show()






'''
a = np.array([[0, 2], 
              [2, 3]])
w,v=eig(a)
print('E-value:', w)
print('E-vector', v)

R = v
print(R)

D = np.matmul(np.matmul(R.T, a), R)
print(D)
'''
