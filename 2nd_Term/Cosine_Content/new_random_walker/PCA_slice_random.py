import numpy as np
from numpy.linalg import eig
import matplotlib.pyplot as plt

from PCA_function import slice, PCA
#------------------------------------
# Slice function: 
# slice data into part with given slice length, Nth slice
# data_array: original data array
# Slicelength (ps): length of slicing
# StepSize (ps): 0.1 / 1 ps
# Nthslice: Nth slice for whole data
#------------------------------------


# time length in ps
N100000_array = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]

random_data_array = np.load("../100Np_10000Ns_position.npy")

random_data_array = random_data_array[:63,:]


# Slice + PCA | 1ps 10000ps
TotalTime = 10000 #ps
StepSize = 1 #ps
for Slicelength in N100000_array:
    for Nthslice in np.arange(1,int(TotalTime/Slicelength)+1):
        #print(Nthslice)
        
        sliced_array = slice(random_data_array, Slicelength, StepSize, Nthslice)
        print("sliced_array:{}".format(sliced_array.shape))

        PCA_projection, Evalue = PCA(sliced_array)

        np.save("PCA_{}ps_{}ps_{}slice.npy".format(Slicelength, StepSize, Nthslice), PCA_projection)
        np.save("Evalue_{}ps_{}ps_{}slice.npy".format(Slicelength, StepSize, Nthslice), Evalue)

        print("PCA Saved! | {}".format("PCA_{}ps_{}ps_{}slice.npy".format(Slicelength, StepSize, Nthslice)))
        print("Evalue Saved! | {}".format("Evalue_{}ps_{}ps_{}slice.npy".format(Slicelength, StepSize, Nthslice)))


