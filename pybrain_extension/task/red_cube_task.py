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


import numpy as np
from pybrain.rl.environments import EpisodicTask

from pybrain_extension.environment.morse_environment import ContinuousControllerEnvironment, ControllerEnvironment
from pybrain.utilities import abstractMethod


def split_image(image, n):
    image_t = np.transpose(image, axes=(1, 0, 2))
    rows, pixels_per_row, channels = image_t.shape
    return image_t.reshape((n, rows / n, pixels_per_row, channels))


class RedCubeTask(EpisodicTask):
    image_splits = 8
    _max_no_change_counter = 10

    def __init__(self, environment):
        super(RedCubeTask, self).__init__(environment)
        self.sensors = None
        self.found_cube = False
        self.discount = 0.996
        self.pixels = None
        self.action = None
        self.no_actions = False
        self.max_samples = 500

    def performAction(self, action):
        self.action = action
        super(RedCubeTask, self).performAction(action)

    def getReward(self):
        abstractMethod()

    def getObservation(self):
        """ A filtered mapping to getSensors of the underlying environment. """
        abstractMethod()

    def isFinished(self):
        """ Is the current episode over? """
        return self.samples > self.max_samples or self.found_cube or self.no_actions

    def reset(self):
        """ Re-initialize the environment """
        EpisodicTask.reset(self)
        self.sensors = None
        self.found_cube = False
        self.no_actions = False

    @property
    def outdim(self):
        return self.env.outdim - 1 + self.env.get_red_pixels()  # image removed and red pixels added


class SimplifiedRedCubeTask(RedCubeTask):

    def __init__(self, environment, simplified):
        super(SimplifiedRedCubeTask, self).__init__(environment)
        self.simplified = simplified
        self.reward = None

    def reset(self):
        super(SimplifiedRedCubeTask, self).reset()
        self.reward = None

    def getReward(self):
        # print("reward: %d" % self.reward)
        return self.reward

    def getObservation(self):
        if self.sensors is None:
            self.sensors = self.env.getSensors()
        return self._get_observation(self.sensors)

    def performAction(self, action):
        self.action = action
        if self.sensors is None:
            self.sensors = self.env.getSensors()
        self.reward = self._get_reward()

        super(SimplifiedRedCubeTask, self).performAction(action)

        observation = self.getObservation()

        count = 0
        while self.simplified and count < 20 and not self.isFinished() and not self.observation_changed(observation):
            if isinstance(self.env, ContinuousControllerEnvironment) and self.env.no_actions():
                self.no_actions = True
                self.reward -= 25
            super(SimplifiedRedCubeTask, self).performAction(action)
            count += 1

        self.sensors = None

    def observation_changed(self, observation):
        abstractMethod()

    def _get_reward(self):
        abstractMethod()

    def _get_observation(self, sensors):
        abstractMethod()


class CameraPixelsRedCubeTask(SimplifiedRedCubeTask):

    def _get_reward(self):
        # image = self.sensors[-1]
        red_pixels = float(sum(self.pixels)) / float(len(self.pixels))
        # reward = (red_pixels - self.red_pixels_before)*10.
        # if reward < 0:
        #    reward *= 0.9
        reward = 0.1 * red_pixels / float(self.max_samples)
        # reward += 0.01 * sum(self.action) / float(self.max_samples)
        self.red_pixels_before = red_pixels
        if self.sensors[0] or self.sensors[1]:
            reward -= 0.05 / self.max_samples

        if self.sensors and self.sensors[0] and self.sensors[1] and red_pixels >= 0.8:
            self.found_cube = True
            if isinstance(self.env, ContinuousControllerEnvironment):
                self.env.reached_aim()
            else:
                print("Found cube!!!")
            reward += 10

        return reward

    def _get_observation(self, sensors):
        observation = sensors[0:2]
        self.pixels = sensors[-1]

        observation.extend(self.pixels)
        return np.array(observation)

    def observation_changed(self, observation):
        return not np.array_equal(observation, self._get_observation(self.env.getSensors()))

    @property
    def outdim(self):
        return self.env.outdim - 1 + self.env.get_red_pixels()  # image removed and 4 red pixel splits added


class MdpRedCubeTask(SimplifiedRedCubeTask):

    def __init__(self, environment, simplified):
        super().__init__(environment, simplified)
        self.next_finished = False

    def _get_observation(self, sensors):
        observation = sensors[0:2]
        self.pixels = sensors[-1]
        observation.extend(self.pixels)
        # print(np.array(observation, dtype=int))
        return self.make_mdp(np.array(observation))

    def observation_changed(self, observation):
        return not np.array_equal(observation, self._get_observation(self.env.getSensors()))

    @staticmethod
    def make_mdp(observation):
        i = 0
        new_obs = 0
        for obs in observation:
            if obs == True:
                new_obs |= 1 << i
            i += 1
        return np.array([new_obs])

    def _get_reward(self):
        if self.next_finished:
            return 0
        red_pixels = float(sum(self.pixels)) / float(len(self.pixels))

        # reward = red_pixels / float(self.max_samples)
        # reward += 0.0001 * sum(ControllerEnvironment.actions[int(self.action[0])])
        reward = -0.02
        if red_pixels == 0 and (self.sensors[0] or self.sensors[1]):
            reward -= 0.5

        if self.sensors and self.sensors[0] and self.sensors[1] and red_pixels >= 0.6:
            self.found_cube = True
            print("Found cube!!!")
            reward += 5

        return reward

    @property
    def outdim(self):
        return 2 ** (self.env.get_red_pixels()+2)
