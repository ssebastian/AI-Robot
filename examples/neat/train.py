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



#from experiment_controller.comsim import ComSimController as CurrentController
from experiment_controller.morse import MorseController as CurrentController
#from controller.tronix import TronicController as CurrentController


from time import time, sleep
import sys
import subprocess

import numpy as np

from neat import population, visualize

from examples.neat.pybrain_agent import NeatAgent

from pybrain.rl.experiments import EpisodicExperiment

from pybrain_extension.environment.morse_environment import ContinuousControllerEnvironment
from pybrain_extension.task.red_cube_task import CameraPixelsRedCubeTask

try:
    import __builtin__
    input = getattr(__builtin__, 'raw_input')
except (ImportError, AttributeError):
    pass


with CurrentController(3) as control:
    environment = ContinuousControllerEnvironment(control)
    task = CameraPixelsRedCubeTask(environment, True)

    experiment = EpisodicExperiment(task, None)

    # control.calibrate()

    start = time()
    bias = True

    def eval_fitness(genomes):
        for g in genomes:
            # visualize.draw_net(g, view=False)
            agent = NeatAgent(g, bias=bias)
            g.fitness = 0
            for state in range(control.get_randomize_states()):
                control.randomize(state)
                g.fitness += task.f(agent)
                if not task.found_cube:
                    break
            print("fitness %f" % g.fitness)
            with open('rewards.csv','a') as f:
                f.write("%f,%d\n" % (task.getTotalReward(), time() - start))

    checkpoint = None if len(sys.argv) <= 1 else str(sys.argv[1])
    pop = population.Population('examples/neat/neat_config', checkpoint_file=checkpoint)
    pop.config.input_nodes = task.outdim + 1 if bias else task.outdim
    pop.config.output_nodes = task.indim

    control.cubes_x = 2
    control.cubes_y = 4
    control.cubes_size = 3
    task.max_samples = 180
    pop.epoch(eval_fitness, 90, checkpoint_interval=0)

    winner = pop.most_fit_genomes[-1]
    print('Number of evaluations: {0:d}'.format(winner.ID))

    # Visualize the winner network and plot statistics.
    visualize.plot_stats(pop.most_fit_genomes, pop.avg_fitness_scores)
    visualize.plot_species(pop.species_log)
    visualize.draw_net(winner, view=False)



