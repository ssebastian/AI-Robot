__author__ = "Sebastian Schmoll"
__copyright__ = "Copyright 2016 Sebastian Schmoll"
__license__ = """
    This file is part of AI Robot.

    AI Robot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    AI Robot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with AI Robot.  If not, see <http://www.gnu.org/licenses/>.
"""
__version__ = "0.1"
__maintainer__ = "Sebastian Schmoll"
__email__ = "sebastian@schmoll-muenchen.de"


from pybrain.rl.agents.agent import Agent

from neat import nn
from neat import population, visualize

import numpy as np


class NeatAgent(Agent):

    def __init__(self, genome, bias=False):
        self.net = nn.create_feed_forward_phenotype(genome)
        self.bias = bias

    def getAction(self):
        return self.net.serial_activate(self.observation)

    def integrateObservation(self, observation):
        if self.bias:
            observation = np.append([1], observation)
        self.observation = observation


