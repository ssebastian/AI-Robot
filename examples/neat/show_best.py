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



# from experiment_controller.comsim import ComSimController as CurrentController
# from experiment_controller.morse import MorseController as CurrentController
from experiment_controller.tronix import TronixController as CurrentController

import sys
import os

from neat import population, visualize

from examples.neat.pybrain_agent import NeatAgent

from pybrain.rl.experiments import EpisodicExperiment

from pybrain_extension.environment.morse_environment import ContinuousControllerEnvironment, ControllerEnvironment
from pybrain_extension.task.red_cube_task import CameraPixelsRedCubeTask


try:
    import __builtin__
    input = getattr(__builtin__, 'raw_input')
except (ImportError, AttributeError):
    pass


with CurrentController(3) as control:
    environment = ContinuousControllerEnvironment(control)
    task = CameraPixelsRedCubeTask(environment, True)

    path = "" if len(sys.argv) <= 1 else str(sys.argv[1])
    best_n = 3 if len(sys.argv) <= 2 else str(sys.argv[2])

    control.cubes_x = 3
    control.cubes_y = 4
    control.cubes_size = 3
    task.max_samples = 1000

    i = 0
    while os.path.isfile(os.path.join(path, "checkpoint_%d" % i)):
        checkpoint = os.path.join(path, "checkpoint_%d" % i)
        print("load checkpoint %d" % i)
        pop = population.Population('approach/neat/neat_config', checkpoint_file=checkpoint)

        for n in reversed(range(1, min(best_n, len(pop.most_fit_genomes))+1)):
            control.pause()
            input("run %d. best in checkpoint %d" % (n, i))

            winner = pop.most_fit_genomes[-1]

            agent = NeatAgent(winner, True)

            for state in range(control.get_randomize_states()):
                control.randomize(state)
                task.f(agent)
                control.pause()

            visualize.draw_net(winner, view=False)

        # Visualize the winner network and plot statistics.
        visualize.plot_stats(pop.most_fit_genomes, pop.avg_fitness_scores)
        visualize.plot_species(pop.species_log)

        i += 1


