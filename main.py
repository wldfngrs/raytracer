from camera import Camera
from hittablelist import HittableList
from sphere import Sphere
from material import *

if __name__ == "__main__":
    world = HittableList()
    
    material_center = Lambertian(np.array([0.1, 0.2, 0.5]))
    
    point = Sphere(np.array([0.0, 0.0, -1.2]), 0.5, material_center)
    world.add(point)
    
    camera = Camera()
    
    camera.aspect_ratio = 16.0 / 9.0
    camera.image_width = 400
    camera.samples_per_pixel = 100
    camera.max_depth = 50
    
    camera.render(world)