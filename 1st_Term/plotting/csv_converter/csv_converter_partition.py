import numpy as np
import pandas as pd

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
partition_ratio_list = [0.2, 0.4, 0.6, 0.8]

for model in model_list:

    for partition_ratio in partition_ratio_list:

        imp_file = open("{}-model_{}-iter_{}-dist_{}-corr_{}-partition.csv".format(model, n_iteration, distance_cutoff, correlation_cutoff, partition_ratio), "rb")
        imp_array = np.loadtxt(imp_file, delimiter=',')


        #print(imp_array.shape)


        imp_word_array = ['Importance']
        imp_chain1_array = imp_array[0:295]
        imp_chain2_array = imp_array[295:]

        imp_chain1_array = np.concatenate((imp_word_array, imp_chain1_array), axis=0)
        imp_chain2_array = np.concatenate((imp_word_array, imp_chain2_array), axis=0)

        imp_chain1_array = imp_chain1_array.reshape(-1,1)
        imp_chain2_array = imp_chain2_array.reshape(-1,1)

        #print(imp_chain1_array.shape)
        #print(imp_chain2_array.shape)



        resid_word_array = ['ResID']
        resid_array = np.arange(35, 330) #35-329
        resid_array = np.concatenate((resid_word_array, resid_array), axis=0)
        resid_array = resid_array.reshape(-1,1)

        #print(resid_array.shape)



        result_chain1_array = np.hstack((resid_array, imp_chain1_array))
        result_chain2_array = np.hstack((resid_array, imp_chain2_array))

        #print(result_chain1_array)

        df1 = pd.DataFrame(result_chain1_array)
        df1.to_csv("{}-model_{}-iter_{}-dist_{}-corr_{}-partition_chain1.csv".format(model, n_iteration, distance_cutoff, correlation_cutoff, partition_ratio), index=False, header=False)

        df2 = pd.DataFrame(result_chain2_array)
        df2.to_csv("{}-model_{}-iter_{}-dist_{}-corr_{}-partition_chain2.csv".format(model, n_iteration, distance_cutoff, correlation_cutoff, partition_ratio), index=False, header=False)




        #np.savetxt("test1.csv", result_chain1_array, delimiter=",")
        #np.savetxt("test2.csv", result_chain2_array, delimiter=",")