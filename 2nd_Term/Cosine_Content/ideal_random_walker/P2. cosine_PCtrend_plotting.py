import numpy as np
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



# 10000 1000 1000 10 5

# cosine content PC trend Plot
#--------------------------------------------
cosine_array = np.load("cosine_{}PC_{}ns_1ps_{}TL_{}ST.npy".format(NoPC, int(N/1000), int(TL/1000), int(ST/1000)))



print("cosine_array: {}".format(cosine_array))
print("Shape: {}".format(cosine_array.shape))


# Plotting
plt.figure()
plt.title("Cosine Content | Random Walker: {} steps".format(int(N)))
plt.ylabel("Cosine Content")
plt.xlabel("Principal Component Index n")

PC = np.arange(1, NoPC+1)

plt.plot(PC,cosine_array)

plt.legend()
plt.savefig("ideal_PCtrend_cosine_{}PC_{}ns_1ps.png".format(NoPC,N/1000))
plt.show()


