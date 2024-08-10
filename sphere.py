from hittable import Hittable, HitRecord
from ray import Ray
from helper import surrounds
import numpy as np
import math

class Sphere(Hittable):
    def __init__(self, center, radius, material):
        self.__center = center
        self.__radius = radius
        self.__material = material
        
    def hit(self, ray : Ray, min, max, rec : HitRecord):
        oc = self.__center - ray.origin()
        a = np.linalg.norm(ray.direction()) ** 2
        h = np.dot(ray.direction(), oc)
        c = (np.linalg.norm(oc) ** 2) - self.__radius * self.__radius
        
        discriminant = h * h - a * c
        if discriminant < 0:
            return False
        
        sqrtd = math.sqrt(discriminant)
        
        root = (h - sqrtd) / a
        if surrounds(root, min, max) == False:
            root = (h + sqrtd) / a
            if surrounds(root, min, max) == False:
                return False
            

        rec.t = root
        rec.p = ray.at(rec.t)
        rec.normal = (rec.p - self.__center) / self.__radius
        outward_normal = (rec.p - self.__center) / self.__radius
        rec.set_face_normal(ray, outward_normal)
        rec.material = self.__material
        
        return True
                