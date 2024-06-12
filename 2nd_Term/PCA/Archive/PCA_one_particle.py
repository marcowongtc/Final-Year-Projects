import numpy as np
from numpy.linalg import eig
import matplotlib.pyplot as plt



D = 3
Np = 1000
Ns = 1000

# position array

# Position array (D, Np, Ns)
Position_array = np.load("{}D_{}Np_{}Ns_position.npy".format(D, Np, Ns))

# one_position_array (D, Ns)
#one_position_array = Position_array[:,1,:]
one_position_array = np.mean(Position_array, axis = 1)
#print(one_position_array)


# mean_array (D)
mean_array = np.mean(one_position_array, axis =1)
print("Mean for each axis: \n {} \n".format(mean_array))


# mean deviation matrix (D)
mean_deviation_array = np.zeros(D)
for i in np.arange(D):
    mean_deviation_array[i] = np.mean(one_position_array[i,:] - mean_array[i])

print("Mean deviation for each axis: \n {} \n".format(mean_deviation_array))



# covariance matrix
Cov_matrix = np.zeros((D,D))

for i in np.arange(D):
    for j in np.arange(D):
        Cov_matrix[i,j] = mean_deviation_array[i] * mean_deviation_array[j]


print("Cov matrix: \n {} \n".format(Cov_matrix))



# eigenvalue and eigenvector

E_value_array, E_vector_matrix = eig(Cov_matrix)

print("Eigenvalue: \n {} \n".format(E_value_array))
print("Eigenvector:\n {} \n".format(E_vector_matrix))


# diagonal matrix | checking
Diag = np.matmul(np.matmul(E_vector_matrix.T, Cov_matrix), E_vector_matrix)

print("diagonal matrix with eigenvalue: \n {} \n".format(Diag))


# Transformed position plotting
transformed_position_array = np.matmul(E_vector_matrix.T, one_position_array) 


plt.figure()
plt.title("Projection on Principal Component")
plt.xlabel("time")
plt.ylabel("Principal component")
for i in np.arange(3):
    plt.plot(transformed_position_array[i, :], label = "PC{}".format(i+1))
plt.legend()
plt.savefig("{}D_{}Np_{}Ns_PCA_time_plot_avg.png".format(D, Np, Ns))
plt.show()



# original position plotting

plt.figure()
plt.title("Position on original coordinate")
plt.xlabel("time")
plt.ylabel("original coordinate")
for i in np.arange(3):
    plt.plot(one_position_array[i, :], label = "x{}".format(i+1))
plt.legend()
plt.savefig("{}D_{}Np_{}Ns_OriCoordinate_time_plot_avg.png".format(D, Np, Ns))
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
