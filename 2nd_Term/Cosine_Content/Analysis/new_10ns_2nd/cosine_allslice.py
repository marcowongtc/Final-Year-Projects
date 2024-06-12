import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from cosine_function import cosine_content


#------------------------------------
# cosine_analysis function: 
# ps_array: time length array for analysis [100, 200, 500, ...]
# TotalTime: 10000 / 1000 ps 
# StepSize: 1 / 0.1ps
#------------------------------------

def cosine_analysis(ps_array, TotalTime, StepSize):

    cosine_mean_array = np.zeros((5,1)) #dummy array for concantenate | will remove at last
    cosine_dev_array = np.zeros((5,1)) #dummy array for concantenate | will remove at last

    for Slicelength in ps_array:

        # Define Cosine all slice array (TotPCNo, NoSlice)
        cosine_allslice_array = np.zeros((TotPCNo, int(TotalTime/Slicelength)))
        
        for Nthslice in np.arange(1,int(TotalTime/Slicelength)+1):
            PCA_projection = np.load("../PCA_Evalue/PCA_{}ps_{}ps_{}slice.npy".format(Slicelength, StepSize, Nthslice))

            for PCNo in np.arange(1,TotPCNo+1):
                #------------------------------------
                # cosine_content function: 
                # PCA_projection: transformed data
                # PCNo: nth PC to be analyzed
                #------------------------------------
                cosine_allslice_array[PCNo-1, Nthslice-1] = cosine_content(PCA_projection, PCNo)
                print("{}ps | {}th slice done \n").format(Slicelength, Nthslice)


        # Cosine Content all slice | Calcualtion Done!
        print("cosine_allslice | {}ps \n {} \n".format(Slicelength, cosine_allslice_array))

        # Cosine mean and dev
        print("mean : \n {}\n".format(np.mean(cosine_allslice_array, axis=1).reshape(-1,1)))
        print("deviation: \n {}\n".format(np.std(cosine_allslice_array, axis=1).reshape(-1,1)))

        cosine_mean_array = np.concatenate((cosine_mean_array, np.mean(cosine_allslice_array, axis=1).reshape(-1,1)), axis=1)
        cosine_dev_array = np.concatenate((cosine_dev_array, np.std(cosine_allslice_array, axis=1).reshape(-1,1)), axis=1)

        #np.save("cosine_allslice_{}ps_{}ps.npy".format(Slicelength, StepSize), cosine_allslice_array)

    # remove dummy zeros array
    cosine_mean_array = cosine_mean_array[:,1:]
    cosine_dev_array = cosine_dev_array[:,1:]

    print("mean | 1ps: \n {}\n".format(cosine_mean_array))
    print("deviation | 1ps: \n {}\n".format(cosine_dev_array))

    np.save("cosine_mean_{}ps_{}ps.npy".format(TotalTime, ps_array), cosine_mean_array)
    np.save("cosine_dev_{}ps_{}ps.npy".format(TotalTime, ps_array), cosine_dev_array)
    print("Data Saved! | {}".format("cosine_mean_{}ps_{}ps.npy".format(TotalTime, ps_array)))
    print("Data Saved! | {}".format("cosine_dev_{}ps_{}ps.npy".format(TotalTime, ps_array)))

    return cosine_mean_array, cosine_dev_array


# Slice length in ps
one_ps_array = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
TotPCNo = 5

mean_1ps, dev_1ps = cosine_analysis(one_ps_array, 10000, 1)


print("all | mean \n {}\n".format(mean_1ps))
print("all | dev \n {}\n".format(dev_1ps))



np.save("cosine_mean_all.npy", mean_1ps)
np.save("cosine_dev_all.npy", dev_1ps)
print("Data Saved! | cosine_mean_all.npy")
print("Data Saved! | cosine_dev_all.npy")