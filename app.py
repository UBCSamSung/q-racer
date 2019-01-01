import threading
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from world import World

RESOLUTION = 1

world = World()

def gameUpdate(*args):
    im.set_data(world.world_map)
    return im,

screen = plt.figure()

im = plt.imshow(world.world_map, cmap='gray', vmin=0, vmax=255, animated=True)
ani = animation.FuncAnimation(screen, gameUpdate, frames=1000, interval=1, blit=False)
plt.show()