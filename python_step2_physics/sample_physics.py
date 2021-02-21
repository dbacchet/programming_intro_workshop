from vector import *
from physics import *

from renderer import SimpleRenderer

def simple_collision():
    obj1 = PhysicsObject(1.0, 1.0, Vector2d(0,0), Vector2d(3,0))
    obj2 = PhysicsObject(2.0, 0.5, Vector2d(10,0.5), Vector2d(-2,0))
    ps = PhysicsSystem()
    ps.add_object(obj1)
    ps.add_object(obj2)
    # setup renderer and run
    renderer = SimpleRenderer
    renderer.objects = ps.objects
    renderer.callback = ps.update
    renderer.run()

def random_agents():
    import random
    random.seed(12345678)

    obj1 = PhysicsObject(1.0, 1.0, Vector2d(0,0), Vector2d(3,0))
    obj2 = PhysicsObject(2.0, 0.5, Vector2d(10,0.5), Vector2d(-2,0))
    ps = PhysicsSystem()
    ps.add_object(obj1)
    ps.add_object(obj2)
    # add a bunch of randomly placed objects
    for i in range(150):
        obj = PhysicsObject(random.uniform(0.5,2.0), random.uniform(0.5,1.5), 
                            Vector2d(random.uniform(-100,100), random.uniform(-100,100)), 
                            Vector2d(random.uniform(-5,5), random.uniform(-5,5)))
        ps.add_object(obj)
    # setup renderer and run
    renderer = SimpleRenderer
    renderer.objects = ps.objects
    renderer.callback = ps.update
    renderer.run()

if __name__ == "__main__":
    # simple_collision()
    random_agents()
