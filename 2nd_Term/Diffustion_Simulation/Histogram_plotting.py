import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.animation as animation


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



###############################
# Final Distance Histogram
###############################
# distance array (Np, Ns)
Distance_array = np.load("{}D_{}Np_{}Ns_distance.npy".format(D, Np, Ns))


plt.figure()
plt.title('Histogram of last distance from origin')
plt.xlabel('distance from origin')
plt.ylabel('Number')
max = np.max(Distance_array)
plt.hist(Distance_array[:,-1], np.arange(0, max+0.5))
plt.savefig("{}D_{}Np_{}Ns_distance_histogram.png".format(D, Np, Ns))
plt.show()



###############################
# Final x position Histogram
###############################

# Position array (D, Np, Ns)
Position_array = np.load("{}D_{}Np_{}Ns_position.npy".format(D, Np, Ns))

plt.figure()
plt.title('Histogram of last position x')
plt.xlabel('x')
plt.ylabel('Number')
range = np.max(np.abs(Position_array))
print(range)
plt.hist(Position_array[0,:,-1], np.arange(-range-0.5, range+0.5))
plt.savefig("{}D_{}Np_{}Ns_xpos_histogram.png".format(D, Np, Ns))
plt.show()


