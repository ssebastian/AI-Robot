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


from simulator.comsim import ComSim
from ..abstract import AbstractController
import random


class ComSimController(AbstractController):

    def __init__(self, red_pixels):
        super(ComSimController, self).__init__(red_pixels)
        self._comsim = ComSim(red_pixels)
        self._curr_action = [0, 0]
        self.cubes_x = 2
        self.cubes_y = 3
        self.cubes_size = 4

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def get_randomize_states(self):
        return self.cubes_x*self.cubes_y

    def randomize(self, state=None):
        self._comsim.clear_env()
        random.seed()
        red_cube_index = state if state is not None else random.randint(0, self.get_randomize_states()-1)
        for i in range(self.cubes_x*self.cubes_y):
            x = (i % self.cubes_x) * self._comsim._width//self.cubes_x + self._comsim._width//(self.cubes_x*2)
            y = (i // self.cubes_x) * self._comsim._height//self.cubes_y + self._comsim._height//(self.cubes_y*2)
            if i == red_cube_index:
                self._comsim.add_red_cube(x, y, self.cubes_size)
            else:
                self._comsim.add_obstacle(x, y, self.cubes_size)

    def reset_environment(self):
        self._comsim.reset()

    def reached_aim(self):
        print("found cube!")
        self.pause()

    def pause(self):
        self._comsim.do([0,0], 0)


    def left_engine(self, power):
        self._curr_action[0] = power

    def right_engine(self, power):
        self._curr_action[1] = power


    def capture_camera(self):
        raise NotImplementedError("Class %s doesn't implement capture_camera()" % (self.__class__.__name__))


    def ultrasonic(self):
        raise NotImplementedError("Class %s doesn't implement ultrasonic()" % (self.__class__.__name__))

    def calibrate(self):
        pass # TODO

    def infrared_left(self):
        return self._comsim.infrared_left()

    def infrared_right(self):
        return self._comsim.infrared_right()

    def red_pixels(self):
        return self._comsim.red_pixels()

    def step(self):
        self._comsim.do(self._curr_action, 0.3)
        # self._comsim.show()
