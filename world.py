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
    def __init__(self, id, position, direction, last_elem):
        self.id=id
        self.position=position
        self.velocity=(0,0)
        self.direction=direction
        self.lap=0
        self.last_elem=last_elem
        self.action=None
        self.start_time=dt.datetime.now()
        self.penalty=0

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
        racer = Racer(len(self.racers), startPosition, direction, last_elem)
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
            #print("Game end!")
            #for racer in racersAtGoal:
            #    print(f"Winning racer: {racer.id} Score: {-racer.penalty}")

            allRacerResults = {}
            for racer in self.racers:
                if racer.id not in racersAtGoal:
                    allRacerResults[racer.id] = float("-inf")
                else:
                    allRacerResults[racer.id] = -racer.penalty
            
            return allRacerResults

        return {}
    
    def update_racer(self, racer):
        if racer.position[1] == self.goal_line:
            #print("Race done")
            return True

        racer.update()
        old_position = racer.position
        new_position = tuple(np.array(np.add(racer.position,racer.velocity), dtype=np.uint8))
        collision_position = self.path_collision(old_position, new_position)

        if collision_position!=None:
            racer.velocity=0
            new_position = collision_position

        self.world_map[old_position]=racer.last_elem

        if self.world_map[new_position] != CAR:
            racer.last_elem=self.world_map[new_position]

        self.world_map[new_position]=CAR
        racer.position = new_position
        racer.penalty += 1
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
    def path_collision(self, old_position, new_position):
        # store last valid point in the path
        previous_valid_point=old_position
        # convert to float to avoid overflow
        old_position=np.array(old_position, dtype=np.float)
        new_position=np.array(new_position, dtype=np.float)
        # check along the axis with higher displacment
        axis=0 if abs(old_position[0] - new_position[0])>abs(old_position[1] - new_position[1]) else 1
        if abs(new_position[axis]-old_position[axis])==0:
            # did not move
            return None
        # use longer axis to create line equation
        line_equation = helper.point2line(old_position, new_position, inverse=axis==0)
        # step through each point along the longer axis
        steps=np.linspace(old_position[axis], new_position[axis], 
            num=abs(old_position[axis] - new_position[axis])+1, 
            endpoint=True)
        for step in steps:
            point = (int(round(step)), int(round(line_equation(step))))
            if axis==1:
                point=point[::-1]
            point=tuple(point)
            if self.point_collision(point):
                return previous_valid_point
            else:
                previous_valid_point=point
        return None

    # detect if point is collision free
    def point_collision(self, point):
        if self.out_of_bound(point) or self.world_map[point]==WALL:
            return True
        return False