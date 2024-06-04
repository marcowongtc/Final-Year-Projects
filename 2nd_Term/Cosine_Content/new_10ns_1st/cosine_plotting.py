import numpy as np
import matplotlib.pyplot as plt

all_ps_array = np.array([10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]).astype(float)
#print(all_ps_array/1000)

cosine_mean_all_array = np.load("cosine_mean_all.npy")
cosine_dev_all_array = np.load("cosine_dev_all.npy")


# PCA projection plotting | one plot view
for PC in np.arange(1,5+1):

    plt.figure()
    plt.title("Cosine Content Analysis - ps scale | PC{}".format(PC))
    plt.ylabel("Cosine Content")
    plt.xlabel("simulation time length (ps)")
    plt.xscale("log")
    x = all_ps_array[:9]
    y = cosine_mean_all_array[PC-1,:9]
    y_error = cosine_dev_all_array[PC-1,:9]

    plt.plot(x, y)
    plt.errorbar(x, y, yerr=y_error, fmt='none', capsize=4, color='red')

    #plt.legend()

    plt.savefig("cosine_plot_{}PC_ps_new.png".format(PC))
    print("Plot Saved! | {}".format("cosine_plot_{}PC_ps_new.png".format(PC)))
    #plt.close()
