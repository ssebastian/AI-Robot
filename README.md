# Ai Robot
This project is meant to learn aritificial intelligence algorithms. You can run the algorithms in a real environment (ultimate 4tronix initio) or in simulation. We have two different simulations. First you can use MORSE, a robot simulation environment based on blender. Thus it has a quite real physics engine and is close to reality. Second you can use a optimized simulation tool that is simulating the environment using computational geometry (in 2D) and is very fast.

# Install environment:

To use this project one needs to install the following python dependencies:
```
matplotlib, scipy, numpy, pillow, readchar, shapely, descartes, neat-python(0.5)
```

Instalation example for Ubuntu envrionment:
```
sudo apt-get install python3-pip
sudo apt-get install python-dev libfreetype6-dev libpng-dev libjpeg-dev libjpeg8-dev libpng3
sudo apt-get install morse-simulator
sudo apt-get install python-matplotlib
pip install --user scipy numpy pillow readchar shapely descartes
pip install --user neat-python==0.5
```

Import the morse project:
```
morse import /path/to/project/simulator/morse_sim/
```


# Start

If you are using the morse simulator, start the simulator with:
```
morse run morse_sim
```

Neat:
```
python -m examples/neat/train
```

Q-Learning:
```
python -m examples/q_learn/train
```

This project is in a very early state. Please feel free to open issues whenever something is not working (or if I forgot to describe something).


# Copyright
Copyright 2016 Sebastian Schmoll

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
