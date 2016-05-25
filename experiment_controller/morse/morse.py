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


from pymorse import Morse
import base64
import numpy as np
import random

from experiment_controller.abstract import AbstractController


class MorseController(AbstractController):

    def __init__(self, red_pixels):
        AbstractController.__init__(self, red_pixels)
        self._morse = Morse()
        self._left_engine = 0
        self._right_engine = 0

    def __enter__(self):
        self._morse.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        return self._morse.__exit__(type, value, traceback)

    def get_randomize_states(self):
        return 6

    def randomize(self, state=None):
        if state is None:
            state = random.randint(0, self.get_randomize_states()-1)
        for i in range(self.get_randomize_states()):
            x = i % 3
            y = i // 3
            box_nr = 0 if state == i else i if state < i else i+1
            getattr(self._morse, "box_%d" % box_nr).teleport.publish({"x": (-10 + x * 5), "y": (-4 + y * 8), "z": 0, "yaw": 0, "pitch": 0, "roll": 0})
        self.reset_environment()

    def reset_environment(self):
        self._morse.reset()
        # self._morse.rpc("robot", "randomize")

        #print(self._morse.robot.pose.get())
        #self._morse.robot.teleport.publish({'x':(random()-0.5)*3,'y':(random()-0.5)*3,'z':0,'roll':0,'yaw':(random()-0.5)*3.14*2,'pitch':0})
        #self._morse.robot.translate(1.0, 0.0, 0.0)
        #self._morse.robot.rotate(0.0, 0.0, 0.0)
        self.pause()

    def reached_aim(self):
        print("found cube!")
        self.pause()

    def pause(self):
        self.left_engine(0)
        self.right_engine(0)

    def _update_motion(self):
        w = self._left_engine - self._right_engine
        v = self._left_engine + self._right_engine
        w /= 4
        v /= 4
        self._morse.robot.motion.publish({"v": v, "w": w})

    def left_engine(self, power):
        self._left_engine = power
        self._update_motion()

    def right_engine(self, power):
        self._right_engine = power
        self._update_motion()



    def capture_camera(self):
        image = np.frombuffer(base64.b64decode(self._morse.robot.camera.get()['image']), dtype=np.uint8)
        #shape = image.shape
        return image.reshape((40,40,4))



    def _infrared_val(self, sensor):
        range_list = sensor.get()['range_list']
        return sum(range_list)/float(len(range_list))


    def _sonar_val(self, sensor):
        range_list = sensor.get()['range_list']
        return np.median(range_list)

    def ultrasonic(self):
        value = self._sonar_val(self._morse.robot.sonar)
        return value/10

    def infrared_left(self):
        return self._infrared_val(self._morse.robot.ir_left) <= 1.9

    def infrared_right(self):
        return self._infrared_val(self._morse.robot.ir_right) <= 1.9
