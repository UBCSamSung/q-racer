import numpy as np

class Racer():
    def __init__(self):
        self.position=(0,0)
        self.velocity=(0,0)
        self.direction=0
        self.lap=0
        self.instruction=None

class World():
    def __init__(self):
        map_height=500
        map_width=1000
        self.racers=[]
        self.world_map=np.zeros([map_height, map_width], dtype=np.uint8)
        
    def get_state(self):
        return {
            'racers': self.racers,
            'world_map': self.world_map
        }
    
    def update(self, agent_inputs=None):
        if agent_inputs:
            for index, agent_input in enumerate(agent_inputs):
                self.racers.instruction = agent_input
        for racer in self.racers:
            self.update_racer(racer)
    
    def update_racer(self, racer):
        # TODO
        pass
        
    # Return True if collision occur, else return False
    def check_collision(self, old_position, new_position):
        if self.world_map[new_position]!=0:
            return True
        return False
