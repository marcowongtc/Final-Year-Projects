import numpy as np
from matplotlib import pyplot

#############################
#Variable defining!!
##############################

# Define some variables to control the simulation:
# number of particles
particles = 100000

# duration of the simulation, i.e. the number of sampling periods
duration = 1000

# the sampling period in arbitrary time units
sampling_period = 1000

# probability that a particle moves in a certain direction during the sampling
# period. Given in number of time units of the sampling period
diffusion_speed = 500

# Allocate a two-dimensional array of integers, which can store
# the positions of all particles during the simulation.
positions = np.zeros((particles, duration), dtype=np.int32)



#############################################
# Simulation!!!
#############################################

# Create a look-up-table of directions to move.
# This table will be indexed by random numbers in range 0 to `sampling_period`.
# TODO: the table can be extended by another axis to include movements
# in y and z directions.
directions = np.zeros(sampling_period, dtype=np.int32)

# move the particle in the positive direction
directions[0:diffusion_speed] = 1

# move the particle in the negative direction
directions[diffusion_speed : diffusion_speed * 2] = -1

# Run the simulation separately for all particles.
# TODO: this loop could be vectorized, i.e. below calculations could be done
# for all particles at once.
for particle in range(particles):
    # Get a random number between 0 and `sampling_period`
    # for all sampling periods in the duration of the simulation.
    random_numbers = np.random.randint(sampling_period, size=duration)

    # Index the first axis in the `directions` look-up-table with the random
    # numbers to obtain the relative moves of the particle for all sampling
    # periods.
    moves = np.take(directions, random_numbers, axis=0)

    # Set the first position of the particle to the origin
    # TODO: the initial position could be randomized.
    moves[0] = 0

    # Calculate all positions of the particle for the duration of the
    # simulation by cumulatively summing the relative moves.
    # The result is stored in the positions array.
    # TODO: to include obstacles in the simulation, the np.cumsum function
    # could be replaced by a custom function restricting movement in and
    # out of obstacles.
    positions[particle] = np.cumsum(moves, axis=0)


# Calculate the mean square displacement (MSD) at each sampling period
# by squaring all positions and averaging them over particles.
msd = np.mean(np.square(positions), axis=0)

# Calculate the diffusion coefficient D from the slope of the MSD values vs
# time. The slope is fitted by solving a linear equation system.

time = np.arange(duration)[..., np.newaxis] #row -> column vector

slope = np.linalg.lstsq(time, msd, rcond=None)[0][0] 
###############################
#[0][0]: get the best fitted line slope (m)
#[0]: get slope (m) and y intercept (c)
################################

D = slope / 2

#print Dt (MSD=2Dt for 1D case)
print(D * sampling_period)




#############################################
# Plot trajectory of selected particle 
#############################################


pyplot.figure()
pyplot.title('Selected particle positions')
pyplot.xlabel('time')
pyplot.ylabel('position')
for i in range(20):
    pyplot.plot(positions[i])
pyplot.show()


#############################################
# Plot histogram of last position of particles
#############################################

pyplot.figure()
pyplot.title('Histogram of last particle position')
pyplot.xlabel('position')
pyplot.ylabel('frequency')
minmax = np.max(np.abs(positions))

##############
# pyplot.hist(x, bins)
#
# x = input array into the histogram
# here we input the all particle last sampling positon
#
# bins = [1,2,3,4] <- bin value
# here we produce bins from -minmax - 0.5 to minmax + 0.5 with step 1 
#############

pyplot.hist(positions[:, -1], np.arange(-minmax - 0.5, minmax + 0.5))
pyplot.show()


#############################################
# MSD of the simulation! 
#############################################

pyplot.figure()
pyplot.title('MSD and linear fit')
pyplot.xlabel('time')
pyplot.ylabel('MSD')
pyplot.plot(time, msd, '.', label='simulation')
pyplot.plot(time, slope * time, '-', lw=3, label='fit')
pyplot.legend()
pyplot.show()