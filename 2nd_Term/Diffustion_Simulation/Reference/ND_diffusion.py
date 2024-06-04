import copy
import math

import numpy
import matplotlib
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D


##################################################
# simulate_diffusion
##################################################
#-------------------------------------------------
# Variables
#-------------------------------------------------
# dimension | N |
#
# duration | N_t | 
# -> number of sampling period
#
# sampling period | t | 
# -> time for one sampling period
#
# number_particle | N_p | 
# -> number of particle
#
# diffusion_speed | T |
# -> probability time in a sampling period for a specific direction to occur
# -> N dimension: P = N * T / t  
#
# positions_init
# -> funciton name to be called 
# -> eg: positons_init_origin()
#
#-------------------------------------------------

def simulate_diffusion(
    dimensions,
    duration,
    sampling_period,
    number_particles,
    diffusion_speed,
    diffusion_model,
    diffusion_model_args,
    positions_init,
    positions_init_args,
):
    """Return nD positions of all particles for duration of simulation."""
    assert 0 < dimensions < 8
    assert sampling_period > diffusion_speed * (dimensions + 1) * 2


    #-----------------------------
    # Generate Direction array
    #-----------------------------

    #-------------------------------------------------
    # Direction Array
    #-------------------------------------------------
    # a look-up-table of directions to move | a set of direction with consideration of probability
    # row: one sampling period t   
    # column: dimension / coordinate 
    # Constraint: only one dimension movement for each sampling period
    #
    # diffusion speed: time length T for possible move within sampling time tau t 
    # -> P() = T/t  
    #
    # EG: 
    # [1, 0, -1, 1, 1]
    # [0, 0, 0, 0, 0]
    # [0, 0, 0, 0, 0]
    # 
    # 00000: T=2, t=3
    #
    # it will further accessed by random_number array with elements of indexes of direction array
    #-------------------------------------------------

    directions = numpy.zeros((sampling_period, dimensions), dtype=numpy.int32)

    
    #-------------------------------------------------
    # all_possible_directions:
    #-------------------------------------------------
    # generate combinations of all possible relative moves in all dimensions
    # row: possible combination i
    # column: coordinate j
    # 
    # numpy.meshgrid(*([-1, 0, 1],) * dimensions)
    # -> if dimension = 3:  ([-1, 0, 1], [-1, 0, 1], [-1, 0, 1]) 
    #
    # -> meshgrid: iterate all possible combination
    # -> 1st pos have 3 cadidates to loop, same as 2nd pos and 3rd pos
    #-------------------------------------------------
    
    all_possible_directions = numpy.stack(
        numpy.meshgrid(*([-1, 0, 1],) * dimensions), -1
    ).reshape(-1, dimensions)


    # Generate Direction Array

    index = 0
    for direction in all_possible_directions:

        
        # Only allow one dimension movement per sampling_period!
        # filter out possible move that contain more than one direction
        if numpy.sum(numpy.abs(direction)) != 1:
            continue

        # ----------------------------------------------------
        # Probability for N dimension | Definition
        #----------------------------------------------------
        # P() = NT / t
        # move the particle in the specified direction if random number is between "index" and "index + diffusion_speed * dimensions"
        # ----------------------------------------------------

        # Add specific direction N*T times in array of length of t
        directions[index : index + diffusion_speed * dimensions] = direction

        # Shift the index to position that is not appended the direction
        index += diffusion_speed * dimensions



    #-----------------------------
    # Generate Position Array
    #-----------------------------

    # get a random number between 0 and `sampling_period`
    # for all particles and sampling periods in the duration of the simulation
        
    # ----------------------------------------------------
    # random_numbers 
    # numpy.random.randint(x, S)
    # ----------------------------------------------------
    # generate array of random integers with size S from 0 to x (excluding)
    # -> row: Np, column: Nt | space represent different particle at different time
    # -> random index for accessing the direction array
    # ----------------------------------------------------
        
    random_numbers = numpy.random.randint(
        sampling_period, size=(number_particles, duration)
    )


    # index the first axis in the `directions` look-up-table with the random
    # numbers to obtain the relative moves of all particles for all sampling
    # periods

    # ----------------------------------------------------
    # random_moves
    # ----------------------------------------------------
    # numpy.take(x, y)
    # x: array for accessing
    # y: array containing index no. for accessing the array x
    # -> output | generate an array of given index number
    # -> our case | get all random movement for each sampling period for all particles
    # ----------------------------------------------------

    random_moves = numpy.take(directions, random_numbers, axis=0)




    # set the initial positions of particles | for the N_t = 0, all = 0
    positions_init(random_moves, **positions_init_args)

    # if not specify diffusion model | return random moves array
    if diffusion_model is None:
        return random_moves

    # if specify diffusion model | return cummulative walk / position array
    # calculate the positions of particles from the random moves using different diffusion model
    positions = diffusion_model(random_moves, **diffusion_model_args)
    return positions

##################################################
# simulate_diffusion
##################################################







def positions_init_origin(random_moves):
    """Set in-place initial position of particles to origin."""
    random_moves[:, 0] = 0


def diffusion_model_unconstrained(random_moves, **kwargs):
    """Diffusion with no constraints."""
    return numpy.cumsum(random_moves, axis=1)




