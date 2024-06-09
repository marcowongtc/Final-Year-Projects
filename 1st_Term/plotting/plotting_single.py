import numpy as np
import matplotlib.pyplot as plt


## variable set

# machine learning model set up
model = 'lr'
#model = 'rf'

# number of iterations on training & shuffling :: default: 20
n_iteration = 20

# remove residue candidates with heavy-atom min distance > :: default: 5.0A
distance_cutoff = 5.0

# correlation filtering during shuffle :: default: 0.9
correlation_cutoff = 0.9

# chain number 
chain_no_list = [1,2]

# IDlist
ID_list = []
ID = 1
while ID <= 590:
    ID_list.append(ID)
    ID += 1


# open the file in read binary mode
imp_file = open("{}-model_{}-iter_{}-dist_{}-corr.csv".format(model, n_iteration, distance_cutoff, correlation_cutoff), "rb")
imp_array = np.loadtxt(imp_file, delimiter=',')


for chain_no in chain_no_list:
    
    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot multiple lines
    ax.plot(ID_list, imp_array)
    #ax.plot(x, y2, label='Line 2')
    #ax.plot(x, y3, label='Line 3')

    # Set labels for x-axis and y-axis
    ax.set_xlabel('residue')
    ax.set_ylabel('importance')

    # Set title for the plot
    ax.set_title('{}-chain_{}-model_{}-iter_{}-dist_{}-corr'.format(chain_no, model, n_iteration, distance_cutoff, correlation_cutoff))

    # Set limit for axis
    if chain_no == 1:
        plt.xlim([1, 295]) 
    else:
        plt.xlim([296, 590]) 


    plt.ylim([0, 1])

    # Display the legend
    ax.legend()

    # Save the plot as an image file
    plt.savefig('{}-chain_{}-model_{}-iter_{}-dist_{}-corr.png'.format(chain_no, model, n_iteration, distance_cutoff, correlation_cutoff))

    # Display the plot
    #plt.show()

