"""
Main file for the program.
"""

import math

from src import simulation
from src import data_parse as dp
from src.vector import Vector


def trappist_1_sim():
    sim = simulation.AstrophysicsSimulation((900,900), sim_speed=36000, title=b"TRAPPIST-1 System")

    sim.centeredBodyIndex = 0      # starts around the trappist-1a

    sim.addPrefabBodies(["Trappist-1a","Trappist-1b", "Trappist-1c", "Trappist-1d", "Trappist-1e", "Trappist-1f", "Trappist-1g", "Trappist-1h"])

    for i, body in enumerate(sim.NBody[1:]):
        data = dp.getData(body.name)
        angle = 2 * math.pi * i / (sim.NBody.N - 1)
        body(data['semimajor_axis'] * Vector(math.cos(angle), math.sin(angle), 0), data['orbital_velocity'] * Vector(-math.sin(angle), math.cos(angle)), angle=math.degrees(angle))
    
    sim.zoomout = dp.getData("Trappist-1h")['semimajor_axis'] * 2.5      # z direction

    return sim

