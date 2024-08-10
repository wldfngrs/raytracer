class Ray():
    def __init__(self, origin, direction):
        self.__origin  = origin
        self.__direction = direction
        
    def origin(self):
        return self.__origin
    
    def direction(self):
        return self.__direction
    
    def at(self, t):
        return self.__origin + (t * self.__direction)