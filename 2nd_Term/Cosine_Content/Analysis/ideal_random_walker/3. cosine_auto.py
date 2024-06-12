import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
import sys

# Parameter input
if len(sys.argv) > 4:
    # Retrieve the parameter value
    N = int(sys.argv[1])
    TL = int(sys.argv[2])
    ST = int(sys.argv[3])
    NoPC = int(sys.argv[4])       
    print("N:{}ps TL:{}ps ST:{}ps | NoPC:{}".format(N, TL, ST, NoPC))
else:
    print("parameters are not fully provided.")




# PCA Projection
PCA_projection = np.load("PCA_{}ns_1ps_{}TL_{}ST.npy".format(int(N/1000), int(TL/1000), int(ST/1000)))
cosine_content_array = np.zeros(NoPC)


#shape of position array
PCA_shape = PCA_projection.shape
Np = PCA_shape[0]
Ns = PCA_shape[1]
print("Data array: \n {} \n".format(PCA_projection))
print("Shape: {} \n".format(PCA_shape))



#cosine content
for current_NoPC in range(1,NoPC+1):
    #print("------------------------------------------")
    print("PC{} cosine content analysis:".format(current_NoPC))
    current_PC = PCA_projection[current_NoPC-1,:]


    # Define your dataset
    x = np.linspace(1,Ns,Ns)                               # x-values
    y1 = np.cos(current_NoPC*np.pi*x/Ns)*current_PC        # y1-values
    y2 = current_PC*current_PC                             # y2-values
    #print("x axis | {}: \n{}\n".format(x.shape, x))
    #print("y1 | {}: \n{}\n".format(y1.shape, y1))
    #print("y2 | {}: \n{}\n".format(y2.shape, y2))

    # Perform integration using the desired method
    int1 = integrate.trapz(y1, x)
    int2 = integrate.trapz(y2, x)
    cosine_content = (2.0/Ns)*int1*int1/int2   #2.0 needed if 2 -> set type to int
    print("Trapezoidal rule | PC{} | int1: {}, int2: {}, cosine content: {}\n".format(current_NoPC, int1, int2, cosine_content))

    cosine_content_array[current_NoPC-1] = cosine_content

print("cosine_content_{}PC_array: \n{}\n".format(NoPC, cosine_content_array))



# save array for plotting
np.save("cosine_{}PC_{}ns_1ps_{}TL_{}ST.npy".format(NoPC, int(N/1000), int(TL/1000), int(ST/1000)), cosine_content_array)
print("Data Saved! | {}".format("cosine_{}PC_{}ns_1ps_{}TL_{}ST.npy".format(NoPC, int(N/1000), int(TL/1000), int(ST/1000))))
print("-----------------------------------------------------------------------")




"""
print("------------------------------------------")

print("ideal cosine content analysis:")
for current_NoPC in range(1,NoPC+1):
    # Define your dataset
    x = np.linspace(1,Ns,Ns)                               # x-values
    current_PC = np.cos(current_NoPC*np.pi*x/Ns)

    y1 = np.cos(current_NoPC*np.pi*x/Ns)*current_PC        # y1-values
    y2 = current_PC*current_PC                             # y2-values
    #print("x axis | {}: \n{}\n".format(x.shape, x))
    #print("y1 | {}: \n{}\n".format(y1.shape, y1))
    #print("y2 | {}: \n{}\n".format(y2.shape, y2))

    # Perform integration using the desired method
    int1 = integrate.trapz(y1, x)
    int2 = integrate.trapz(y2, x)
    cosine_content = (2.0/Ns)*int1*int1/int2   #2.0 needed if 2 -> set type to int
    print("Trapezoidal rule | PC{} | int1: {}, int2: {}, cosine content: {}\n".format(current_NoPC, int1, int2, cosine_content))

    cosine_content_array[current_NoPC-1] = cosine_content

print("------------------------------------------")
"""