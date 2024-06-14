import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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
SelNo = 21



# Position array (D, Np, Ns)
Position_array = np.load("{}D_{}Np_{}Ns_position.npy".format(D, Np, Ns))

# Plot details
fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')


# number of frame
Nf = 1000
N_list = np.arange(0, Nf+1)


#c = [0.0, 0.0, float(k)/float(max(k_list))]
#color = [0.0, 0.0, float(id+1)/float(SelNo)]
color_array = ["red","blue", "green"]
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

def init():
    plt.cla()

def run(n_c):
    plt.cla()
    for id in np.arange(SelNo):
        x = Position_array[0,id,0:n_c]
        y = Position_array[1,id,0:n_c]
        z = Position_array[2,id,0:n_c]

        # red green blue | alternating
        #colorid = np.mod(id, 3)
        #ax.plot(x,y,z,'-', color = color_array[colorid])

        # color gradient
        ax.plot(x,y,z,'-', color = [0.0, 0.0, float(id+1)/float(SelNo)])
        #ax.plot(x,y,z,'-', color = cycle[id])

        del x, y, z

    ax.set_title('Particle Trajectory | Random Walker')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')


    

ani = animation.FuncAnimation(fig, run, frames=N_list, interval=30, init_func=init, repeat = True)

ani.save('random_3D_{}_1000.mp4'.format(SelNo))
plt.show()