def particle_counter_box(positions, counter_shape=None, counter_position=None):
    """Return number of particles in observation box over time.

    Also return the indices of particles that were counted.

    """
    dimensions = positions.shape[-1]
    if counter_shape is None:
        counter_shape = (1,) * dimensions  # one element
    if counter_position is None:
        counter_position = (0,) * dimensions  # center
    lower = tuple(p - s // 2 for p, s in zip(counter_position, counter_shape))
    upper = tuple(
        p + s // 2 + s % 2 for p, s in zip(counter_position, counter_shape)
    )
    in_box = numpy.all((positions >= lower) & (positions < upper), axis=-1)
    particle_counts = numpy.sum(in_box, axis=0)
    particles_counted = numpy.nonzero(numpy.any(in_box, axis=1))
    return particle_counts, particles_counted





def calculate_msd_d(positions):
    """Return mean square displacement and D of simulated positions."""
    number_particles, duration, dimensions = positions.shape
    msd = numpy.mean(
        numpy.square(positions - positions[:, 0:1, :]), axis=(0, -1)
    )
    time = numpy.arange(duration)[..., numpy.newaxis]
    slope = numpy.linalg.lstsq(time, msd, rcond=None)[0][0]
    d = slope / (2 * dimensions)
    return msd, d



def plot_positions(positions, selection=None, ax=None, title=None, label=None):
    """Plot positions of selected particles over duration of simulation."""
    number_particles, duration, dimensions = positions.shape
    if selection is None:
        selection = slice(1)  # first particle
    threed = dimensions > 2 and not isinstance(selection, int)
    ax_ = ax
    if ax is None:
        fig = pyplot.figure(figsize=(7.0, 7.0) if threed else None)
        ax = fig.add_subplot(111, projection='3d' if threed else None)
    if title is None:
        title = 'Selected particle positions'
    ax.set_title(title)
    if isinstance(selection, int):
        time = numpy.arange(duration)
        ax.set_xlabel('time')
        ax.set_ylabel('position')
        label = '' if label is None else label + ' '
        for i, dim in zip(range(dimensions - 1, -1, -1), 'xyzwvuts'):
            ax.plot(time, positions[selection, :, i], label=label + dim)
    elif dimensions == 1:
        time = numpy.arange(duration)
        ax.set_xlabel('time')
        ax.set_ylabel('x')
        for pos in positions[selection]:
            ax.plot(time, pos, label=label)
    elif dimensions == 2:
        ax.set_aspect('equal')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        for pos in positions[selection]:
            ax.plot(pos[:, 1], pos[:, 0], label=label)
    else:
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        for pos in positions[selection]:
            ax.plot(pos[:, 2], pos[:, 1], pos[:, 0], label=label)
    if label is not None:
        ax.legend()
    if ax_ is None:
        pyplot.show()


def plot_msd(msd, d, dimensions=None, ax=None, labels=('simulation', 'fit')):
    """Plot MSD and line fit."""
    duration = msd.shape[0]
    time = numpy.arange(duration)
    ax_ = ax
    if ax is None:
        fig = pyplot.figure()
        ax = fig.add_subplot(111)
    ax.set_title('MSD and line fit')
    ax.set_xlabel('time')
    ax.set_ylabel('MSD')
    try:
        label0, label1 = labels
    except Exception:
        label0, label1 = None, None
    if dimensions:
        ax.plot(time, msd, '.', label=label0)
        ax.plot(time, d * 2 * dimensions * time, '-', lw=3, label=label1)
    else:
        ax.plot(time, msd, label=label0)
    if label0 or label1:
        ax.legend()
    if ax_ is None:
        pyplot.show()






'''

def example_nd_simulations():
    """Compare diffusion in 1, 2, and 3 dimensions."""

    # create two empty plots
    plots = []
    for _ in range(2):
        fig = pyplot.figure()
        plots.append(fig.add_subplot(111))

    # iterate over dimensions 1 to 3
    for dimensions in range(1, 4):
        # define simulation parameters
        simulation_args = {
            'dimensions': dimensions,
            'duration': 2500,
            'sampling_period': 1000,
            'number_particles': 1000,
            'diffusion_speed': 10,
            'positions_init': positions_init_origin,
            'positions_init_args': {},
            'diffusion_model': diffusion_model_unconstrained,
            'diffusion_model_args': {},
        }


        # run simulation of model
        positions = simulate_diffusion(**simulation_args)

        # analyze positions and counted particles
        msd, D = calculate_msd_d(positions)

        # plot results of simulation and analysis
        label = str(dimensions) + 'D'
        plot_positions(positions, 0, ax=plots[0], label=label)
        plot_msd(
            msd,
            D,
            ax=plots[1],
            labels=(
                '{} D={:.3f}'.format(label, D * simulation_args["sampling_period"]),
                None,
            ),
        )

    pyplot.show()


example_nd_simulations()


'''

## modify!!!

def example_nd_simulations():
    """Compare diffusion in 1, 2, and 3 dimensions."""

    # create two empty plots
    fig = pyplot.figure(figsize=(7.0, 7.0))
    plot0 = fig.add_subplot(111, projection='3d')

    # define simulation parameters
    simulation_args = {
        'dimensions': 3,
        'duration': 2500,
        'sampling_period': 1000,
        'number_particles': 1000,
        'diffusion_speed': 10,
        'positions_init': positions_init_origin,
        'positions_init_args': {},
        'diffusion_model': diffusion_model_unconstrained,
        'diffusion_model_args': {},
    }


    # run simulation of model
    positions = simulate_diffusion(**simulation_args)


    # plot results of simulation and analysis
    label = '3D'
    plot_positions(positions, ax=plot0, label=label)

    pyplot.show()


example_nd_simulations()



#%time example_nd_simulations()