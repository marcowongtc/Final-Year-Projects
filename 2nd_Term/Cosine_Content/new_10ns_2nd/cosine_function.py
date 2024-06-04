import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

#------------------------------------
# cosine_content function: 
# PCA_projection: transformed data
# PCNo: nth PC to be analyzed
#------------------------------------

def cosine_content(PCA_projection, PCNo):

    #cosine content
    #shape of PCA array
    PCA_shape = PCA_projection.shape
    Np = PCA_shape[0]
    Ns = PCA_shape[1]

    print("PC{} cosine content analysis:".format(PCNo))
    current_PC = PCA_projection[PCNo-1,:]


    # Define your dataset
    x = np.linspace(1,Ns,Ns)                               # x-values
    y1 = np.cos(PCNo*np.pi*x/Ns)*current_PC                # y1-values
    y2 = current_PC*current_PC                             # y2-values

    # Perform integration using the desired method
    int1 = integrate.trapz(y1, x)
    int2 = integrate.trapz(y2, x)
    cosine_content = (2.0/Ns)*int1*int1/int2   #2.0 needed if 2 -> set type to int
    print("Trapezoidal rule | PC{} | int1: {}, int2: {}, cosine content: {}".format(PCNo, int1, int2, cosine_content))

    return cosine_content

