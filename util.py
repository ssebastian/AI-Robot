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



# from colormath.color_objects import sRGBColor, LabColor
# from colormath.color_conversions import convert_color
# from colormath.color_diff import delta_e_cie2000
#
# # global target_color
# target_color = convert_color(sRGBColor(1.0, 0.0, 0.0, is_upscaled=False), LabColor) # red
#
#
# def set_target_color(col):
#     global target_color
#     target_color = convert_color(sRGBColor(col[0], col[1], col[2], is_upscaled=True), LabColor)
#
#
# def red_pixel_dist(x):
#     global target_color
#     color = convert_color(sRGBColor(x[0], x[1], x[2], is_upscaled=True), LabColor)
#     #print(color)
#     #print(target_color)
#     delta_e = delta_e_cie2000(target_color, color)
#     #return x[2] > 100 and x[2] > x[1] * 3. and x[2] > x[0] * 3.
#     #print("delta_e: %f"% delta_e)
#     return delta_e


def red_pixel(x):
    return x[0] > 100 and x[0] > x[1] * 2. and x[0] > x[2] * 2.


# def get_red_pixels(image):
#     rows, cols, channels = image.shape
#     image_reshaped = image.reshape((rows*cols,channels))
#     filtered = filter(lambda x: red_pixel(x), image_reshaped)
#     return float(len(list(filtered))) / float(len(image_reshaped))
#     #print("calculate...")
#     #result = sum(x[0]>x[1]*2 and x[0]>x[2]*2 for x in image_reshaped)
#     #print("ok!")
#     #return result


