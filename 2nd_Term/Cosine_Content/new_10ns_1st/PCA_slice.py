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
one_ps_array = [100, 200, 500, 1000, 2000, 5000, 10000]
pointone_ps_array = [10, 20, 50, 100, 200, 500, 1000]


one_ps_data_array = np.load("../data_full_10000ps_1ps.npy")
pointone_ps_data_array = np.load("../data_full_1000ps_0.1ps.npy")


# Slice + PCA | 1ps 10000ps
TotalTime = 10000 #ps
StepSize = 1 #ps
for Slicelength in one_ps_array:
    for Nthslice in np.arange(1,int(TotalTime/Slicelength)+1):
        #print(Nthslice)
        
        sliced_array = slice(one_ps_data_array, Slicelength, StepSize, Nthslice)
        print("sliced_array:{}".format(sliced_array.shape))

        PCA_projection, Evalue = PCA(sliced_array)

        np.save("PCA_{}ps_{}ps_{}slice.npy".format(Slicelength, StepSize, Nthslice), PCA_projection)
        np.save("Evalue_{}ps_{}ps_{}slice.npy".format(Slicelength, StepSize, Nthslice), Evalue)

        print("PCA Saved! | {}".format("PCA_{}ps_{}ps_{}slice.npy".format(Slicelength, StepSize, Nthslice)))
        print("Evalue Saved! | {}".format("Evalue_{}ps_{}ps_{}slice.npy".format(Slicelength, StepSize, Nthslice)))



# Slice + PCA | 1ps 10000ps
TotalTime = 1000 #ps
StepSize = 0.1 #ps
for Slicelength in pointone_ps_array:
    for Nthslice in np.arange(1,int(TotalTime/Slicelength)+1):
        #print(Nthslice)
        
        sliced_array = slice(pointone_ps_data_array, Slicelength, StepSize, Nthslice)
        print("sliced_array:{}".format(sliced_array.shape))

        PCA_projection, Evalue = PCA(sliced_array)

        np.save("PCA_{}ps_{}ps_{}slice.npy".format(Slicelength, StepSize, Nthslice), PCA_projection)
        np.save("Evalue_{}ps_{}ps_{}slice.npy".format(Slicelength, StepSize, Nthslice), Evalue)

        print("PCA Saved! | {}".format("PCA_{}ps_{}ps_{}slice.npy".format(Slicelength, StepSize, Nthslice)))
        print("Evalue Saved! | {}".format("Evalue_{}ps_{}ps_{}slice.npy".format(Slicelength, StepSize, Nthslice)))

