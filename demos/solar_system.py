"""
Main file for the program.
"""

import math

from src import simulation
from src import data_parse as dp
from src.vector import Vector


def solar_system_sim():
    sim = simulation.AstrophysicsSimulation((900,900), sim_speed=36000, title=b"Solar System")

    sim.centeredBodyIndex = 0      # starts around the sun
    system_inclination = dp.getData("Earth")['inclination']      # inclination starts around the earth

    sim.addPrefabBodies(["Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"])

    for body in sim.NBody[1:]:
        data = dp.getData(body.name)
        incline_x = 0 #math.cos(math.pi/2 + data['inclination'] - system_inclination)

        body(data['semimajor_axis'] * Vector(math.sqrt(1 - incline_x**2), 0, incline_x), data['orbital_velocity'] * Vector(0,1))
    
    sim.zoomout = dp.getData("Mars")['semimajor_axis'] * 2.5      # z direction

    return sim

