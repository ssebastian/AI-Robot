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


from time import sleep
from util import red_pixel
import matplotlib
import readchar
import numpy as np


class AbstractController(object):

    def __init__(self, red_pixels):
        self.red_pixel_count = red_pixels

        def left():
            self.left_engine(1)
            self.right_engine(-1)
            sleep(0.5)
            self.pause()
        def right():
            self.left_engine(-1)
            self.right_engine(1)
            sleep(0.5)
            self.pause()
        # def target_color():
        #     print("please enter the target color")
        #     red = int(input("red: "))
        #     green = int(input("green: "))
        #     blue = int(input("blue: "))
        #     set_target_color([red, green, blue])
        def save():
            print("test image...")
            data = self.capture_camera()
            cam_pix_x = data.shape[0]
            cam_pix_y = data.shape[1]
            colors = data.shape[2]

            # recommendation = mode(data.reshape(cam_pix_x*cam_pix_y, colors))[0][0]

            matplotlib.image.imsave('calibration.png', data.reshape(cam_pix_x, cam_pix_y, colors))
            # red_pixel_img = np.array(
            #     list(map(red_pixel_dist,
            #              data.reshape(cam_pix_x*cam_pix_y, colors)
            #              )),
            #     dtype=np.uint8
            # )
            #red_pixel_img *= 255. / red_pixel_img.max()
            # red_pixel_img = red_pixel_img.reshape(cam_pix_x, cam_pix_y)
            # img = Image.fromarray(red_pixel_img)
            # img.save('calibration_delta.png')
            #matplotlib.image.imsave('calibration_delta.png', red_pixel_img)

            data = data.reshape(cam_pix_x*cam_pix_y, colors)
            pixels = sum(map(red_pixel, data)) / float(cam_pix_x*cam_pix_y)
            print("red pixels: %f" % pixels)
            # print("color recommendation: " + str(recommendation))
        def picture():
            print("capture picture...")
            data = self.capture_camera()
            matplotlib.image.imsave('calibration_picture.png', data)
            print("done")


        self.calibration_functions = {
            readchar.key.LEFT: left,
            readchar.key.RIGHT: right,
            # "t": target_color,
            "s": save,
            "p": picture
        }

    def get_randomize_states(self):
        return 1

    def randomize(self, state=None):
        raise NotImplementedError("Class %s doesn't implement randomize()" % (self.__class__.__name__))

    def reset_environment(self):
        raise NotImplementedError("Class %s doesn't implement reset_environment()" % (self.__class__.__name__))

    def reached_aim(self):
        raise NotImplementedError("Class %s doesn't implement reached_aim()" % (self.__class__.__name__))

    def pause(self):
        raise NotImplementedError("Class %s doesn't implement pause()" % (self.__class__.__name__))


    def left_engine(self, power):
        raise NotImplementedError("Class %s doesn't implement left_engine()" % (self.__class__.__name__))

    def right_engine(self, power):
        raise NotImplementedError("Class %s doesn't implement right_engine()" % (self.__class__.__name__))


    def capture_camera(self):
        raise NotImplementedError("Class %s doesn't implement capture_camera()" % (self.__class__.__name__))


    def ultrasonic(self):
        raise NotImplementedError("Class %s doesn't implement ultrasonic()" % (self.__class__.__name__))


    def infrared_left(self):
        raise NotImplementedError("Class %s doesn't implement infrared_left()" % (self.__class__.__name__))

    def infrared_right(self):
        raise NotImplementedError("Class %s doesn't implement infrared_right()" % (self.__class__.__name__))

    def red_pixels(self):
        image = self.capture_camera()
        rows, cols, channels = image.shape
        image_reshaped = image[rows // 2].reshape((cols, channels))
        step_size = (cols//self.red_pixel_count)
        image_reshaped = image_reshaped[:step_size*self.red_pixel_count]
        image_reshaped = image_reshaped.reshape((self.red_pixel_count, step_size, channels))
        return np.apply_along_axis(red_pixel, 2, image_reshaped).any(axis=1)

    def calibrate(self):
        print("calibration:")
        while True:
            key = readchar.readkey()
            if key == readchar.key.ENTER:
                break
            if key in self.calibration_functions:
                self.calibration_functions[key]()
        print("finished calibration")

    def step(self):
        """
        Method to go one step further in simulation (if any).
        :return: None
        """
