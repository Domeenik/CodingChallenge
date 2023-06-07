from src.vectors import Vector2
import unittest
import math

class TestVector2(unittest.TestCase):
    
    def setUp(self):
        self.v1 = Vector2(3,4)
        self.v2 = Vector2(-2,1)
    
    def test___new__(self):
        va = Vector2(1,2)
        vb = Vector2([1,2])
        self.assertEqual(va.x(), vb.x())
        self.assertEqual(va.y(), vb.y())
        self.assertListEqual(list(va), list(vb))
        vc = Vector2(va)
        self.assertListEqual(list(vc), list(vb))
        with self.assertRaises(TypeError):
            v4 = Vector2("string")
        with self.assertRaises(IndexError):
            v4 = Vector2(1,2,3)
            
    def test___add__(self):
        self.assertEqual(list(self.v1 + self.v2), list(Vector2(1, 5)))
        
    def test___sub__(self):
        self.assertEqual(list(self.v1 - self.v2), list(Vector2(5, 3)))
        
    def test___mul__(self):
        self.assertEqual(self.v1 * self.v2, -2)
        self.assertEqual(list(self.v2 * 2), list(Vector2(-4,2)))
        
    def test___floordiv__(self):
        self.assertEqual(list(self.v2//2), list(Vector2(-1, 0)))
        
    def test___floordiv__(self):
        self.assertEqual(list(self.v2/2), list(Vector2(-1, 0.5)))
        
    def test_length(self):
        self.assertEqual(self.v2.length(), math.sqrt(5))
        
    def test_norm(self):
        self.assertEqual(list(self.v2.norm()), list(Vector2(-2,1)/self.v2.length()))
        
    def test_distance_to(self):
        self.assertEqual(self.v1.distance_to(self.v2), 5.830951894845301)
                
    def test_x(self):
        self.assertEqual(self.v2.x(), list(self.v2)[0])
        
    def test_y(self):
        self.assertEqual(self.v2.y(), list(self.v2)[1])
        
    def test_xy(self):
        self.assertEqual(list(self.v2.xy()), list(self.v2))
        
    def test_set_x(self):
        self.v2.set_x(4)
        self.assertEqual(list(self.v2), list(Vector2(4,1)))
        
    def test_set_y(self):
        self.v2.set_y(-2)
        self.assertEqual(list(self.v2), list(Vector2(-2,-2)))