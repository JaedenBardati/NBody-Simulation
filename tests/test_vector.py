"""
Tests for the nbody file.
Yes, this is likely quite excessive.
"""

import math
import unittest

from src.vector import Vector


class TestVectorAccess(unittest.TestCase):

    def test_vector_get_x(self):
        self.assertEqual(Vector(1, 2, 3).x, 1, msg="vector.x must return the x value.")

    def test_vector_get_y(self):
        self.assertEqual(Vector(1, 2, 3).y, 2, msg="vector.y must return the y value.")

    def test_vector_get_z(self):
        self.assertEqual(Vector(1, 2, 3).z, 3, msg="vector.z must return the z value.")

    def test_vector_index_0(self):
        self.assertEqual(Vector(1, 2, 3)[0], 1, msg="vector[0] must return the x value.")

    def test_vector_index_1(self):
        self.assertEqual(Vector(1, 2, 3)[1], 2, msg="vector[1] must return the y value.")

    def test_vector_index_2(self):
        self.assertEqual(Vector(1, 2, 3)[2], 3, msg="vector[2] must return the z value.")



class TestVectorEquality(unittest.TestCase):

    def test_vector_equal_to_vector(self):
        self.assertEqual(Vector(-1, 0, 3.14), Vector(-1, 0, 3.14), msg="Vectors equality failed.")

    def test_vector_not_equal_to_vector(self):
        self.assertNotEqual(Vector(1, 0, 3), Vector(1, 0, 2.99), msg="Vectors strict inequality failed.")


    def test_2D_vector_equal_to_3D_vector(self):
        self.assertEqual(Vector(-1, 1.1), Vector(-1, 1.1, 0), msg="2D vectors must be the same as a 3D vector with 0 as the z value.")

    def test_2D_vector_not_equal_to_3D_vector(self):
        self.assertNotEqual(Vector(-1, 1.1), Vector(-1, 1.1, 1), msg="2D vectors must always be different from a 3D vector with a non zero z value.")


    def test_vector_equal_to_scalar(self):
        self.assertRaises(TypeError, Vector(1, 2, 3).__eq__, 1, msg="Vector equality with a scalar should not be possible.")

    def test_vector_not_equal_to_scalar(self):
        self.assertRaises(TypeError, Vector(1, 2, 3).__ne__, 1, msg="Vector strict inequality with a scalar should not be possible.")



class TestVectorAddition(unittest.TestCase):

    def test_vector_addition_with_vector(self):
        self.assertAlmostEqual(Vector(1, 2, -4.1) + Vector(0, -2, 3.1), Vector(1, 0, -1), msg="Vector addition with a vector failed.")      # Not exactly equal because of floating point rounding errors.

    def test_vector_subtraction_with_vector(self):
        self.assertAlmostEqual(Vector(1, 0, -1) - Vector(1, 2, -4.1), Vector(0, -2, 3.1), msg="Vector subtraction with a vector failed.")   # Not exactly equal because of floating point rounding errors.


    def test_vector_reverse_addition_with_vector(self):
        self.assertEqual(Vector(1, 2, -4.1) + Vector(0, -2, 3.1), Vector(0, -2, 3.1) + Vector(1, 2, -4.1), msg="Vector addition should be commutative.")

    def test_vector_reverse_subtraction_with_vector(self):
        self.assertNotEqual(Vector(1, 0, -1) - Vector(1, 2, -4.1), Vector(1, 2, -4.1) - Vector(1, 0, -1), msg="Vector subtraction should not be commutative.")


    def test_vector_addition_with_scalar(self):
        self.assertRaises(TypeError, Vector(1, 2, 3).__add__, 1, msg="Vector addition with a scalar should not be possible.")

    def test_vector_subtraction_with_scalar(self):
        self.assertRaises(TypeError, Vector(1, 2, 3).__sub__, 1, msg="Vector subtraction with a scalar should not be possible.")


    def test_vector_reverse_addition_with_scalar(self):
        self.assertRaises(TypeError, Vector(1, 2, 3).__radd__, 1, msg="Vector reverse addition with a scalar should not be possible.")

    def test_vector_reverse_subtraction_with_scalar(self):
        self.assertRaises(TypeError, Vector(1, 2, 3).__rsub__, 1, msg="Vector reverse subtraction with a scalar should not be possible.")



