import numpy as np
from ray import Ray

class HitRecord():
    def __init__(self):
        self.p = np.array([0, 0, 0])
        self.normal = np.array([0, 0, 0])
        self.t = 0.0
        
    def set_face_normal(self, ray, outward_normal):
        self.front_face = np.dot(ray.direction(), outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal
        
class Hittable():
    def hit(self, ray : Ray, min, max, rec : HitRecord):
        print("Hittable hit")
        
