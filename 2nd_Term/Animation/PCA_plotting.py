import numpy as np
import matplotlib.pyplot as plt


# variable
N = 10000

Plot_N = 5

A = 10
y = np.empty((5,N))
x = np.linspace(0,N,N)
for i in np.arange(0,5):
    y[i,:] = A/(i+1)*np.cos((i+1)*np.pi*x/N)



print(y.shape)

# PCA projection plotting | subplot view
plt.figure(figsize=(7, Plot_N*2.5))

max = np.max(np.abs(y))

for i in np.arange(Plot_N):
    
    plt.subplot(Plot_N, 1, i+1)
    plt.plot(y[i, :]) 
    plt.plot(np.zeros(N), ls = '-.', color='grey') # dashed line at average position 0

    plt.ylim(-max, max)

    # label of subplot
    plt.ylabel("PC{}".format(i+1))
    plt.xlabel("time")


plt.suptitle("Projection on Principal Component")

plt.savefig("ideal_PCA_time_subplot.png")
plt.show()


"""

# PCA projection plotting | one plot view
plt.figure()
plt.title("Projection on Principal Component ")
plt.ylabel("Projection")
plt.xlabel("steps")

for i in np.arange(Plot_N):
    plt.plot(y[i, :], label = "PC{}, sd = {:.2f}".format(i+1, E_value_array[i]))

plt.legend()
plt.savefig("{}Np_{}Ns_{}PC_PCA_time_plot.png".format(Np, Ns, Plot_N))
plt.show()


"""