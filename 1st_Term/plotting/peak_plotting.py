import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


## variable set

# machine learning model set up
model = 'lr'

# number of iterations on training & shuffling :: default: 20
n_iteration = 20

# remove residue candidates with heavy-atom min distance > :: default: 5.0A
distance_cutoff_list = [3.0, 5.0, 7.0, 9.0, 11.0, 13.0]

# correlation filtering during shuffle :: default: 0.9
correlation_cutoff = 0.9

# chain number 
chain_no = 2

#Target residue No. for plotting | in one graph
plotting_id_list = [311]



#plotting parameter
x_plotting = distance_cutoff_list
x_label = "distance cutoff"





# Plotting!!!!!
# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 4))
#fig, ax = plt.subplots()


for plotting_id in plotting_id_list:

    y_plotting = np.array([])

    for distance_cutoff in distance_cutoff_list:
    
        # open the file 
        df = pd.read_csv("{}-model_{}-iter_{}-dist_{}-corr_chain{}.csv".format(model, n_iteration, distance_cutoff, correlation_cutoff, chain_no))
        imp_array = df.values #only extract elements wiht values

        #print(imp_array)

        y_plotting = np.append(y_plotting, imp_array[plotting_id-35, 1])
        print(y_plotting)
        #print(plotting_id-35)
        #print(x_plotting)

    ax.plot(x_plotting, y_plotting, label = 'resid = {}'.format(plotting_id))

# Set labels for x-axis and y-axis
ax.set_xlabel(x_label) 
ax.set_ylabel('importance')

# Set title for the plot
ax.set_title('{}-chain {}-model {} trend'.format(chain_no, model, x_label))

# Set limit for axis
plt.xlim([x_plotting[0], x_plotting[-1]]) 
plt.ylim([0, 1])

# Display the legend
ax.legend()

# Save the plot as an image file
plt.savefig('../../figure/trend/{}-chain_{}-model {}-{} {}-id_peakplot.png'.format(chain_no, model, x_plotting, x_label, plotting_id_list))

# Display the plot 
#plt.show()






    





