import numpy as np

class Racer():
    def __init__(self, position, direction):
        self.position=position
        self.velocity=(0,0)
        self.direction=direction
        self.lap=0
        self.instruction=None

class World():
    def __init__(self):
        map_height=30
        map_width=40
        self.racers=[]
        self.world_map=np.zeros([map_height, map_width], dtype=np.uint8)
        # For demo:
        self.add_racer((10,20), 0)
        self.racers[0].velocity=(1,0)
        
    def get_state(self):
        return {
            'racers': self.racers,
            'world_map': self.world_map
        }
    
    def add_racer(self, position, direction):
        racer = Racer(position, direction)
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
        self.world_map[old_position]=0
        self.world_map[new_position]=128
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
        if self.out_of_bound(new_position) or self.world_map[new_position]>0:
            return old_position
        return None
