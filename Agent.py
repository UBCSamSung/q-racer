import numpy as np

# template class for agent
# create classes that implement this for smarter agent
class Agent():
    def __init__(self):
        pass
    
    # take state and return action
    def get_action(self, state):
        return np.random.choice(['forward', 'backward', 'left', 'right', None], 1)