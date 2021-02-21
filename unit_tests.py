import unittest

from vector import *
from physics import PhysicsObject, PhysicsSystem

class TestVector(unittest.TestCase):
    def test_creation(self):
        v = Vector2d()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)
        v = Vector2d(1,2)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)
        self.assertEqual(v,Vector2d(1,2))

    def test_math(self):
        v1 = Vector2d(1,2)
        v2 = Vector2d(3,4.5)
        # v = v1.add(v2)
        # self.assertEqual(v.x, 4)
        # self.assertEqual(v.y, 6.5)
        # v = v1.sub(v2)
        # self.assertEqual(v.x, -2)
        # self.assertEqual(v.y, -2.5)
        # v = v1.mul(3.0)
        # self.assertEqual(v.x, 3)
        # self.assertEqual(v.y, 6)
        # use operators
        v = v1 + v2
        self.assertEqual(v.x, 4)
        self.assertEqual(v.y, 6.5)
        v = v1 - v2
        self.assertEqual(v.x, -2)
        self.assertEqual(v.y, -2.5)
        v = v1 * 3
        self.assertEqual(v.x, 3)
        self.assertEqual(v.y, 6)
        # length
        v = Vector2d(3,4)
        self.assertEqual(v.length(), 5)

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
        for o in ps.objects:
            print(o)

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
            for o in ps.objects:
                print(o)
        # make the objects collide
        obj1.pos = Vector2d(0.9,0)
        obj2.pos = Vector2d(-0.9,0)
        # update
        for i in range(10):
            ps.update(0.1)
            # self.assertEqual(obj1.acc, Vector2d())
            # self.assertEqual(obj2.acc, Vector2d())
            for o in ps.objects:
                print(o)


if __name__ == '__main__':
    unittest.main()
