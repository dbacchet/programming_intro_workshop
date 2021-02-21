import math

class Vector2d(object):
    def __init__(self, x=0.0, y=0.0):
        self.x=x
        self.y=y

    def add(self, other):
        v = Vector2d()
        v.x = self.x + other.x
        v.y = self.y + other.y
        return v

    def sub(self, other):
        v = Vector2d()
        v.x = self.x - other.x
        v.y = self.y - other.y
        return v

    def mul(self, scalar):
        v = Vector2d()
        v.x = self.x * scalar
        v.y = self.y * scalar
        return v

    def __add__(self, other):
        v = Vector2d()
        v.x = self.x + other.x
        v.y = self.y + other.y
        return v

    def __sub__(self, other):
        v = Vector2d()
        v.x = self.x - other.x
        v.y = self.y - other.y
        return v
        
    def __mul__(self, scalar):
        v = Vector2d()
        v.x = self.x * scalar
        v.y = self.y * scalar
        return v

    def __truediv__(self, scalar):
        v = Vector2d()
        v.x = self.x / scalar
        v.y = self.y / scalar
        return v

    def __eq__(self, other):
        return abs(self.x-other.x)<1E-6 and abs(self.y-other.y)<1E-6

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def length(self):
        return math.sqrt(self.x*self.x + self.y*self.y)
