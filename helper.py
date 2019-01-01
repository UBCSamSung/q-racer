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