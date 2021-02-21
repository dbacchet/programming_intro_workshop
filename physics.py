import math
from vector import *

class PhysicsObject(object):
    def __init__(self, mass = 1.0, radius=1.0, pos=Vector2d(), vel=Vector2d()):
        self.mass = mass
        self.radius = radius
        self.pos = pos
        self.vel = vel
        self.acc = Vector2d()

    def __str__(self):
        return "pos: {} vel: {}, acc:{}, mass:{}, radius:{}".format(self.pos, self.vel, self.acc, self.mass, self.radius)

class PhysicsSystem(object):
    def __init__(self): 
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def update(self, dt):
        # reset ephemeral state
        for obj in self.objects:
            obj.acc = Vector2d(0,0)
        # collisions
        self.process_collisions()
        # integrate dynamics
        for obj in self.objects:
            obj.vel = obj.vel + obj.acc*dt
            if (obj.vel.length()>5):
                obj.vel = obj.vel * 0.9
            obj.pos = obj.pos + obj.vel*dt
            if (obj.pos.x>100): obj.pos.x = -100
            if (obj.pos.y>100): obj.pos.y = -100
            if (obj.pos.x<-100): obj.pos.x = 100
            if (obj.pos.y<-100): obj.pos.y = 100

    def process_collisions(self):
        for obj1 in self.objects:
            # check collisions with every other object
            for obj2 in self.objects:
                # skip if two objs are the same
                if obj1 is obj2:
                    continue
                d = (obj1.pos-obj2.pos).length()
                if (d<1E-6): d=1E-6
                comp = obj1.radius+obj2.radius - d
                if comp>0:
                    # objects are colliding
                    direction = (obj1.pos-obj2.pos) / d;
                    stiffness = 1000;
                    obj1.acc = direction * comp * stiffness / obj1.mass
                    obj2.acc = direction * comp * stiffness / obj2.mass * -1
