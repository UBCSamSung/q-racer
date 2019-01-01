import numpy as np
import datetime as dt
import helper

# Color coding for map elements
WALL=0
ROAD=255
CAR=128
LINE=200
GOAL=100

# Track info
TRACK_WIDTH = 10


class Racer():
    def __init__(self, position, direction, last_elem):
        self.position=position
        self.velocity=(0,0)
        self.direction=direction
        self.lap=0
        self.last_elem=last_elem
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
        self.racers=[]
        self.world_map=None
        self.start_line=None
        self.goal_line=None
        self.start_time=dt.datetime.now()
        
    def set_map(self, map):
        self.world_map, self.start_line, self.goal_line = map

    def get_state(self):
        return {
            'racers': self.racers,
            'world_map': self.world_map
        }
    
    def add_racer(self, direction):
        startY = np.random.choice(np.where(self.world_map[:,self.start_line] == LINE)[0], 1)[0]
        startPosition = (startY, self.start_line)

        last_elem=self.world_map[startPosition]
        racer = Racer(startPosition, direction, last_elem)
        self.racers.append(racer)
    
    def update(self, agent_inputs=None):
        if agent_inputs:
            for index, agent_input in enumerate(agent_inputs):
                self.racers[index].action = agent_input

        racersAtGoal = []
        for racer in self.racers:
            crossedGoal = self.update_racer(racer)
            if crossedGoal:
                racersAtGoal.append(racer)
        if len(racersAtGoal) > 0:
            print("Game end!")
            print(f"Winning racers: {racersAtGoal}")
    
    def update_racer(self, racer):
        if racer.position[1] == self.goal_line:
            print("Race done")
            return True

        racer.update()
        old_position = racer.position
        new_position = tuple(np.array(np.add(racer.position,racer.velocity), dtype=np.uint8))
        collision_position = self.check_collision(old_position, new_position)

        if collision_position!=None:
            racer.velocity=0
            new_position = collision_position

        self.world_map[old_position]=racer.last_elem

        if self.world_map[new_position] != CAR:
            racer.last_elem=self.world_map[new_position]

        self.world_map[new_position]=CAR
        racer.position = new_position
        return False
        
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
