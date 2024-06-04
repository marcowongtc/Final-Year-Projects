
import numpy 

dimensions = 4

all_possible_directions = numpy.stack(
numpy.meshgrid(*([-1, 0, 1],) * dimensions), -1
).reshape(-1, dimensions)


#a = numpy.meshgrid(*([-1, 0, 1],) * dimensions)
#b = numpy.meshgrid(([-1, 0, 1], [-1, 0, 1], [-1, 0, 1]))
#print(a)
#print(b)
#c = *([-1, 0, 1],) * dimensions
#print(c)

print(all_possible_directions)

###############

#all possible direction (3D)
'''
[[-1 -1 -1]
[-1 -1  0]
[-1 -1  1]
[-1  0 -1]
[-1  0  0]
[-1  0  1]
[-1  1 -1]
[-1  1  0]
[-1  1  1]
[ 0 -1 -1]
[ 0 -1  0]
[ 0 -1  1]
[ 0  0 -1]
[ 0  0  0]
[ 0  0  1]
[ 0  1 -1]
[ 0  1  0]
[ 0  1  1]
[ 1 -1 -1]
[ 1 -1  0]
[ 1 -1  1]
[ 1  0 -1]
[ 1  0  0]
[ 1  0  1]
[ 1  1 -1]
[ 1  1  0]
[ 1  1  1]]

'''
###############

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the coordinates for Set 1
x1 = np.array([1, 2, 3, 4, 5])
y1 = np.array([6, 7, 8, 9, 10])
z1 = np.array([11, 12, 13, 14, 15])

# Define the coordinates for Set 2
x2 = np.array([2, 4, 6, 8, 10])
y2 = np.array([3, 6, 9, 12, 15])
z2 = np.array([1, 4, 7, 10, 13])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot Set 1
ax.plot(x1, y1, z1, '-', label='Set 1')
# Plot Set 2
ax.plot(x2, y2, z2, '-', label='Set 2')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.title('Multiple Sets in 3D Plot')
plt.legend()
plt.show()