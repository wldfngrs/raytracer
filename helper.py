import numpy as np
import random
import math

class ASWrapper():
    def __init__(self, attenuation, scattered):
        self.attenuation = attenuation
        self.scattered = scattered
    

def normalize(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

def clamp(x, min, max):    
    if x < min:
        return min
    if x > max:
        return max
    return x

def surrounds(x, min, max):
    return min < x and x < max

def random_in_unit_disk():
    while True:
        p = np.array([random.uniform(-1, 1), random.uniform(-1, 1), 0])
        if np.linalg.norm(p) < 1:
            return p
        
def random_double():
    return random.uniform(0, 1)

def random_in_unit_sphere():
    while True:
        p = np.array([random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)])
        if np.linalg.norm(p) < 1:
            return p

def random_unit_vector():
    return normalize(random_in_unit_sphere())

def absolute_value(vector):
    return np.array([abs(vector[0]), abs(vector[1]), abs(vector[2])])

def near_zero(vector):
    return abs(vector[0]) < 1e-8 and abs(vector[1]) < 1e-8 and abs(vector[2]) < 1e-8

def reflect(vectorV, vectorN):
    return vectorV - 2 * np.dot(vectorV, vectorN) * vectorN

def refract(uv, n, etai_over_etat):
    cos_theta = min(np.dot(-uv, n), 1.0)
    r_out_perp = etai_over_etat * (uv + cos_theta * n)
    r_out_parallel = -math.sqrt(abs(1.0 - (np.linalg.norm(r_out_perp) ** 2)) * n)
    return r_out_perp + r_out_parallel