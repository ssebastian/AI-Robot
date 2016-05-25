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
from shapely import affinity
from shapely.geometry import Polygon, LineString, Point
from descartes import PolygonPatch
from matplotlib import pyplot as plt


class _Robot:
    bounding_x = 0.2
    bounding_y = 0.4

    def __init__(self):
        self.pos = Point([0,0])
        self.rotation = 0

    def get_bounding_box(self, x=None, y=None, rotation=None):
        x = self.pos.x if x is None else x
        y = self.pos.y if y is None else y
        rotation = self.rotation if rotation is None else rotation
        return affinity.rotate(Polygon([
                [x+self.bounding_x, y+self.bounding_y],
                [x+self.bounding_x, y-self.bounding_y],
                [x-self.bounding_x, y-self.bounding_y],
                [x-self.bounding_x, y+self.bounding_y]]),
            rotation, origin=self.pos, use_radians=True)


class ComSim:

    infrared_length = 3
    infrared_width = 0.5

    def __init__(self, red_pixel_sensors, camera_field_of_view=0.610865111, width=50, height=50):
        self._red_cubes = []
        self._obstacles = []
        self._width = width
        self._height = height
        self._red_pixel_sensors = red_pixel_sensors
        self._fov = camera_field_of_view
        self._robot = _Robot()
        self.fig = None
        self.area = Polygon([[0,0], [height,0], [height,width], [0,width]])

    def clear_env(self):
        self._red_cubes = [] #.clear()
        self._obstacles = [] #.clear()
        self.reset()

    def reset(self):
        self._robot.pos.coords = (self._width/2, self._height/2)
        self._robot.rotation = 0

    def add_red_cube(self, x, y, size=5):
        self._red_cubes.append(Polygon([
            [x-size/2, y-size/2],[x-size/2, y+size/2],
            [x+size/2, y+size/2],[x+size/2, y-size/2] ]))

    def add_obstacle(self, x, y, size=5):
        self._obstacles.append(Polygon([
            [x-size/2, y-size/2],[x-size/2, y+size/2],
            [x+size/2, y+size/2],[x+size/2, y-size/2] ]))

    def do(self, action, dt):
        w = action[0] + action[1]
        v = action[0] - action[1]
        w /= 2
        v /= 4

        rotation = self._robot.rotation + v * dt
        x = self._robot.pos.x + w * np.cos(rotation) * dt
        y = self._robot.pos.y + w * np.sin(rotation) * dt

        bounding_box = self._robot.get_bounding_box(x, y, rotation)

        collision = not (0 < x < self._width and 0 < y < self._height)
        if not collision:
            collision = np.array([bounding_box.intersects(cube) for cube in self._red_cubes]).any()
        if not collision:
            collision = np.array([bounding_box.intersects(cube) for cube in self._obstacles]).any()
        if not collision:
            self._robot.rotation = rotation
            self._robot.pos.coords = (x, y)

    def red_pixels(self):
        pixels = np.zeros(self._red_pixel_sensors)
        for i in range(self._red_pixel_sensors):
            rotation = self._robot.rotation - self._fov / 2 + i * self._fov / (self._red_pixel_sensors-1)
            ray = affinity.rotate(
                LineString([np.array(self._robot.pos.coords)[0],
                            np.array(self._robot.pos.coords)[0] + (self._height*2, 0)]),
                rotation, origin=self._robot.pos, use_radians=True)
            dists_red = np.min(np.array([self._robot.pos.distance(point) if not point.is_empty else np.inf
                                for point in (ray.intersection(cube) for cube in self._red_cubes)]))
            dists_obs = np.min(np.array([self._robot.pos.distance(point) if not point.is_empty else np.inf
                                for point in (ray.intersection(cube) for cube in
                                    #filter(lambda o: np.array([self._robot.pos.distance(Point(p)) < dists_red for p in o.exterior.coords]).any(),
                                           self._obstacles)]))
            pixels[i] = dists_red < dists_obs
        return pixels

    def infrared_left(self):
        ir = Polygon([
            np.array(self._robot.pos.coords)[0] + (self._robot.bounding_x, self._robot.bounding_y),
            np.array(self._robot.pos.coords)[0] + (self._robot.bounding_x, self._robot.bounding_y) + (self.infrared_length, -self.infrared_width),
            np.array(self._robot.pos.coords)[0] + (self._robot.bounding_x, self._robot.bounding_y) + (self.infrared_length,  self.infrared_width)])

        ir = affinity.rotate(ir, self._robot.rotation - 0.07, origin=self._robot.pos, use_radians=True)

        return not self.area.contains(ir) \
            or np.array([ir.intersects(cube) for cube in self._red_cubes]).any() \
            or np.array([ir.intersects(cube) for cube in self._obstacles]).any()

    def infrared_right(self):
        ir = Polygon([
            np.array(self._robot.pos.coords)[0] + (self._robot.bounding_x, self._robot.bounding_y),
            np.array(self._robot.pos.coords)[0] + (self._robot.bounding_x, self._robot.bounding_y) + (self.infrared_length, -self.infrared_width),
            np.array(self._robot.pos.coords)[0] + (self._robot.bounding_x, self._robot.bounding_y) + (self.infrared_length,  self.infrared_width)])

        ir = affinity.rotate(ir, self._robot.rotation + 0.07, origin=self._robot.pos, use_radians=True)

        return not self.area.contains(ir) \
            or np.array([ir.intersects(cube) for cube in self._red_cubes]).any() \
            or np.array([ir.intersects(cube) for cube in self._obstacles]).any()

    def show(self):
        if self.fig is None:
            plt.ion()
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111)
            self.ax.axis([0,self._width,0,self._height])
            plt.show()

        plt.cla()

        rob = PolygonPatch(self._robot.get_bounding_box())
        rob.set_color("b")
        self.ax.add_patch(rob)
        # rob = Polygon([[self._robot.x+.5, self._robot.y+1], [self._robot.x+.5, self._robot.y+1.1],
        #               [self._robot.x-.5, self._robot.y+1.1], [self._robot.x-.5, self._robot.y+1]])
        # rob = affinity.rotate(rob, self._robot.rotation, origin=(self._robot.x, self._robot.y), use_radians=True)
        # rob = PolygonPatch(rob)
        # rob.set_color("y")
        # self.ax.add_patch(rob)

        for i in range(self._red_pixel_sensors):
            rotation = self._robot.rotation - self._fov / 2 + i * self._fov / (self._red_pixel_sensors-1)
            ray = affinity.rotate(
                    LineString([
                        np.array(self._robot.pos.coords)[0],
                        np.array(self._robot.pos.coords)[0] + (self._height*2, 0)]),
                    rotation, origin=self._robot.pos, use_radians=True)
            patch = PolygonPatch(ray.buffer(0.1))
            patch.set_color("r")
            self.ax.add_patch(patch)

        for cube in self._red_cubes:
            patch = PolygonPatch(cube)
            patch.set_color("r")
            self.ax.add_patch(patch)

        for obstacle in self._obstacles:
            patch = PolygonPatch(obstacle)
            patch.set_color("b")
            self.ax.add_patch(patch)

        # plt.show()
        # self.fig.savefig()
        plt.pause(0.01)

