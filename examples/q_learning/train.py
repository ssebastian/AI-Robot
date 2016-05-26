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


from time import time

import os
import numpy as np
from pybrain_extension.environment.morse_environment import ControllerEnvironment
from pybrain.rl.experiments import Experiment
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q
from pybrain.rl.learners.valuebased import ActionValueTable
import pylab

from pybrain_extension.task.red_cube_task import MdpRedCubeTask


# from experiment_controller.morse import MorseController as CurrentController
# from experiment_controller.tronix import TronicController as CurrentController
from experiment_controller.comsim import ComSimController as CurrentController


#q_net = buildNetwork(4, 12, 7, bias=True)#, hiddenclass=TanhLayer)
#q_net.randomize()
#data = SupervisedDataSet(4, 7)
#trainer = BackpropTrainer(q_net, data)
#action = np.array([0,0,0,0,0,0,0])
#red_pixels = [0,0,0,0]
#red_pixels_before = 0.0
#
#def apply_action(control, action):
#    actions = ((0,0),(0,1),(1,0),(1,1),(0,-1),(-1,0),(-1,-1))
#    act = actions[action]
#    control.left_engine(act[0])
#    control.right_engine(act[1])
#
#def do_next_action(control, image):
#    global q_net, action, red_pixels
#    splitted_image = split_image(image, 4)
#    red_pixels = list(map(get_red_pixels, splitted_image))
#    action = q_net.activate(red_pixels)
#    arg = np.argmax(action)
#    apply_action(control, arg)

pylab.ion()
pylab.hot()
pylab.show()

with CurrentController(3) as control:
    environment = ControllerEnvironment(control)
    task = MdpRedCubeTask(environment, False)

    control.cubes_x = 2
    control.cubes_y = 3
    control.cubes_size = 4
    task.max_samples = 500

    actions = len(environment.actions)

    actionValueNetwork = ActionValueTable(task.outdim, task.indim)
    actionValueNetwork.stdParams = 0.0001
    actionValueNetwork.randomize()
    # actionValueNetwork = ActionValueNetwork(task.outdim,task.indim)
    # if os.path.isfile("q/q_train.npy"):
    #    actionValueNetwork.param = np.load("q/q_train.npy")
    #else: actionValueNetwork.initialize(0.0001)
    # if os.path.isfile("nfq.xml"): actionValueNetwork.network = NetworkReader.readFrom('nfq.xml')
    pylab.pcolor(actionValueNetwork.params.reshape(32, actions).max(1).reshape(8,4).T)
    pylab.pause(0.01)

    learner = Q()
    agent = LearningAgent(actionValueNetwork, learner)
    experiment = Experiment(task, agent)

    start = time()

    i = 0

    while True:
        for state in range(control.get_randomize_states()):
            control.randomize(state)
            task.reset()

            print("run %d" % i)

            experiment.doInteractions(1000)
            agent.learn()
            agent.reset()

            with open('q/rewards.csv','a') as f: f.write("%f,%d\n" % (task.getTotalReward(), time() - start))

            # print("learn")
            # agent.learn()
            # agent.reset()
            # control.pause()

            pylab.pcolor(actionValueNetwork.params.reshape(32, actions).max(1).reshape(8,4).T)
            pylab.pause(0.01)

            if (i % 20) == 0:
                print("save network")
                #NetworkWriter.writeToFile(actionValueNetwork.network, 'nfq.xml')
                np.save("q/q_train.npy", actionValueNetwork.params)
                pylab.savefig('q/action_value_%d.png' % i)
            i += 1

    #        agent.reset()

    #        pylab.pcolor(controller.params.reshape(81,4).max(1).reshape(9,9))
    #        pylab.draw()

    #        image = control.capture_camera()
    #        reward = get_reward(image)
    #        data.clear()
    #        arg = np.argmax(action)
    #        target = action
    #        target[arg] = reward
    #        data.addSample(red_pixels, target)
    #        trainer.train()
    #        print ("reward: %f" % reward)
    #        do_next_action(control, image)
    #        #sleep(0.01)

    control.left_engine(0)
    control.right_engine(0)


