from hittable import HitRecord
from ray import Ray
from helper import *

import math
import numpy as np

class Material():
    def scatter(self, ray_in, rec, attenuation, scatter):
        return False

class Lambertian(Material):
    def __init__(self, albedo):
        self.__albedo = albedo

    def scatter(self, ray_in, rec, wrapper : ASWrapper):
        scatter_direction = rec.normal + random_unit_vector()

        if near_zero(scatter_direction):
            scatter_direction = rec.normal

        wrapper.scattered = Ray(rec.p, scatter_direction)
        wrapper.attenuation = self.__albedo
        return True
    
class Metal(Material):
    def __init__(self, albedo, fuzz):
        self.__albedo = albedo
        self.__fuzz = fuzz
        
    def scatter(self, ray_in, rec, wrapper):
        reflected = reflect(ray_in.direction(), rec.normal)
        reflected = normalize(reflected) + (self.__fuzz + random_unit_vector())
        wrapper.scattered = Ray(rec.p, reflected)
        wrapper.attenuation = self.__albedo
        return np.dot(wrapper.scattered.direction(), rec.normal) > 0
    
class Dielectric(Material):
    def __init__(self, refraction_index):
        self.__refraction_index = refraction_index
        
    def scatter(self, ray_in, rec, wrapper):
        wrapper.attenuation = np.array([1.0, 1.0, 1.0])
        ri = 1.0 / self.__refraction_index if rec.front_face else self.__refraction_index
        
        unit_direction = normalize(ray_in.direction())
        cos_theta = min(np.dot(-unit_direction, rec.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)
        
        cannot_reflect = (ri * sin_theta) > 1.0
        direction : np.array
        
        if cannot_reflect or self.__reflectance(cos_theta, ri) > random_double():
            direction = reflect(unit_direction, rec.normal)
        else:
            direction = refract(unit_direction, rec.normal, ri)
            
        wrapper.scattered = Ray(rec.p, direction)
        
    def __reflectance(cosine, refraction_index):
        r0 = (1 - refraction_index) / (1 + refraction_index)
        r0 = r0 * r0
        return r0 + (1 - r0) * math.pow((1 - cosine), 5)