import numpy as np
import matplotlib.pyplot as plt


# variable
Np = 63
Ns = 10000

Plot_N = 5



# load data for plotting
#Position_array = np.load("{}Np_{}Ns_position.npy".format(Np, Ns))
transformed_position_array = np.load("{}Np_{}Ns_PCA_projection.npy".format(Np, Ns))
#E_value_array = np.load("{}Np_{}Ns_E_value.npy".format(Np, Ns))

#print("Position array: \n {} \n".format(Position_array))
print("PCA projection array: \n {} \n".format(transformed_position_array))
#print("Eigenvalue: \n {} \n".format(E_value_array))



# original position plotting
#plt.figure()
#plt.title("Position on original coordinate - {}Np {}Ns".format(Np, Ns))
#plt.xlabel("time")
#plt.ylabel("original coordinate")
#for i in np.arange(Plot_N):
#    plt.plot(Position_array[i, :], label = "x{}".format(i+1))
#plt.legend()
#plt.savefig("{}Np_{}Ns_time_plot.png".format(Np, Ns))
#plt.show()


print(transformed_position_array.shape)

# PCA projection plotting | subplot view
plt.figure(figsize=(7, Plot_N*2.5))

max = np.max(np.abs(transformed_position_array))

for i in np.arange(Plot_N):
    
    plt.subplot(Plot_N, 1, i+1)
    plt.plot(transformed_position_array[i, :]) 
    plt.plot(np.zeros(Ns), ls = '-.', color='grey') # dashed line at average position 0

    plt.ylim(-max, max)

    # label of subplot
    plt.ylabel("PC{}".format(i+1))
    plt.xlabel("time (ps)")


plt.suptitle("Projection on Principal Component")

plt.savefig("{}Np_{}Ns_{}PC_PCA_time_subplot.png".format(Np, Ns, Plot_N))
plt.show()


"""

# PCA projection plotting | one plot view
plt.figure()
plt.title("Projection on Principal Component ")
plt.ylabel("Projection")
plt.xlabel("steps")

for i in np.arange(Plot_N):
    plt.plot(transformed_position_array[i, :], label = "PC{}, sd = {:.2f}".format(i+1, E_value_array[i]))

plt.legend()
plt.savefig("{}Np_{}Ns_{}PC_PCA_time_plot.png".format(Np, Ns, Plot_N))
plt.show()


"""