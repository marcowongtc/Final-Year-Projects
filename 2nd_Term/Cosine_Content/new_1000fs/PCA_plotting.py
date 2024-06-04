import numpy as np
import matplotlib.pyplot as plt
from PCA_function import PCA_slice_plot

#------------------------------------
# PCA plotting: 
# PCA_projection: PCA of sliced array
# Evalue_array: Evalue of sliced array
# Slicelength (ps): length of slicing
# Step size (ps): 1ps / 0.1ps
# Nthslice: Nth slice we desired to plot
# NoPCplot: No of PC to be plotted
#------------------------------------

# time length in ps
one_ps_array = [100, 200, 500, 1000, 2000, 5000, 10000]
pointone_ps_array = [10, 20, 50, 100, 200, 500, 1000]


# PCA plotting | 1ps 10000ps
TotalTime = 10000 #ps
StepSize = 1 #ps
NoPCplot = 5 #no. of PC to be plotted
for Slicelength in one_ps_array:
    for Nthslice in np.arange(1,int(TotalTime/Slicelength)+1):
        PCA_projection = np.load("../PCA_Evalue/PCA_{}ps_{}ps_{}slice.npy".format(Slicelength, StepSize, Nthslice))
        Evalue = np.load("../PCA_Evalue/Evalue_{}ps_{}ps_{}slice.npy".format(Slicelength, StepSize, Nthslice))
        PCA_slice_plot(PCA_projection, Evalue, Slicelength, StepSize, Nthslice, NoPCplot = 5)



# PCA plotting | 1ps 10000ps
TotalTime = 1000 #ps
StepSize = 0.1 #ps
NoPCplot = 5 #no. of PC to be plotted
for Slicelength in pointone_ps_array:
    for Nthslice in np.arange(1,int(TotalTime/Slicelength)+1):
        PCA_projection = np.load("../PCA_Evalue/PCA_{}ps_{}ps_{}slice.npy".format(Slicelength, StepSize, Nthslice))
        Evalue = np.load("../PCA_Evalue/Evalue_{}ps_{}ps_{}slice.npy".format(Slicelength, StepSize, Nthslice))
        PCA_slice_plot(PCA_projection, Evalue, Slicelength, StepSize, Nthslice, NoPCplot = 5)

