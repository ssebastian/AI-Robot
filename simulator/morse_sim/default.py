#! /usr/bin/env morseexec

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


""" Basic MORSE simulation scene for <simulation> environment

Feel free to edit this template as you like!
"""

from morse.builder import *
from morse_sim.builder.robots import Box, Redbox
from morse_sim.random_env import randomize
from morse.core import blenderapi

#bpymorse.set_speed(10, 5, 5)


# Add the MORSE mascott, MORSY.
# Out-the-box available robots are listed here:
# http://www.openrobots.org/morse/doc/stable/components_library.html
#
# 'morse add robot <name> simulation' can help you to build custom robots.
robot = ATRV()

#robot.frequency(delay=1)


# The list of the main methods to manipulate your components
# is here: http://www.openrobots.org/morse/doc/stable/user/builder_overview.html
robot.translate(-4.0, 0.0, 0.0)
# robot.rotate(0.,0.,3.14/4*3)

# Add a motion controller
# Check here the other available actuators:
# http://www.openrobots.org/morse/doc/stable/components_library.html#actuators
#
# 'morse add actuator <name> race' can help you with the creation of a custom
# actuator.
motion = MotionVW()
robot.append(motion)
#teleport = Teleport()
#robot.append(teleport)

# Camera with res: 40 x 40 pixel
camera = VideoCamera()
camera.properties(cam_width = 40, cam_height = 40)
camera.translate(0.6, 0.0, 0.4)
robot.append(camera)


# Infrared sensor
infrared = Infrared()
infrared.name = "ir_left"
infrared.translate(0.5, -0.2, 0.0)
robot.append(infrared)

infrared = Infrared()
infrared.name = "ir_right"
infrared.translate(0.5, 0.2, 0.0)
robot.append(infrared)

sick = Infrared()
sick.name = "sonar"
sick.translate(0.5, 0.0, 0.4)
sick.properties(laser_range = 10.0)
robot.append(sick)


# Add a keyboard controller to move the robot with arrow keys.
keyboard = Keyboard()
robot.append(keyboard)
keyboard.properties(ControlType = 'Position')

# Add a pose sensor that exports the current location and orientation
# of the robot in the world frame
# Check here the other available actuators:
# http://www.openrobots.org/morse/doc/stable/components_library.html#sensors
#
# 'morse add sensor <name> race' can help you with the creation of a custom
# sensor.
pose = Pose()
robot.append(pose)

# To ease development and debugging, we add a socket interface to our robot.
#
# Check here: http://www.openrobots.org/morse/doc/stable/user/integration.html 
# the other available interfaces (like ROS, YARP...)
robot.add_default_interface('socket')



for i in range(6):
    box = Redbox() if i == 0 else Box()
    box.name = "box_%d" % i
    teleport = Teleport()
    box.append(teleport)
    box.add_default_interface('socket')


# set 'fastmode' to True to switch to wireframe mode
env = Environment('simulation/environment/random_red_cube.blend', fastmode = False)
env.set_camera_location([10.0, -10.0, 10.0])
env.set_camera_rotation([1.05, 0, 0.78])

# randomize()

from threading import Timer
from morse.core.morse_time import FixedSimulationStepStrategy

#env.set_time_strategy(FixedSimulationStepStrategy())

# env.show_framerate(True)

