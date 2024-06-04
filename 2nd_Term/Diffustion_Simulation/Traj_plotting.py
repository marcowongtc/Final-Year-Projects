import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#######################################
# Simulation variable and array
#######################################

# dimension 
D = 3

# No. of particle to simulate
Np = 1000

# No. of Step 
Ns = 1000

# time interval
t = 1

# No. of particle selected to plot 
SelNo = 3



###############################
# Distance Trajectory
###############################
"""

# distance array (Np, Ns)
Distance_array = np.load("{}D_{}Np_{}Ns_distance.npy".format(D, Np, Ns))

plt.figure()
plt.title('Selected particle positions')
plt.xlabel('time')
plt.ylabel('distance')
for i in range(SelNo):
    plt.plot(Distance_array[i])

plt.savefig("{}D_{}Np_{}Ns_distance_trajectory.png".format(D, Np, Ns))
plt.show()

"""

################################
# Postion Trajectory
################################

# Position array (D, Np, Ns)
Position_array = np.load("{}D_{}Np_{}Ns_position.npy".format(D, Np, Ns))

fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')


for id in np.arange(SelNo):
    x = Position_array[0,id,0:200]
    y = Position_array[1,id,0:200]
    z = Position_array[2,id,0:200]
    ax.plot(x,y,z,'-')


ax.set_title('Particle Trajectory | Random Walker')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')


plt.legend()
plt.savefig("{}D_{}Np_{}Ns_Position_trajectory_3.png".format(D, Np, Ns))
plt.show()




