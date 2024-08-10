import logging
import math

import numpy as np

from hittable import Hittable, HitRecord
from ray import Ray
from helper import *
from color import write_color

class Camera():
    def __init__(self):
        self.image_width = 100
        self.aspect_ratio = 1.0
        self.samples_per_pixel = 10
        self.max_depth = 10

        self.vertical_fov = 90
        self.look_from = np.array([0, 0, 0])
        self.look_at = np.array([0, 0, -1])
        self.world_up = np.array([0, 1, 0])
        
        self.defocus_angle = 0
        self.focus_dist = 10
        
    def render(self, world : Hittable):
        self.__initialize()
            
        print(f"P3\n {self.image_width} {self.__image_height}\n255")
           
        for j in range(self.__image_height):
            logging.info(f"\r{(j / self.__image_height) * 100}")
            for i in range(self.image_width):
                pixel_color = np.array([0.0, 0.0, 0.0])
                
                for _ in range(self.samples_per_pixel):
                    ray = self.__get_ray(i, j)
                    pixel_color += self.__ray_color(ray, self.max_depth, world)
                    
                write_color(self.__pixel_samples_scale * pixel_color)
            

# private
    def __initialize(self):
        self.__image_height = int(self.image_width / self.aspect_ratio)
        self.__image_height = 1 if self.__image_height < 1 else self.__image_height
        
        self.__pixel_samples_scale = 1.0 / self.samples_per_pixel
        
        self.__center = self.look_from;

        h = math.tan(self.vertical_fov)
        viewport_height = 2 * h * self.focus_dist
        viewport_width = viewport_height * self.image_width / self.__image_height
        
        self.__w = normalize(self.look_from - self.look_at)
        self.__u = normalize(np.cross(self.world_up, self.__w))
        self.__v = np.cross(self.__w, self.__u)
        
        viewport_u = viewport_width * self.__u
        viewport_v = viewport_height * -self.__v
        
        self.__pixel_delta_u = viewport_u / self.image_width
        self.__pixel_delta_v = viewport_v / self.__image_height
        
        viewport_upper_left = self.__center - (self.focus_dist * self.__w) - viewport_u /2 - viewport_v / 2
        self.__pixel00_loc = viewport_upper_left + 0.5 * (self.__pixel_delta_u + self.__pixel_delta_v)
        
        defocus_radius = self.focus_dist * math.tan(self.defocus_angle / 2)
        self.__defocus_disk_u = self.__u * defocus_radius
        self.__defocus_disk_v = self.__v * defocus_radius
        
    def __get_ray(self, i, j):
        offset = self.__sample_square()
        pixel_sample = self.__pixel00_loc + ((i + offset[0]) * self.__pixel_delta_u) + ((j + offset[1]) * self.__pixel_delta_v)
        
        ray_origin = self.__center if (self.defocus_angle) <= 0 else self.__defocus_disk_sample()
        ray_direction = pixel_sample - ray_origin
        
        return Ray(ray_origin, ray_direction)
    
    def __sample_square(self):
        return np.array([random_double() - 0.5, random_double() - 0.5, 0])
    
    def __defocus_disk_sample(self):
        p = random_in_unit_disk()
        return self.__center + (p[0] + self.__defocus_disk_u) + (p[1] + self.__defocus_disk_v)
    
    def __ray_color(self, ray : Ray, depth : int, world : Hittable):
        if depth <= 0:
            return np.array([0, 0, 0])
        
        rec = HitRecord()
        
        if world.hit(ray, 0.001, math.inf,  rec):
            attenuation = np.array([0, 0, 0])
            scattered = np.array([0, 0, 0])
            wrapper = ASWrapper(attenuation, scattered)
            if rec.material.scatter(ray, rec, wrapper):
                return wrapper.attenuation * self.__ray_color(wrapper.scattered, depth - 1, world)
            
            return np.array([0, 0, 0])
        
        unit_direction = normalize(ray.direction())
        a = 0.5 * (unit_direction[1] + 1.0)
        return ((1.0 - a) * np.array([1.0, 1.0, 1.0])) + (a * np.array([0.5, 0.7, 1.0]))
        
        