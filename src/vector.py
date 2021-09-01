"""
Contains the vector class.
"""

import math


class Vector():
    """A simple 3D/2D vector class. It contains operations such as vector addition, scalar multiplication, dot and cross products, norm, etc."""
    
    def __init__(self, x, y, z=None):
        if z == None:
            z = 0
        
        self.x, self.y, self.z = x, y, z

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        else:
            raise IndexError("Index must be 0, 1 or 2.")
    
    def __eq__(self, other):
        if type(other) == type(Vector(0, 0)):
            return self.x == other.x and self.y == other.y and self.z == other.z
        elif other == None:
            return False         # If this method is being called, it exists (and thus is not None).
        else:
            raise TypeError("Scalars cannot be equal to vectors!")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if type(other) == type(Vector(0, 0)):
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError("Scalars cannot be added to vectors!")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if type(other) == type(Vector(0, 0)):
            return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise TypeError("Scalars cannot be subtracted with vectors!")
    
    def __rsub__(self, other):
        return -self.__sub__(other)

    def __mul__(self, other):
        if type(other) == type(0) or type(other) == type(0.0):
            return Vector(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError("Only scalars can be multiplied with vectors! Use .dot() or .cross() to perform dot or cross products of vectors.")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if type(other) == type(0) or type(other) == type(0.0):
            return Vector(self.x / other, self.y / other, self.z / other)
        else:
            raise TypeError("Only scalars can be divided with vectors!")

    def __floordiv__(self, other):
        if type(other) == type(0) or type(other) == type(0.0):
            return Vector(self.x // other, self.y // other, self.z // other)
        else:
            raise TypeError("Only scalars can be divided with vectors!")

    def __div__(self, other):       # Python2 support
        if type(other) == type(0) or type(other) == type(0.0):
            return Vector(float(self.x) / other, float(self.y) / other, float(self.z) / other)
        else:
            raise TypeError("Only scalars can be divided with vectors!")

    def __neg__(self):
        return self.__mul__(-1)

    def __abs__(self):
        return self.norm()

    def __repr__(self):
        if self.z == 0:
            return str((self.x, self.y))
        return str((self.x, self.y, self.z))


    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def dot(self, other):
        # Computes dot product.
        if type(other) == type(Vector(0, 0)):
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            raise TypeError("Dot products must be done with vectors!")

    def cross(self, other):
        # Computes cross product.
        if type(other) == type(Vector(0, 0)):
            return Vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)
        else:
            raise TypeError("Cross products must be done with vectors!")

