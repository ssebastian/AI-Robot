import logging; logger = logging.getLogger("morse." + __name__)
import morse.core.robot

from morse.core import blenderapi
from morse.core.services import service
from morse.services.supervision_services import main_reset


class Chappy(morse.core.robot.Robot):
    """ 
    Class definition for the chappy robot.
    """

    _name = 'chappy robot'

    def __init__(self, obj, parent=None):
        """ Constructor method

        Receives the reference to the Blender object.
        Optionally it gets the name of the object's parent,
        but that information is not currently used for a robot.
        """

        logger.info('%s initialization' % obj.name)
        morse.core.robot.Robot.__init__(self, obj, parent)

        # Do here robot specific initializations
        logger.info('Component initialized')

    def default_action(self):
        """ Main loop of the robot
        """

        # This is usually not used (responsibility of the actuators
        # and sensors). But you can add here robot-level actions.
        pass

    @service
    def randomize(self):
        print("\n\n\n\n\n\n\n\n\n__________________\n________________\nrandomize!!!\n\n\n\n\n\n\n\n\n\n\n\n\n")
        from morse.builder import morsebuilder
        objlist = morsebuilder.bpymorse.get_objects()
        boxlist = list(filter(lambda x: x.name.startswith("Box."), objlist))

        import random
        random.shuffle(boxlist)

        for i, box in enumerate(boxlist):
            x = i % 5
            y = i // 5
            print(box)
            print(box.location)
            box.location = (-10 + x * 3, -6 + y * 4, 0.51)
            print(box.location)

        contr = blenderapi.controller()
        main_reset(contr)
