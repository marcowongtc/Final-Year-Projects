import numpy as np
#######################################
# Simulation variable and array
#######################################

# dimension 
D = 3

# No. of particle to simulate
Np = 21

# No. of Step 
Ns = 1000

# time interval
t = 1


#################################################
# array definition: (dimension, Particle Id, Step)


# direction array | determine the direction
# random generated array with size (Np, Ns) range from 0 to 1
Dir_array = np.random.rand(D, Np, Ns)
#print(Dir_array)

# turn elements where >= 0.5 into 1, otherwise into -1
Dir_array = np.where(Dir_array >= 0.5, 1, -1)
print(Dir_array)

# turn the first direction into 0
Dir_array[:,:,0] = 0
print(Dir_array)


# Step Size array 
StepSize_array = np.random.rand(D, Np, Ns)
#StepSize_array = np.ones((D,Np,Ns))
print(StepSize_array)


# Step array
# get each displacement for each step
Step_array = Dir_array * StepSize_array
print(Step_array)



# Position array (D, Np, Ns)
# cumulative sum along axis = 2, which is step no. axis | to get the real position
Position_array = np.cumsum(Step_array, axis = 2)
print(Position_array)


# distance array (Np, Ns)
# square whole array first then sum along dimension axis, then sqrt. 
Distance_array = np.sqrt(np.sum(np.square(Position_array), axis = 0))
print(Distance_array)

# mean square distance array (Ns) 
# square distance array then mean along particle id axis.
MSD_array = np.mean(np.square(Distance_array), axis = 0)
print(MSD_array)


#Saving array
np.save("{}D_{}Np_{}Ns_position.npy".format(D, Np, Ns), Position_array)
np.save("{}D_{}Np_{}Ns_distance.npy".format(D, Np, Ns), Distance_array)
np.save("{}D_{}Np_{}Ns_MSD.npy".format(D, Np, Ns), MSD_array)



