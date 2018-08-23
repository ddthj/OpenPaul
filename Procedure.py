from util import *


def pre_process(self, game): #Turns gamepacket into more useful values

    self.game = game
    self.player = game.gamecars[self.index]
    self.ball = game.gameball

    # converting vector3 and rotator classes into numpy arrays
    self.player_loc = a3(self.player.Location)
    self.player_vel = a3(self.player.Velocity)
    self.player_rot = a3(self.player.Rotation)
    self.player_angvel = a3(self.player.AngularVelocity)

    self.ball_loc = a3(self.ball.Location)
    self.ball_vel = a3(self.ball.Velocity)

    if not hasattr(self, 'counter'):

        self.counter = 0

        self.throttle = self.steer = self.pitch = self.yaw = self.roll = self.jump = self.boost = self.powerslide = 0

        self.target_loc = self.player_loc
        self.desired_speed = MAX_CAR_SPEED

        self.throttle_type = "point"

        feedback(self)

    # converting the veloctites to local coordinates
    self.pitch_vel, self.roll_vel, self.yaw_vel = local(self.player_angvel, ZEROS3, self.player_rot)
    self.player_local_vel = local(self.player_vel, ZEROS3, self.player_rot)
    self.player_vel_mag, self.player_vel_yaw_ang, self.player_vel_pitch_ang = spherical(*self.player_local_vel)

    # approximate turning radius
    self.player_radius = turning_radius(dist2d(self.player_local_vel))

    self.color = -sign(self.player.Team)
    self.goal = a3([0, FIELD_LENGTH / 2 * self.color, 0])


def feedback(self):

    self.last_throttle, self.last_steer = self.throttle, self.steer
    self.last_pitch, self.last_yaw, self.last_roll = self.pitch, self.yaw, self.roll
    self.last_jump, self.last_boost, self.last_powersilde = self.jump, self.boost, self.powerslide

    self.counter += 1


def finish(self):

    if self.counter % 2:#Just throttles the GUI to maintain FPS of the actual bot code
        self.gui.update(self.game, self)
        
    #Some paths are dynamic, meaning they change depending on the game conditions
    #This is where the path is updated from    
    self.path.update(self) 

    #An old method for deleting a user-drawn path after it has been completed 
    '''
    if len(self.path.lines) != 0 and hasattr(self, "line"):

        if dist3d(self.player_loc, self.line.start) < 99:
            self.line.started = True
        
        
        if self.line.started and dist2d(self.player_loc, self.line.end) < 99:
            self.line.finished = True
            self.path.delete(self)
    '''
