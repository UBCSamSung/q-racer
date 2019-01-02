import numpy as np
import math

# Return vector rotated CW by angle
def rotate(vector, angle):
    radians=math.radians(angle)
    c,s=np.cos(radians),np.sin(radians)
    M=np.array([[c,-s],[s,c]])
    return np.dot(M, vector)

def angle2vector(angle):
    return rotate([1,0], angle)

def vector2angle(vector):
    return math.degrees(math.atan2(vector[1], vector[0]))

# Return a function that take x position and return y position
def point2line(p1, p2, inverse=False):
    if inverse:
        p1=p1[::-1]
        p2=p2[::-1]
    return lambda x: (p2[0]-p1[0])/(p2[1]-p1[1])*(x-p1[1])+p1[0]
