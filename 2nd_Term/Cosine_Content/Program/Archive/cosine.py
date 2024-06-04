import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

Np = 100
Ns = 10000

PCA_projection = np.load("{}Np_{}Ns_PCA_projection.npy".format(Np, Ns))
#PC1 = PCA_projection[0,:]
PC1 = PCA_projection[1,:]
#cosine_PC1 = PC1/np.max(np.abs(PC1))
cosine_PC1 = PC1


# Define your dataset
x = np.linspace(0,Ns-1,Ns)  # x-values
#y1 = np.cos(np.pi*x/Ns)*np.cos(np.pi*x/Ns) # y1-values
#y2 = y1                # y2-values
y1 = np.cos(2*np.pi*x/Ns)*cosine_PC1        # y1-values
y2 = cosine_PC1*cosine_PC1                # y2-values

# Perform integration using the desired method
int1 = integrate.trapz(y1, x)
int2 = integrate.trapz(y2, x)
cosine_content = (2.0/Ns)*int1*int1/int2   #2.0 needed if 2 -> set type to int
print("Trapezoidal rule | int1: {}, int2: {}, cosine content: {}".format(int1, int2, cosine_content))


int1 = integrate.simps(y1, x)
int2 = integrate.simps(y2, x)
cosine_content = (2.0/Ns)*int1*int1/int2
print("Simpson's rule | int1: {}, int2: {}, cosine content: {}".format(int1, int2, cosine_content))


plt.figure()
plt.title("PC1 - {}Ns".format(Ns))
plt.ylabel("PC1")
plt.xlabel("time")
plt.plot(cosine_PC1)
plt.plot(np.max(np.abs(PC1))*np.cos(2*np.pi*x/Ns))
plt.legend()
plt.show()