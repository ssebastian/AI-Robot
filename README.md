# Install environment:

To use this project one needs to install the following python dependencies:
```
matplotlib, scipy, numpy, pillow, readchar, shapely, descartes, neat-python(0.5)
```

Instalation example for Ubuntu envrionment:
```
sudo apt-get install python3-pip
sudo apt-get install python-dev libfreetype6-dev libpng-dev libjpeg-dev libjpeg8-dev libpng3
sudo apt-get install python-matplotlib
pip install --user scipy numpy pillow readchar shapely descartes
pip install --user neat-python==0.5
```


# Start

Neat:
```
python -m examples/neat/train
```

Q-Learning:
```
python -m examples/q_learn/train
```


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
