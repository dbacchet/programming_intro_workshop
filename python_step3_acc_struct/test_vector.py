import unittest

from vector import *

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


if __name__ == '__main__':
    unittest.main()
