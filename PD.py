from util import *


# proportional function, curve1(x) = 1 (if x >= 0.0126), curve1(-0.0063) = -0.1250235
def curve1(x):
    if x > .5:
        x = 1 - Range(x, 1)
    s = x * x * x * 5e5
    return Range(s, 1)


def linear1(x):
    return Range(x / 60, 1)


# PD for steering
def steer_from_angle(angle, derivative, pi=PI):
    return curve1(Range180(angle - derivative / 19, PI) / PI)


def time_until_full_stop(speed):
    return abs(speed) / BRAKES_RATE + 1 / 60


def time_until_desired_velocity(relative_vel):
    if relative_vel > 0:
        rate = 2100
    else:
        rate = 9000
    return abs(relative_vel) / rate


# PD for throttling, uses a 1-dimensional location for forwards or backwards
def throttle_to_point(location, velocity, brakes=True):
    return sign(location - time_until_full_stop(velocity) * brakes * velocity) * linear1(abs(location) + abs(velocity))


def throttle_velocity(velocity, desired_velocity, last_throttle):
    relative_vel = desired_velocity - velocity - last_throttle * 9
    return Range(time_until_desired_velocity(relative_vel) * 60 * sign(relative_vel), 1)


def boost_velocity(velocity, desired_velocity, last_boost):
    relative_vel = desired_velocity - velocity - last_boost * 20
    if velocity < 1400:
        threshold = 200
    else:
        threshold = 20
    return relative_vel > threshold
