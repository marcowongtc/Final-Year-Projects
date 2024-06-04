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
    print("N:{}ps TLincr:{}ps STincr:{}ps NoPC:{} | PC to be plotted: {}\n".format(N, TLincr, STincr, NoPC, NoPCplot))
else:
    print("parameters are not fully provided.")

#10000 1000 1000 10 5

# TL cosine Plot
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
plt.title("Time Length Cosine Content Analysis | Total Time Lenght: {}ns".format(int(N/1000)))
plt.ylabel("Cosine Content")
plt.xlabel("Time Length (ns)")

t = np.arange(1, N/TLincr+1)

for current_NoPC in np.arange(1, NoPCplot+1):
    plt.plot(t,TL_cosine_array[:, current_NoPC-1], label = "PC{}".format(current_NoPC))

plt.legend()
plt.savefig("TL_cosine_{}PC_{}ns_1ps.png".format(NoPCplot,N/1000))
plt.show()


# ST cosine Plot
#--------------------------------------------
#Data Import
ST_cosine_array = np.zeros((N/STincr, NoPC))
TL = 1
for ST in range(N/STincr):
    print("Start Time:{}ns".format(ST*1000))
    current_cosine_array = np.load("cosine_{}PC_{}ns_1ps_{}TL_{}ST.npy".format(NoPC, int(N/1000), int(TL), int(ST)))
    #print("cosine_array: {}".format(current_cosine_array))
    ST_cosine_array[ST] = current_cosine_array

print("ST_cosine_array: {}".format(ST_cosine_array))
print("Shape: {}".format(ST_cosine_array.shape))


# Plotting
plt.figure()
plt.title("Start Time Cosine Content Analysis | Total Time Lenght: {}ns".format(int(N/1000)))
plt.ylabel("Cosine Content")
plt.xlabel("Start Time (ns)")

t = np.arange(N/STincr)

for current_NoPC in np.arange(1, NoPCplot+1):
    plt.plot(t,ST_cosine_array[:, current_NoPC-1], label = "PC{}".format(current_NoPC))

plt.legend()
plt.savefig("ST_cosine_{}PC_{}ns_1ps.png".format(NoPCplot,N/1000))
plt.show()