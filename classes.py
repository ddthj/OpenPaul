from util import *


# A path is really just a list of lines
class path:
    def __init__(self, lines=None):
        if lines is not None:
            self.lines = lines
        else:
            self.lines = []

    def update(self, agent):  # updates all the lines, in the case that they have dynamic conditions
        for index, line in enumerate(self.lines):
            line.update(line, agent, index)

    def get_points(self): # returns the start and end points of the first line that hasn't "finished"
        for item in self.lines:
            if not item.finished:
                return (item.start, item.end)
        return self.lines[-1].start, self.lines[-1].end

    def get_line(self, current=True): # returns the entire line, not just the points
        # setting current to False will cause it to get the next line instead of the current one
        for line in self.lines:
            if not line.finished and current is True:
                return line
            else:
                current = True
        return self.lines[-1]

    def finish(self):
        self.get_line().finished = True

    def get_speed(self, distance):  # returns how fast the car should be at this point in the line
        return self.get_line().get_speed(distance)

    def delete(self, agent):  # removes the first line
        self.lines[0].delete(self, agent)
        del self.lines[0]

    def clean(self):  # removes any lines that are finished
        i = 0
        while 1:
            if i < len(self.lines):
                if self.lines[i].finished:
                    del self.lines[i]
                else:
                    i += 1
            else:
                break


# Contains all the information about a line
class line:
    def __init__(self, start=ZEROS3, end=ZEROS3, speed=MAX_CAR_SPEED):
        self.start = start
        self.end = end
        self.arm = True
        self.finished = False
        self.events = [Event(0, speed, True)]  # lines will always have at least one speed event
        self.update = lambda line, agent, index: 0
        self.delete = lambda line, agent: 0

    def get_speed(self, distance):  # used for getting the most recent speed to follow
        temp = None
        for event in self.events:
            if temp is None:
                temp = event
            elif event.distance <= distance and temp.distance <= event.distance:
                temp = event
        return temp.speed


#Events currently only support speed editing, they should be able to handle dodging though
class Event():
    def __init__(self, distance, speed=MAX_CAR_SPEED, anchored=False):
        self.distance = distance
        self.speed = speed
        self.active_editing = False  # if this event is currently being edited
        self.anchored = anchored  # prevents moving these events
