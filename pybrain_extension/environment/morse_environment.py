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


from pybrain.rl.environments import Environment

try:
    import __builtin__
    input = getattr(__builtin__, 'raw_input')
except (ImportError, AttributeError):
    pass

assert input, "Input is either in __builtin__ (python 2) or already defined (python 3)"



class ControllerEnvironment(Environment):

    # actions = ((0,0),(0,1),(1,0),(1,1),(0,-1),(-1,0),(-1,-1))
    # actions = ((0,1),(1,0),(1,1),(0,-1),(-1,0),(-1,-1))
    actions = ((0,0),(1,1),(1,-1),(-1,1),(-1,-1))

    def __init__(self, control):
        self.control = control
        self.indim = len(self.actions)
        self.outdim = 3
        self.reset()

    def get_red_pixels(self):
        return self.control.red_pixel_count

    def getSensors(self):
        """ the currently visible state of the world (the observation may be
            stochastic - repeated calls returning different values)
            :rtype: by default, this is assumed to be a numpy array of doubles
            :note: This function is abstract and has to be implemented.
        """
        return [
            self.control.infrared_left(),
            self.control.infrared_right(),
            # self.control.ultrasonic(),
            self.control.red_pixels()
        ]

    def performAction(self, action):
        """ perform an action on the world that changes it's internal state (maybe
            stochastically).
            :key action: an action that should be executed in the Environment.
            :type action: by default, this is assumed to be a numpy array of doubles
            :note: This function is abstract and has to be implemented.
        """
        #print ("action: ", action)
        act = self.actions[int(action[0])]
        self.control.left_engine(act[0])
        self.control.right_engine(act[1])
        self.control.step()

    def reset(self):
        """ Most environments will implement this optional method that allows for
            reinitialization.
        """
        self.control.left_engine(0)
        self.control.right_engine(0)
        #input("Press enter to continue")
        self.control.reset_environment()


class ContinuousControllerEnvironment(ControllerEnvironment):
    def __init__(self, control):
        super(ContinuousControllerEnvironment, self).__init__(control)
        self.no_action_counter = 0
        self.indim = 2

    def performAction(self, action):
        self.control.left_engine(action[0])
        self.control.right_engine(action[1])

        if [x for x in action if abs(x) > 0.01]:
            self.no_action_counter = 0
        else:
            self.no_action_counter += 1

        self.control.step()

    def reached_aim(self):
        self.control.reached_aim()

    def no_actions(self):
        result = self.no_action_counter >= 3
        if result:
            self.no_action_counter = 0
        return result

    def reset(self):
        self.no_action_counter = 0
        super(ContinuousControllerEnvironment, self).reset()
