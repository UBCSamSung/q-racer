import numpy as np
import helper

WALL=0
ROAD=255
CAR=128
LINE=200



class Racer():
    def __init__(self, position, direction):
        self.position=position
        self.velocity=(0,0)
        self.direction=direction
        self.lap=0
        self.action=None
        # car option
        self.deltaV=1
        self.deltaPhi=10
    
    def update(self):
        if self.action==None:
            return
        elif self.action=="forward":
            acceleration = helper.angle2vector(self.direction)*self.deltaV
            self.velocity=tuple(np.add(self.velocity, acceleration))
        elif self.action=="backward":
            acceleration = -helper.angle2vector(self.direction)*self.deltaV

            self.velocity=tuple(np.add(self.velocity, acceleration))
        elif self.action=="left":
            self.direction+=self.deltaPhi
        elif self.action=="right":
            self.direction-=self.deltaPhi
        else:
            raise Exception('bad action')

            

class World():
    def __init__(self):
        map_height=30
        map_width=40
        self.racers=[]
        self.world_map=np.zeros([map_height, map_width], dtype=np.uint8)
        
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
                self.racers[index].action = agent_input
        for racer in self.racers:
            self.update_racer(racer)
    
    def update_racer(self, racer):
        racer.update()
        old_position = racer.position
        new_position = tuple(np.array(np.add(racer.position,racer.velocity), dtype=np.uint8))
        print("new position", new_position)
        collision_position = self.check_collision(old_position, new_position)
        if collision_position!=None:
            racer.velocity=0
            new_position = collision_position
        self.world_map[old_position]=ROAD
        self.world_map[new_position]=CAR
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
