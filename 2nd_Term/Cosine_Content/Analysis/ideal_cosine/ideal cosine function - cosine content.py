import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
import sys



print("------------------------------------------")

N = 10000
NoPC = 50

ideal_cosine_content_array = np.zeros(NoPC)

print("ideal cosine content analysis:")
for current_NoPC in range(1,NoPC+1):
    # Define your dataset
    x = np.linspace(1,N,N)                               # x-values
    current_PC = np.cos(current_NoPC*np.pi*x/N)

    y1 = np.cos(current_NoPC*np.pi*x/N)*current_PC        # y1-values
    y2 = current_PC*current_PC                             # y2-values
    #print("x axis | {}: \n{}\n".format(x.shape, x))
    #print("y1 | {}: \n{}\n".format(y1.shape, y1))
    #print("y2 | {}: \n{}\n".format(y2.shape, y2))

    # Perform integration using the desired method
    int1 = integrate.trapz(y1, x)
    int2 = integrate.trapz(y2, x)
    cosine_content = (2.0/N)*int1*int1/int2   #2.0 needed if 2 -> set type to int
    print("Trapezoidal rule | PC{} | int1: {}, int2: {}, cosine content: {}\n".format(current_NoPC, int1, int2, cosine_content))

    ideal_cosine_content_array[current_NoPC-1] = cosine_content

print("------------------------------------------")

print("cosine content: {}".format(ideal_cosine_content_array))
# Plotting
plt.figure()
plt.title("Cosine Content of PC Trend | ideal cosine: {} steps".format(int(N)))
plt.ylabel("Cosine Content")
plt.xlabel("Principal Component Axis No.")

plt.ylim((0,1.5))

PC = np.arange(1, NoPC+1)

plt.plot(PC,ideal_cosine_content_array)

plt.legend()
plt.savefig("ideal_cosinefunction_PCtrend_cosine_{}PC.png".format(NoPC,N/1000))
plt.show()
