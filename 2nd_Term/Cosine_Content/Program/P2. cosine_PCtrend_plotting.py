import numpy as np
import matplotlib.pyplot as plt
import sys

# Parameter input
if len(sys.argv) > 5:
    # Retrieve the parameter value
    N = int(sys.argv[1])
    TLincr = int(sys.argv[2])
    STincr = int(sys.argv[3])
    NoPC = int(sys.argv[4])
    NoPCplot = int(sys.argv[5])       
    print("N:{}ps TLincr:{}ps STincr:{}ps NoPC:{} | PC to be plotted: {}".format(N, TLincr, STincr, NoPC, NoPCplot))
else:
    print("parameters are not fully provided.")

# 10000 1000 1000 10 5

# cosine content PC trend Plot
#--------------------------------------------
#Data Import
TL_cosine_array = np.zeros((N/TLincr, NoPC))
ST = 0
for TL in range(1,N/TLincr+1):
    current_cosine_array = np.load("cosine_{}PC_{}ns_1ps_{}TL_{}ST.npy".format(NoPC, int(N/1000), int(TL), int(ST)))
    #print("Time length: {}".format(TL*1000))
    #print("cosine_array: {}".format(current_cosine_array))
    TL_cosine_array[TL-1] = current_cosine_array

print("TL_cosine_array: {}".format(TL_cosine_array))
print("Shape: {}".format(TL_cosine_array.shape))


# Plotting
plt.figure()
plt.title("Cosine Content Analysis of PC Trend | Total Time Lenght: {}ns".format(int(N/1000)))
plt.ylabel("Cosine Content")
plt.xlabel("Principal Component Axis No.")

t = np.arange(1, NoPCplot+1)

for TL_index in np.arange(N/TLincr):
    plt.plot(t,TL_cosine_array[TL_index, :NoPCplot], label = "TL:{}ns".format(TL_index+1))

plt.legend()
plt.savefig("PCtrend_cosine_{}PC_{}ns_1ps.png".format(NoPCplot,N/1000))
plt.show()


