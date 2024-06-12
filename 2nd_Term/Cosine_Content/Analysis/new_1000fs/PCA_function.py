import numpy as np
from numpy.linalg import eig
import matplotlib.pyplot as plt


#------------------------------------
# Slice function: 
# slice data into part with given slice length, Nth slice
# data_array: original data array
# Slicelength (ps): length of slicing
# StepSize (ps): 0.1 / 1 ps
# Nthslice: Nth slice for whole data
#------------------------------------

def slice(data_array, Slicelength, StepSize, Nthslice):
    sliced_data_array = data_array[:,int(Slicelength/StepSize)*(Nthslice-1):int(Slicelength/StepSize)*(Nthslice)]
    return sliced_data_array



#------------------------------------
# PCA function: 
# do all Principal component analysis
# return transformed data + E value
#------------------------------------

def PCA(data_array):    
    # Position array (Np, Ns)
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
    PCA_projection = np.matmul(E_vector_matrix.T, deviation_array) 

    return PCA_projection, E_value_array




#------------------------------------
# PCA plotting: 
# PCA_projection: PCA of sliced array
# Evalue_array: Evalue of sliced array
# Slicelength (ps): length of slicing
# Step size (ps): 1ps / 0.1ps
# Nthslice: Nth slice we desired to plot
# NoPCplot: No of PC to be plotted
#------------------------------------
def PCA_slice_plot(PCA_projection, Evalue_array, Slicelength, Stepsize, Nthslice, NoPCplot):

    # PCA projection plotting | subplot view
    plt.figure(figsize=(7, NoPCplot*2))

    max = np.max(np.abs(PCA_projection))

    #No. of steps
    Ns = PCA_projection.shape[1]

    for i in np.arange(NoPCplot):
        
        plt.subplot(NoPCplot, 1, i+1)
        t = np.linspace(Stepsize,Stepsize*Ns, Ns)
        plt.plot(t, PCA_projection[i, :], label = "PC{}, {:.2f}".format(i+1, Evalue_array[i])) 
        plt.plot(t, np.zeros(Ns), ls = '-.', color='grey') # dashed line at average position 0

        plt.ylim(-max, max)

        # label of subplot
        plt.ylabel("PC{}".format(i+1))
        plt.xlabel("time (ps)")


    plt.suptitle("PC Projection | Time Length: {}ps | Time Step: {}ps | Slice: {} ".format(Slicelength, Stepsize, Nthslice))
    plt.savefig("PCA_subplot_{}ps_{}ps_{}slice_{}PC.png".format(Slicelength, Stepsize, Nthslice, NoPCplot))
    print("Plot Saved! | {}".format("PCA_subplot_{}ps_{}ps_{}slice_{}PC.png".format(Slicelength, Stepsize, Nthslice, NoPCplot)))
    plt.close()
    #plt.show()


    # PCA projection plotting | one plot view
    plt.figure()
    plt.title("PC Projection | Time Length: {}ps | Time Step: {}ps | Slice: {} ".format(Slicelength, Stepsize, Nthslice))
    plt.ylabel("Principle component projection")
    plt.xlabel("time (ps)")

    for i in np.arange(NoPCplot):
        plt.plot(t,PCA_projection[i, :], label = "PC{}, {:.2f}".format(i+1, Evalue_array[i]))

    plt.legend()
    plt.savefig("PCA_plot_{}ps_{}ps_{}slice_{}PC.png".format(Slicelength, Stepsize, Nthslice, NoPCplot))
    print("Plot Saved! | {}".format("PCA_plot_{}ps_{}ps_{}slice_{}PC.png".format(Slicelength, Stepsize, Nthslice, NoPCplot)))
    plt.close()
    #plt.show()

