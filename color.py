import math
from helper import clamp

def linear_to_gamma(linear_component):
    if (linear_component > 0):
        return math.sqrt(linear_component)
    return 0

def write_color(pixel_color):
    r = pixel_color[0]
    g = pixel_color[1]
    b = pixel_color[2]
    
    r = linear_to_gamma(r)
    g = linear_to_gamma(g)
    b = linear_to_gamma(b)
    
    rbyte = int(256 * clamp(r, 0.000, 0.999))
    gbyte = int(256 * clamp(g, 0.000, 0.999))
    bbyte = int(256 * clamp(b, 0.000, 0.999))
    
    print(f"{rbyte} {gbyte} {bbyte}")
    

