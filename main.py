"""
Main file for the program.
"""

import demos

def main():
    sim = demos.earth_and_moon_sim()        # options are "earth_and_moon_sim", "solar_system_sim", "trappist_1_sim"
    sim.main()
    sys.exit()


if __name__ == "__main__":
    main()
