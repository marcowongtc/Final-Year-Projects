import numpy as np
import matplotlib.pyplot as plt
import sys

# Parameter input
if len(sys.argv) > 4:
    # Retrieve the parameter value
    N = int(sys.argv[1])
    TL = int(sys.argv[2])
    ST = int(sys.argv[3])
    NoPCplot = int(sys.argv[4])       
    print("N:{}ps TL:{}ps ST:{}ps | NoPCplot:{} \n".format(N, TL, ST, NoPCplot))
else:
    print("parameters are not fully provided.")



# PCA Projection
PCA_projection = np.load("PCA_{}ns_1ps_{}TL_{}ST.npy".format(int(N/1000), int(TL/1000), int(ST/1000)))
Evalue_array = np.load("Evalue_{}ns_1ps_{}TL_{}ST.npy".format(int(N/1000), int(TL/1000), int(ST/1000)))

print("PCA projection: \nShape: {} \n{} \n".format(PCA_projection.shape, PCA_projection))
print("Eigenvalue: \nShape: {} \n {} \n".format(Evalue_array.shape, Evalue_array))






# PCA projection plotting | subplot view
plt.figure(figsize=(7, NoPCplot*2))

max = np.max(np.abs(PCA_projection))

for i in np.arange(NoPCplot):
    
    plt.subplot(NoPCplot, 1, i+1)
    plt.plot(PCA_projection[i, :]) 
    plt.plot(np.zeros(TL), ls = '-.', color='grey') # dashed line at average position 0

    plt.ylim(-max, max)

    # label of subplot
    plt.ylabel("PC{}".format(i+1))
    plt.xlabel("time (ps)")


plt.suptitle("Principal Component Projection | Time Length: {}ns ".format(int(TL/1000)))
plt.savefig("PCA_subplot_{}PC_{}ns_1ps_{}TL_{}ST.png".format(NoPCplot,int(N/1000), int(TL/1000), int(ST/1000)))
print("Plot Saved! | {}".format("PCA_subplot_{}PC_{}ns_1ps_{}TL_{}ST.png".format(NoPCplot,int(N/1000), int(TL/1000), int(ST/1000))))
#plt.show()


# PCA projection plotting | one plot view
plt.figure()
plt.title("Principal Component Projection | Time Length: {}ns ".format(int(TL/1000)))
plt.ylabel("Principle component projection")
plt.xlabel("time (ps)")

for i in np.arange(NoPCplot):
    plt.plot(PCA_projection[i, :], label = "PC{}, {:.2f}".format(i+1, Evalue_array[i]))

plt.legend()
plt.savefig("PCA_plot_{}PC_{}ns_1ps_{}TL_{}ST.png".format(NoPCplot,int(N/1000), int(TL/1000), int(ST/1000)))
print("Plot Saved! | {}".format("PCA_plot_{}PC_{}ns_1ps_{}TL_{}ST.png".format(NoPCplot,int(N/1000), int(TL/1000), int(ST/1000))))
#plt.show()

