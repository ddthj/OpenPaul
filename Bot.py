import Procedure
import Strategy
import Handling


def Process(self, game):

    Procedure.pre_process(self, game)

    Strategy.plan(self)

    Handling.controls(self)

    Procedure.feedback(self)

    Procedure.finish(self)

    return Handling.output(self)
