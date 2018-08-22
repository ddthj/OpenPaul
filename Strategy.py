from paths import pathTypes
from util import *
from copy import deepcopy


def plan(self):

    if not hasattr(self, "path"):  # use path when there is none, not when it's empty
        self.path = deepcopy(pathTypes.basicShot)

    if len(self.path.lines) != 0:
        Follow_Line(self)


def Follow_Line(self):
    self.line = self.path.get_line()
    if len(self.path.lines)-1 > self.path.lines.index(self.line):
        self.next_line = self.path.lines[self.path.lines.index(self.line)+1]
        prep_flag = True
    else:
        prep_flag = False
    #getting player's projection and converting it to local cords (from the line start)
    self.line_yaw = math.atan2(*(a2(self.line.end) - a2(self.line.start)))
    player_projection = line_projection(self.line.start,self.line.end,self.player_loc)
    local_player_projection = local_2d(player_projection, self.line.start, self.line_yaw)

    #calculating how far the target should be from teh projection (the closer the bot is the farther down the line)
    player_2d_error = dist2d(self.player_loc, player_projection)
    target_distance = Range(180000/(1 + abs(player_2d_error)),1800) #this could probably be 180000
    local_player_projection[1] += target_distance

    #converting the point we just calculated back into world cords
    self.target_loc = world_2d(local_player_projection,self.line.start,self.line_yaw)
    z = ((self.line.end[2]-self.line.start[2]) / dist2d(self.line.start,self.line.end))*local_player_projection[1]
    self.target_loc = a3([*self.target_loc,z])

    '''
    self.line_yaw = math.atan2(*(a2(self.line.end) - a2(self.line.start)))
    self.player_to_line = local_2d(self.player_loc, self.line.start, self.line_yaw)
    
    if not self.line.started:
        self.target_loc = self.line.start
    else:
        self.target_loc = self.line.end
    '''
    #Desired speed goes here so that we can use that number to predict our radius
    self.desired_speed = self.line.get_speed(local_player_projection[1])
    #figuring out if we can start the next line or not
    if self.line.arm and prep_flag:
        circle_left_local = a3([turning_radius(self.desired_speed),0,0])
        circle_left = world(circle_left_local,self.player_loc,self.player_rot)

        circle_left_projection_distance = dist2d(line_projection(self.next_line.start,self.next_line.end,circle_left),circle_left)

        circle_right_local = a3([-turning_radius(self.desired_speed), 0,0])
        circle_right = world(circle_right_local, self.player_loc, self.player_rot)
        circle_right_projection_distance = dist2d(line_projection(self.next_line.start, self.next_line.end, circle_right),circle_right)

        # this assumes the player is not going to change speed from the current line to the next line, we could calculate a radius based on the target speed on the start of the next line to prevent
        # acceleration-related overshoots/undershoots
        if circle_left_projection_distance <= turning_radius(self.desired_speed) * 1.2 or circle_right_projection_distance <= turning_radius(self.desired_speed) * 1.2:
            self.line.finished = True
    if dist2d(self.player_loc, self.line.end) <= self.player_radius:
        self.line.finished = True


    # converting target location into car local coordinates
    self.target_local_loc = local(self.target_loc, self.player_loc, self.player_rot)

    # getting distance and relative angles to target
    self.target_dist, self.target_yaw_ang, self.target_pitch_ang = spherical(*self.target_local_loc)
