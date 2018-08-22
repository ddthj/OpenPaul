from rlbot.agents.base_agent import BaseAgent
from gui import GUI
import Bot


'''
Paul, by Marvin GooseFairy and Brom

'''


class Paul(BaseAgent):

    def initialize_agent(self):
        self.gui = GUI()

    def get_output(self, packet):

        game = self.convert_packet_to_v3(packet)
        output = Bot.Process(self, game)

        return self.convert_output_to_v4(output)
