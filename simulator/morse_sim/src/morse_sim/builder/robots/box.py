from morse.builder import *

class Box(GroundRobot):
    """
    A template robot model for box, with a motion controller and a pose sensor.
    """
    def __init__(self, name = None, debug = True):

        # box.blend is located in the data/robots directory
        Robot.__init__(self, 'morse_sim/robots/box.blend', name)
        self.properties(classpath = "morse_sim.robots.Box")

        ###################################
        # Actuators
        ###################################


        # (v,w) motion controller
        # Check here the other available actuators:
        # http://www.openrobots.org/morse/doc/stable/components_library.html#actuators
        self.motion = MotionVW()
        self.append(self.motion)

        # Optionally allow to move the robot with the keyboard
        if debug:
            keyboard = Keyboard()
            keyboard.properties(ControlType = 'Position')
            self.append(keyboard)

        ###################################
        # Sensors
        ###################################

        self.pose = Pose()
        self.append(self.pose)

