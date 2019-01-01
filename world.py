import numpy as np

WALL=0
ROAD=255
CAR=128
LINE=200

class Racer():
    def __init__(self, position, direction, last_elem):
        self.position=position
        self.velocity=(0,0)
        self.direction=direction
        self.lap=0
        self.instruction=None
        self.last_elem=last_elem

class World():
    def __init__(self):
        self.racers=[]
        self.world_map=None

    def set_map(self, map):
        self.world_map = map

    def get_state(self):
        return {
            'racers': self.racers,
            'world_map': self.world_map
        }
    
    def add_racer(self, position, direction):
        last_elem=self.world_map[position]
        racer = Racer(position, direction, last_elem)
        self.racers.append(racer)
    
    def update(self, agent_inputs=None):
        if agent_inputs:
            for index, agent_input in enumerate(agent_inputs):
                self.racers.instruction = agent_input
        for racer in self.racers:
            self.update_racer(racer)
        # self.world_map[:]=255
    
    def update_racer(self, racer):
        old_position = racer.position
        new_position = tuple(np.clip(np.add(racer.position,racer.velocity), [0,0], self.world_map.shape))
        new_position = self.check_collision(old_position, new_position) or new_position
        
        # trying
        self.world_map[old_position]=racer.last_elem
        racer.last_elem=self.world_map[new_position]
        self.world_map[new_position]=CAR
        
        # if above doesn't work...
        #self.world_map[old_position]=ROAD
        #self.world_map[new_position]=CAR

        racer.position = new_position
        
    def out_of_bound(self, position):
        height, width=self.world_map.shape
        if position[0]<0 or position[0]>=height:
            return True
        if position[1]<0 or position[1]>=width:
            return True
        return False
    
    # Return position of collision if collision occur in the path
    # Otherwise, return None
    def check_collision(self, old_position, new_position):
        if self.out_of_bound(new_position) or self.world_map[new_position]==WALL:
            return old_position
        return None
