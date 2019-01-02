import numpy as np

# template class for agent
# create classes that implement this for smarter agent
class Agent():
    def __init__(self):
        pass
    
    # take state and return action
    def get_action(self, state):
        return np.random.choice(['forward', 'backward', 'left', 'right', None], 1)

class GeneAgent():
    def __init__(self, actionList):
        self.actions = actionList
        self.nextAction = 0
    
    def get_action(self, state):
        availableActions = ['forward', 'backward', 'left', 'right', None]

        action = None
        if self.nextAction < len(self.actions):
            action = availableActions[self.actions[self.nextAction]]
            self.nextAction += 1
        
        return action