class TestVectorMultiplication(unittest.TestCase):
    
    def test_vector_multiplication_with_scalar(self):
        self.assertAlmostEqual(Vector(1, 2, 3) * 2.1, Vector(2.1, 4.2, 6.3), msg="Vector multiplication with a scalar failed.")     # Not exactly equal because of floating point rounding errors.

    def test_vector_true_division_with_scalar(self):
        self.assertEqual(Vector(1, 2, 3) / 2, Vector(0.5, 1, 1.5), msg="Vector true division with a scalar failed.")

    def test_vector_floor_division_with_scalar(self):
        self.assertEqual(Vector(1, 2, 3) // 2, Vector(0, 1, 1), msg="Vector floor division with a scalar failed.")


    def test_vector_multiplication_with_vector(self):
        self.assertRaises(TypeError, Vector(1, 2, 3).__mul__, Vector(2.1, 4.2, 6.3), msg="Vector multiplication with a vector must be specified.")

    def test_vector_division_with_vector(self):
        self.assertRaises(TypeError, Vector(1, 2, 3).__div__, Vector(0.5, 1, 1.5), msg="Vector division with a vector should not be possible.")

    def test_vector_true_division_with_vector(self):
        self.assertRaises(TypeError, Vector(1, 2, 3).__truediv__, Vector(0.5, 1, 1.5), msg="Vector true division with a vector should not be possible.")

    def test_vector_floor_division_with_vector(self):
        self.assertRaises(TypeError, Vector(1, 2, 3).__floordiv__, Vector(0, 1, 1), msg="Vector floor division with a vector should not be possible.")


    def test_vector_negative(self):
        self.assertEqual(-Vector(1, 2, 3), Vector(-1, -2, -3), msg="Vector negative has failed.")


    def test_vector_dot_product_vector(self):
        self.assertEqual(Vector(1, 2, 3).dot(Vector(4.45, 5.1, 6.8)), 35.05, msg="Vector dot producted with another vector failed.")

    def test_vector_cross_product_vector(self):
        self.assertAlmostEqual(Vector(1, 2, 3).cross(Vector(4.45, 5.1, 6.8)), Vector(-1.7, 6.55, -3.8), msg="Vector cross producted with another vector failed.")   # Not exactly equal because of floating point rounding errors.


    def test_vector_dot_product_scalar(self):
        self.assertRaises(TypeError, Vector(1, 2, 3).dot, 1, msg="Vector dot product with a scalar should not be possible.")

    def test_vector_cross_product_scalar(self):
        self.assertRaises(TypeError, Vector(1, 2, 3).cross, 1, msg="Vector cross product with a scalar should not be possible.")



class TestVectorNorm(unittest.TestCase):

    def test_vector_norm_positive_integers(self):
        self.assertEqual(Vector(9, 6, 2).norm(), 11, msg="Vector norm does not work for positive integer values.")

    def test_vector_norm_negatives(self):
        self.assertEqual(Vector(-9, 6, -2).norm(), Vector(-9, -6, 2).norm(), msg="Vector norm does not work for negative values.")
    
    def test_vector_norm_rationals(self):
        self.assertEqual(Vector(3, -4, 5).norm(), 5*math.sqrt(2), msg="Vector norm does not work for rationals.")

    def test_vector_abs_rationals(self):
        self.assertEqual(abs(Vector(3, -4, 5)), Vector(3, -4, 5).norm(), msg="Vector absolute value should conventionally equal the vector norm.")



class TestVectorString(unittest.TestCase):

    def test_repr_2D(self):
        self.assertEqual(str(Vector(1, 2)), '(1, 2)', msg="2D Vector string output must return the 2D vectors values in a 2D tuple.")

    def test_repr_3D_(self):
        self.assertEqual(str(Vector(1.0, 2, 3.14)), '(1.0, 2, 3.14)', msg="3D Vector string output must return a 3D vectors values in a 3D tuple.")



if __name__ == '__main__':
    unittest.main()

