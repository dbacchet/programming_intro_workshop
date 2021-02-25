import unittest

from vector import *
from physics import PhysicsObject, PhysicsSystem

class TestPhysics(unittest.TestCase):
    def test_integrate(self):
        obj1 = PhysicsObject(1,1.5,Vector2d(10,10), Vector2d(1,0))
        obj2 = PhysicsObject(1,0.5,Vector2d(20,10), Vector2d(-1,0))
        ps = PhysicsSystem()
        ps.add_object(obj1)
        ps.add_object(obj2)
        # update
        ps.update(0.1)
        self.assertEqual(obj1.pos.x, 10.1)
        self.assertEqual(obj1.pos.y, 10)
        self.assertEqual(obj1.pos, Vector2d(10.1,10))
        self.assertEqual(obj2.pos, Vector2d(19.9,10))
        # for o in ps.objects:
        #     print(o)

    def test_collisions(self):
        obj1 = PhysicsObject(2,1.0,Vector2d(1,0), Vector2d(0,0))
        obj2 = PhysicsObject(1,1.0,Vector2d(-1,0), Vector2d(0,0))
        ps = PhysicsSystem()
        ps.add_object(obj1)
        ps.add_object(obj2)
        # update
        for i in range(10):
            ps.update(0.1)
            self.assertEqual(obj1.acc, Vector2d())
            self.assertEqual(obj2.acc, Vector2d())
            # for o in ps.objects:
            #     print(o)
        # make the objects collide
        obj1.pos = Vector2d(0.9,0)
        obj2.pos = Vector2d(-0.9,0)
        # update
        for i in range(10):
            ps.update(0.1)
            # self.assertEqual(obj1.acc, Vector2d())
            # self.assertEqual(obj2.acc, Vector2d())
            # for o in ps.objects:
            #     print(o)


if __name__ == '__main__':
    unittest.main()
