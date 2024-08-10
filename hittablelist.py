from hittable import *

class HittableList(Hittable):
    def __init__(self):
        self.objects = []
    
    def clear(self):
        self.objects.clear()
        
    def add(self, object):
        self.objects.append(object)
        
    def hit(self, ray, min, max, rec):
        temp_rec = HitRecord()
        hit_anything = False
        closest_so_far = max
        
        for object in self.objects:
            if object.hit(ray, min, closest_so_far, temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t
                rec.p = temp_rec.p
                rec.normal = temp_rec.normal
                rec.material = temp_rec.material
                rec.t = temp_rec.t
                rec.front_face = temp_rec.front_face
        
        return hit_anything