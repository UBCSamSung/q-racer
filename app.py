import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from world import World
from test_maps import rectangle, straight
from Agent import Agent


# Initialize new world
world = World()
world.set_map(straight)
#world.set_map(rectangle)

# For demo:
world.add_racer(0)
world.racers[0].velocity=(0,1)

agents = []
agents.append(Agent())

# Game update
def gameUpdate(*args):
    state = world.get_state()
    actions=[agent.get_action(state) for agent in agents]
    world.update(actions)
    im.set_data(world.world_map)
    return im,

# Initialize renderer
screen = plt.figure()
im = plt.imshow(world.world_map, cmap='gray', vmin=0, vmax=255, animated=True)
ani = animation.FuncAnimation(screen, gameUpdate, frames=1000, interval=30, blit=False)
plt.show()