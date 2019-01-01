import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from world import World
from test_maps import rectangle

# Initialize new world
world = World()
world.world_map = rectangle

# Game update
def gameUpdate(*args):
    im.set_data(world.world_map)
    return im,

# Initialize renderer
screen = plt.figure()
im = plt.imshow(world.world_map, cmap='gray', vmin=0, vmax=255, animated=True)
ani = animation.FuncAnimation(screen, gameUpdate, frames=1000, interval=1, blit=False)
plt.show()