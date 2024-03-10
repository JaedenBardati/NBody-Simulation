# Naive Astronomical Visual Simulation
A simple visual n-body simulation of planetary orbits, created to accompany a presentation for an astrophysics class in fall 2019.

The program simulates the gravitational force interaction between any number of astronomical bodies in space, with a naive particle model. The calculation is done by simply choosing a small value for dt and iterating over many steps to obtain a somewhat accurate idea of the position and velocity of each particle. The forces are very inefficiently calculated at each step by comparing each particle in the simulation to each other, no matter their distance. Various existing [solar system (Solar System Scope)](https://www.solarsystemscope.com/textures/) and [Trappist-1 (NASA)](https://informal.jpl.nasa.gov/museum/content/trappist-1-exoplanet-surfaces-noaa-science-sphere) sphere map textures have been used to render the planets and stars.

This code was written just to be accurate enough to be sufficiently visually accurate, but no more. At the time, I was stubborn to try to make as much of it from scratch as I could, so I avoided many useful packages. It is not even vectorized in an efficient way (such as with NumPy). The only external python libraries that were used were a python port of OpenGL, for rendering; and Pillow, for image loading. I did use the built-in threading module, though it was done for convenience and not for efficiency.

### What is needed ...

* [Python 3.6](https://www.python.org/downloads/release/python-368/)
* An installation of [freeglut](http://freeglut.sourceforge.net/)


#### Python Requirements

> PyOpenGL 3.1.0  
> PyOpenGL_accelerate 3.1.0  
> Pillow 6.2.1

## Running
1. Clone the repo.  

2. Install python dependencies using pip:  
```
pip install -r requirements.txt
```

3. Run the main script:  
```
python main.py
```


#### Changing the system
There are currently 3 demo systems implemented (earth-moon, solar system, and Trappist-1 system). By default, the earth-moon system is loaded. Each system has its own demo file (in the `demos` directory). The `main.py` file can be altered to change the system that is rendered. To do so, change 
```py
sim = demos.earth_and_moon_sim()
```
in the `main` function declaration to either
```py
sim = demos.solar_system_sim()
```
for the solar system, or to
```py
sim = demos.trappist_1_sim()
```
for the Trappist-1 system.

More systems can be implemented by adding the system data to the `resources/astronomical_data.xml` file, adding sphere maps to the `resources/maps` directory, creating a demo python file in `demos`, and adjusting `demos/__init__.py` and `main.py` to properly load the file.


#### Controls

I have included a variety of simple controls to control the program.

* <kbd>Esc</kbd> - Quits the program
* <kbd>Space</kbd> - Starts/stops the system motion
* <kbd>Scroll up</kbd>/<kbd>Scroll down</kbd> - Zooms in/out
* <kbd>+</kbd>/<kbd>-</kbd> - Changes the viewed body in increasing/decreasing order
* <kbd>o</kbd>/<kbd>l</kbd> - Increases/decreases the scale factor of the center object (often the star; defaults to 1)
* <kbd>u</kbd>/<kbd>j</kbd> - Increases/decreases the scale factor of all objects (defaults to 1)
* <kbd>t</kbd>/<kbd>g</kbd> - Increases/decreases the value of dt (view in the title of the program window)

Due to the fact that the size of the orbiting bodies is often very small compared to the central body and the distances between them, the scale usually has to be adjusted by pressing <kbd>u</kbd> and <kbd>l</kbd> until the desired relative scale is reached. The <kbd>Space</kbd> button must be pressed to start the motion.
