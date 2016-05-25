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


from io import BytesIO
from time import sleep
from PIL import Image

import matplotlib
import numpy as np
import picamera

from experiment_controller.abstract import AbstractController
from experiment_controller.tronix import initio
from util import red_pixel, red_pixel_dist

try:
    import __builtin__
    input = getattr(__builtin__, 'raw_input')
except (ImportError, AttributeError):
    pass

class TronixController(AbstractController):

    def __init__(self, red_pixels):
        AbstractController.__init__(self, red_pixels)
        initio.init()
        self._left_engine = 0
        self._right_engine = 0

        def more_bright():
            self.camera.brightness = max(0, min(100, self.camera.brightness + 5))
            print("brightness %d" % self.camera.brightness)
        self.calibration_functions["b"] = more_bright

        def less_bright():
            self.camera.brightness = max(0, min(100, self.camera.brightness - 5))
            print("brightness %d" % self.camera.brightness)
        self.calibration_functions["n"] = less_bright

        def more_contrast():
            self.camera.contrast = max(-100, min(100, self.camera.contrast + 5))
            print("contrast %d" % self.camera.contrast)
        self.calibration_functions["c"] = more_contrast

        def less_contrast():
            self.camera.contrast = max(-100, min(100, self.camera.contrast - 5))
            print("contrast %d" % self.camera.contrast)
        self.calibration_functions["v"] = less_contrast

        def shutter_longer():
            self.camera.shutter_speed = min(int(1e6/float(self.camera.frame_rate)), self.camera.shutter_speed + 1000)
            print("shutter speed: %d" % self.camera.shutter_speed)
        self.calibration_functions["+"] = shutter_longer

        def shutter_shorter():
            self.camera.shutter_speed = max(0, self.camera.shutter_speed - 1000)
            print("shutter speed: %d" % self.camera.shutter_speed)
        self.calibration_functions["-"] = shutter_shorter

        def set_awb_gains():
            red = input("red: ")
            blue = input("blue: ")
            self.camera.awb_gains = (float(red), float(blue))
            print("awb_gains:" + str(self.camera.awb_gains))
        self.calibration_functions["g"] = set_awb_gains

        def save_optimized():
            print("try with contrast=%d and brightness=%d"% (self.camera.contrast, self.camera.brightness))
            stream = BytesIO()
            self.camera.capture(stream, format='rgb', use_video_port=True)
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            stream.close()

            #recommendation = mode(data.reshape(480*640, 3)[::8,::8])[0][0]

            matplotlib.image.imsave('calibration.png', data.reshape(480,640,3))
            red_pixel_img = np.array(
                                map(red_pixel,
                                    data.reshape(480,640,3)[::16,::16].reshape(480/16*640/16,3)
                                    ),
                                dtype=np.uint8
                            )
            red_pixel_img *= 255
            #red_pixel_img *= 255. / red_pixel_img.max()
            red_pixel_img = red_pixel_img.reshape(480/16, 640/16)
            img = Image.fromarray(red_pixel_img)
            img.save('calibration_delta.png')
            #matplotlib.image.imsave('calibration_delta.png', red_pixel_img)

            data = data.reshape(480*640,3)
            pixels = sum(map(red_pixel, data[::160])) / (480.*640./160.)
            print("red pixels: %f" % pixels)
            #print("color recommendation: " + str(recommendation))
        self.calibration_functions["s"] = save_optimized

        def picture_optimized():
            print("capture...")
            print(self.camera.digital_gain)
            print(self.camera.exposure_compensation)
            self.exposure_mode = 'off'
            print(self.camera.exposure_mode)
            self.camera.image_denoise = False
            print(self.camera.image_denoise)
            self.camera.meter_mode = 'spot'
            print(self.camera.meter_mode)
            self.camera.saturation = 100
            print(self.camera.saturation)
            print(self.camera.sharpness)
            stream = BytesIO()
            self.camera.capture(stream, format='rgb', use_video_port=True)
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            stream.close()
            matplotlib.image.imsave("calibration_picture.png", data.reshape(480,640,3))
            print("done")
        self.calibration_functions["p"] = picture_optimized

    def __enter__(self):
        self.camera = picamera.PiCamera()
        self.camera.__enter__()
        self.camera.contrast = 60
        self.camera.brightness = 50
        self.camera.resolution = (640,480)
        self.camera.frame_rate = 24
        sleep(1)
        self.camera.start_preview()

        self.camera_stream = picamera.PiCameraCircularIO(self.camera, size=640*480*3)
        self.camera.start_recording(self.camera_stream, format='rgb')
        self.camera.wait_recording(1)
        #self.camera.awb_mode = 'off'
        #self.camera.awb_gains = (1.8, 1.5)
        #self.camera.shutter_speed = 30000
        #self.camera.exposure_mode = 'off'
        #sleep(20)
        return self

    def __exit__(self, type, value, traceback):
        initio.cleanup()
        self.camera.stop_recording()
        return self.camera.__exit__(type,value,traceback)

    def randomize(self, state=0):
        pass # TODO

    def reset_environment(self):
        # TODO
        self.pause()

    def reached_aim(self):
        self.pause()
        input("found cube!")
        self.left_engine(-1)
        self.right_engine(-1)
        sleep(0.3)
        self.left_engine(1)
        sleep(0.3)
        self.left_engine(0)
        self.right_engine(0)


    def pause(self):
        initio.stop()

    def _update_motion(self):
        #print(self._left_engine, self._right_engine)
        initio.updateMotion(self._left_engine, self._right_engine)
#        initio.turnForward(self._left_engine, self._right_engine)

    def left_engine(self, power):
        self._left_engine = power*100
        self._update_motion()

    def right_engine(self, power):
        self._right_engine = power*100
        self._update_motion()



    def capture_camera(self):
        frame = iter(self.camera_stream.frames).next()
        result = None
        while result is None or len(result)!=640*480*3:
            self.camera_stream.seek(0)
            result = np.fromstring(self.camera_stream.read1(frame.frame_size),dtype=np.uint8)
        result = result.reshape(640,480,3)
        result = result[::640//40,::480//40]
        return result



    def ultrasonic(self):
        return initio.getDistance()

    def infrared_left(self):
        return initio.irLeft()

    def infrared_right(self):
        return initio.irRight()
