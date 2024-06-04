import numpy as np
import matplotlib
from matplotlib import pyplot as plt

#######################################
# Simulation variable and array
#######################################

# dimension 
D = 3

# No. of particle to simulate
Np = 10000

# No. of Step 
Ns = 10000

# time interval
t = 1

# No. of particle selected to plot 
SelNo = 5


#############################################
# MSD of the simulation! 
#############################################

# MSD array
time_array = np.arange(Ns)
MSD_array = np.load("{}D_{}Np_{}Ns_MSD.npy".format(D, Np, Ns))


# slope of MSD against time
# function require a column matrix of time (reshaped!) 

m = np.linalg.lstsq(time_array.reshape(Ns,1), MSD_array, rcond= None)[0][0]
Dc = m/6
print("Slope = {}".format(m,m))
print("Diffusion coefficient = {}".format(Dc))

plt.figure()
plt.title('MSD and linear fit')
plt.xlabel('time')
plt.ylabel('MSD')
plt.legend()

plt.plot(time_array, MSD_array, '-', label = 'simulation')
plt.savefig("{}D_{}Np_{}Ns_MSD.png".format(D, Np, Ns))

plt.plot(time_array, m*time_array, '-', label = 'best fitted line')
plt.savefig("{}D_{}Np_{}Ns_MSD_bestfittedline.png".format(D, Np, Ns))

plt.show()

