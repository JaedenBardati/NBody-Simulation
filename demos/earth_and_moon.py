"""
Main file for the program.
"""

from src import simulation
from src import data_parse as dp
from src.vector import Vector


def earth_and_moon_sim():
    sim = simulation.AstrophysicsSimulation((900,900), sim_speed=36000, title=b"Earth and Moon System")

    sim.centeredBodyIndex = 0      # starts around the earth

    sim.addPrefabBody("Earth")
    sim.addPrefabBody("Moon")

    moon_data = dp.getData("Moon")
    sim.NBody[1](moon_data['semimajor_axis'] * Vector(1, 0, 0), moon_data['orbital_velocity'] * Vector(0,1))
    
    sim.zoomout = moon_data['semimajor_axis'] * 2.5      # z direction

    return sim

