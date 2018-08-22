import Procedure
import Handling
import Strategy


def Process(s, game, version=3):
    """Main Loop."""

    Procedure.pre_process(s, game)

    Strategy.plan(s)
    Handling.controls(s)

    Procedure.feedback(s)

    # Testing.graph_path(s)

    return output(s, version)


def output(s, version):
    """Return bot controls"""

    return [s.throttle, s.steer, s.pitch, s.yaw, s.roll, s.jump, s.boost, s.powerslide]
