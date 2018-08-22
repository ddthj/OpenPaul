from util import *
from classes import *


""" Lines """

def ball_to_goal_update(line, agent, index):
    speed = 2300
    line.events[0].speed = speed
    dist = dist3d(agent.goal, agent.ball_loc)
    line.start = set_dist(agent.goal, agent.ball_loc, dist + (turning_radius(speed)*2))
    line.end = set_dist(agent.goal, agent.ball_loc, dist + 150)

def car_to_next_update(line,agent,index):
    line.start = (agent.player_loc)
    line.end = (agent.path.lines[index+1].start)
    line.events[0].speed = 2300

ball_to_goal = line()
ball_to_goal.update = ball_to_goal_update

car_to_next = line()
car_to_next.update = car_to_next_update

""" Paths """
class pathTypes():
    def __init__(self):
        self.basicShot = path([car_to_next, ball_to_goal])
        self.basicShot2 = path()

pathTypes = pathTypes()
