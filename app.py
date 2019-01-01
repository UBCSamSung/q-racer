import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from world import World
from test_maps import rectangle

# Initialize new world
world = World()
# For demo:
world.add_racer((5,5), 0)
world.world_map = rectangle
last_state=None

# Game update
def gameUpdate(*args):
    state = world.get_state()
    if last_state and state[1]==last_state[1]:
        # stuck somewhere
        world.update([np.random.choice(['backward'], 1)])
    else:
        # not stuck. accelerate
        world.update([np.random.choice(['forward', 'left', 'right'], 1)])
    im.set_data(world.world_map)
    return im,

# Initialize renderer
screen = plt.figure()
im = plt.imshow(world.world_map, cmap='gray', vmin=0, vmax=255, animated=True)
ani = animation.FuncAnimation(screen, gameUpdate, frames=1000, interval=1, blit=False)
plt.show()