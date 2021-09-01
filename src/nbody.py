"""
Contains the astronomical Body and Nbody classes.
It deals with the physics of the simulation.
"""

import os

from . import data_parse as dp
from .vector import Vector


G = dp.getConstantFromSymbol('G')
PI = dp.getConstantFromName('Pi')


class Body:
    """An astronomical body class. It contains data methods for the properties of an astronomical body such as its motion over time. Enter data in SI units."""
    
    def __init__(self, name, mass, radius, rotational_velocity=None, obliquity=None, body_type=None):
        # Enter data in SI units.
        if rotational_velocity == None:
            rotational_velocity = 0
        if obliquity == None:
            obliquity = 0

        self.name = name
        self.body_type = body_type

        self.mass = mass
        self.radius = radius
        
        self.pos = Vector(0, 0)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)

        self.angular_velocity = rotational_velocity * 360 / (2 * PI * radius)     # sidereal (in deg)
        self.obliquity = obliquity

        self.angle = 0


    def __call__(self, pos=None, vel=None, acc=None, angle=None, angular_velocity=None):
        # Sets body conditions. All vectors default to the 0 vector. Enter data in SI units.
        if pos != None:
            self.pos = pos
        if vel != None:
            self.vel = vel
        if acc != None:
            self.acc = acc
        if angle != None:
            self.angle = angle
        if angular_velocity != None:
            self.angular_velocity = angular_velocity
        return self


    def __copy__(self):
        return Body(self.name, self.mass, self.radius, obliquity=self.obliquity, body_type=self.body_type)(self.pos, self.vel, self.acc, self.angle, self.angular_velocity)


    def updateRotation(self, deltatime):
        # Updates the angle based on the angular velocity over a given deltatime.
        self.angle = (self.angle + self.angular_velocity * deltatime) % 360


    def updateMotion(self, deltatime):
        # Updates the position and velocity vectors based on the acceleration vector over a given deltatime. Based on the standard equations of motion.
        self.vel += self.acc * deltatime
        self.pos += self.vel * deltatime


    def updateKinematicMotion(self, deltatime):
        # Updates the position and velocity vectors based on the acceleration vector over a given deltatime. Based on the kinematic equations.
        pvel = self.vel
        self.vel += self.acc * deltatime
        self.pos += 0.5 * (self.vel + pvel) * deltatime


    def updateForceAcceleration(self, forces):
        # Updates the acceleration based on the sum of the forces. Based on Newton's second law.
        sumforces = Vector(0, 0)
        for f in forces:
            sumforces += f
        self.acc += sumforces / self.mass


    def resetAcceleration(self):
        self.acc = Vector(0, 0)



class NBody:
    """A class that contains a list of astronomical body classes and methods that deal with their interaction."""
   
    def __init__(self):
        self.bodies = []
        self.N = 0


    def __getitem__(self, key):
        return self.bodies[key]


    def __copy__(self):
        newNBody = NBody()
        for body in self.bodies:
            newNBody.addBody(body.__copy__())
        return newNBody


    def addBody(self, body):
        self.bodies.append(body)
        self.N += 1


    def removeBody(self, body):
        self.bodies.remove(body)
        self.N -= 1


    def searchBody(self, i=None, name=None):
        # Returns a body in the sim with an inputted index or name.
        if (i == None):
            i = self.searchIndex(name)
            if (i == None):
                return None
        return self[int(i)]


    def searchIndex(self, name):
        # Returns the first index with name "name".
        for i, body in enumerate(self.bodies):
            if body.name == name:
                return i


    def update(self, deltatime):        # delatime is the simulated time
        # Reset bodies' acceleration.
        for body in self.bodies:
            body.resetAcceleration()

        # Update gravitational forces and bodies' acceleration.
        for i in range(self.N - 1):
            forces = []

            for j in range(i + 1, self.N):
                force = self.forceBetween(i, j)

                forces.append(force)
                self[j].updateForceAcceleration([-force])

            self[i].updateForceAcceleration(forces)
        
        # Update bodies' motion vectors (velocity and position).
        for body in self.bodies:
            body.updateMotion(deltatime)
            body.updateRotation(deltatime)


    def forceBetween(self, i, j):
        # Calculation of the gravitational force vector of i as affected by j. Based on Newton's universal law of gravitation. 
        return (self[j].pos - self[i].pos) * (G * self[j].mass  * self[i].mass / (abs(self[j].pos - self[i].pos) ** 3))



def prefabBody(name):
    data = dp.getData(name)
    return Body(name, data['mass'], data['radius'], data['rotational_velocity'], data['obliquity'], data['type'])     ## GET DATA

    