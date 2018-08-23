from rlbot.agents.base_agent import BaseAgent
from gui import GUI
import Bot


'''
Paul, by Marvin GooseFairy and Brom

Mini-ReadMe:
Paul is a set of tools we made in an effort to approach strategy more efficently.
Paul works with paths, which are lines draw from point-to-point in order to accomplish some state
Events can also be added to paths, which control the path speed, jumps, etc. Events are NOT fully implemented

In the master branch most of these tools are undisturbed, in the shooter circles branch paths are
made of lines and circles and the bot is capeable of playing a game.
'''


class Paul(BaseAgent):

    def initialize_agent(self):
        self.gui = GUI() #Paul has a nice GUI that allows for drawing paths, creating and moving/editing events

    def get_output(self, packet):

        game = self.convert_packet_to_v3(packet)#Paul is a V3 Bot, a rework of preprocessing would be needed to re-optimize it
        
        output = Bot.Process(self, game)

        return self.convert_output_to_v4(output)
