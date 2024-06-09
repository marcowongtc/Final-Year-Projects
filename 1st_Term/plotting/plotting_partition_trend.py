import numpy as np
import matplotlib.pyplot as plt


## variable set

# machine learning model set up
model_list = ['lr', 'rf']

# number of iterations on training & shuffling :: default: 20
n_iteration = 20

# remove residue candidates with heavy-atom min distance > :: default: 5.0A
distance_cutoff = 5.0

# correlation filtering during shuffle :: default: 0.9
correlation_cutoff = 0.9


# cvpartition test:train ratio :: default: 0.4
partition_ratio_list = [0.2, 0.4, 0.6]

# chain number 
chain_no_list = [1,2]



# IDlist
ID_list = []
ID = 35
while ID <= 329:
    ID_list.append(ID)
    ID += 1



# Plotting!!!!!
for model in model_list:

    for chain_no in chain_no_list:

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(10, 4))
    
        for partition_ratio in partition_ratio_list:

            # open the file in read binary mode
            imp_file = open("{}-model_{}-iter_{}-dist_{}-corr_{}-partition.csv".format(model, n_iteration, distance_cutoff, correlation_cutoff, partition_ratio), "rb")
            imp_array = np.loadtxt(imp_file, delimiter=',')
    

            # Plot multiple lines
            if chain_no == 1:
                ax.plot(ID_list, imp_array[0:295], label = 'p = {}'.format(partition_ratio)) #get 1-295
            if chain_no == 2:
                ax.plot(ID_list, imp_array[295:], label = 'p = {}'.format(partition_ratio)) #get 295-590


        # Set labels for x-axis and y-axis
        ax.set_xlabel('residue')
        ax.set_ylabel('importance')

        # Set title for the plot
        ax.set_title('{}-chain_{}-model partition trend'.format(chain_no, model))

        # Set limit for axis
        plt.xlim([35, 329]) 
        plt.ylim([0, 1])

    
        # Display the legend
        plt.legend()

        # Save the plot as an image file
        plt.savefig('{}-chain_{}-model_partition_{}_plot.png'.format(chain_no, model, partition_ratio_list))

        # Display the plot
        #plt.show()

