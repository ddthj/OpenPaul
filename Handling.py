from util import *
from PD import *


def controls(self):
    #All of Paul's targets and plans are already set into variables from Strategy.plan, so all we are doing here is feeding
    #that info into our PD controls

    self.powerslide = 0

    #SlowDown(self)
    
    #Paul uses PD control
    self.steer = steer_from_angle(self.target_yaw_ang, self.yaw_vel, PI)

    self.throttle = throttle_velocity(self.player_local_vel[1], self.desired_speed, self.last_throttle)
    self.boost = self.throttle == 1 and boost_velocity(self.player_local_vel[1], self.desired_speed, self.last_boost)


def SlowDown(self):

    player_circle_local = a3([self.player_radius * sign(self.target_local_loc[0]), 0, 0])
    self.player_circle = world(player_circle_local, self.player_loc, self.player_rot)

    # if target is inside our turning radius
    if dist2d(self.player_circle, self.target_loc) < self.player_radius - 50:
        # slow down
        self.desired_speed = min(max(turning_speed(localized_circle_radius(
            *a2(self.target_local_loc))), 400), self.desired_speed)
        # if we're already too slow > powerslide
        if self.player_vel_mag < 400:
            self.powerslide = 1


def output(self):
    return [self.throttle, self.steer, self.pitch, self.yaw, self.roll, self.jump, self.boost, self.powerslide]
