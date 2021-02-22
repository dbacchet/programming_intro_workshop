import unittest

from vector import *
from physics import PhysicsObject, PhysicsSystem
from grid import *

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

class TestGrid(unittest.TestCase):
    def test_grid(self):
        # default cell size
        grid = Grid()
        grid.add(Vector2d(0,0),"a")
        grid.add(Vector2d(3,1),"b")
        grid.add(Vector2d(0.1,0.1),"c")
        grid.add(Vector2d(-4,0),"d")
        grid.add(Vector2d(10,2),"e")
        objs = grid.objects_in_radius(Vector2d(0.1,0.1),1)
        self.assertEqual(len(objs), 2)
        self.assertTrue("a" in objs)
        self.assertTrue("c" in objs)
        objs = grid.objects_in_radius(Vector2d(0.1,0.1),5)
        self.assertEqual(len(objs), 4)
        self.assertTrue("a" in objs)
        self.assertTrue("b" in objs)
        self.assertTrue("c" in objs)
        self.assertTrue("d" in objs)
        objs = grid.objects_in_radius(Vector2d(-10.1,0),5)
        self.assertEqual(len(objs), 0)
        # different cell size
        grid = Grid(cell_side_len=2.1)
        grid.add(Vector2d(0,0),"a")
        grid.add(Vector2d(3,1),"b")
        grid.add(Vector2d(0.1,0.1),"c")
        grid.add(Vector2d(-4,0),"d")
        grid.add(Vector2d(10,2),"e")
        objs = grid.objects_in_radius(Vector2d(0.1,0.1),1)
        self.assertEqual(len(objs), 3) # the bigger cell size will return also "d"
        self.assertTrue("a" in objs)
        self.assertTrue("b" in objs)
        self.assertTrue("c" in objs)
        objs = grid.objects_in_radius(Vector2d(0.1,0.1),5)
        self.assertEqual(len(objs), 4)
        self.assertTrue("a" in objs)
        self.assertTrue("b" in objs)
        self.assertTrue("c" in objs)
        self.assertTrue("d" in objs)
        objs = grid.objects_in_radius(Vector2d(-15.1,0),5)
        self.assertEqual(len(objs), 0)

if __name__ == '__main__':
    unittest.main()
