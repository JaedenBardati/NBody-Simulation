"""
Main simulation class.
It deals with the graphics and timing of the simulation.
"""

import os
import sys
import time
import math
import threading

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image

from . import nbody as nb
from . import data_parse as dp
from .vector import Vector


class AstrophysicsSimulation():
    """Main astrophysics simulation class"""
    def __init__(self, size, sim_speed=None, title=None):
        # Defaults
        if sim_speed == None:
            sim_speed = 1
        if title == None:
            self.title = b"Astrophysics Simulation"
        
        # Simulation variables
        self.title = title
        self.width, self.height = size

        self.unitscale = 400000000      # unit of scale (in m) every 1 unit
        self.unittime = sim_speed       # unit of sim time (in sec) every 1 sec (actual, dynamically changes)
        self.lastTime = 0
        self.dt = 0

        self.NBody = nb.NBody()
        self.displaylists = []

        self.znear = 0.01
        self.zfar = 100000.0

        self.done = False               # Flag for program to end
        self.donesetup = False          # Flag for physics to start
        self.static = True             # Flag for physics to pause

        self.bodyscale = 1.0            # All bodies scale
        self.focusscale = 1.0           # To make stars smaller --TEMP--?

        self.centeredBodyIndex = 0        # default center of view

        self.camerapos = Vector(0.0, 0.0, 0.0)
        self.cameralook = Vector(0.0, 0.0, 0.0)

        # Preprocessor
        # self.preiterations = 3
        # self.pretime = self.unittime * 3
        # self.predictedLine = [(200,300,0),(400, 100, 0)]


    def setup(self):
        global window

        # OpenGL/glut initialization
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

        # Window creation
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(0, 0)
        window = glutCreateWindow(self.title)

        # Glut function assignment
        glutDisplayFunc(self.draw)
        glutIdleFunc(self.draw)
        glutKeyboardFunc(self.keyboard_callback)
        glutMouseFunc(self.mouse_callback)
        glutReshapeFunc(self.reshape_callback)
        
        # Lighting +
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)
        
        glShadeModel(GL_SMOOTH)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)

        glEnable(GL_LIGHTING)
        lightZeroPosition = [10., 4., 10., 1.]
        lightZeroColor = [0.8, 1.0, 0.8, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
        glEnable(GL_LIGHT0)

        # Load skybox
        #self.load_skybox()

        # Load body textures
        for body in self.NBody:
            self.addBodyTexture(body.name.lower() + '.jpg')        # Texture map convention

        self.reshape_callback(self.width, self.height)          # Initialize perspective


    def addBody(self, body):
        self.NBody.addBody(body)


    def addPrefabBody(self, name):
        self.addBody(nb.prefabBody(name))


    def addPrefabBodies(self, names):
        for name in names:
            self.addPrefabBody(name)


    def addBodyTexture(self, texture_filename, i=None):        
        if i == None:
            self.displaylists.append(glGenLists(1))
            glNewList(self.displaylists[-1], GL_COMPILE)
        else:
            self.displaylists[i] = glGenLists(1)
            glNewList(self.displaylists[i], GL_COMPILE)

        tex = load_texture(os.path.join('resources', 'maps', texture_filename))
        
        qobj = gluNewQuadric()
        gluQuadricTexture(qobj, GL_TRUE)
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex)
        glBegin(GL_TRIANGLES)
        gluSphere(qobj, 1, 50, 50)
        gluDeleteQuadric(qobj)
        glDisable(GL_TEXTURE_2D)
        glEndList()


    # def load_skybox(self):
    #     self.skybox = glGenLists(1)
    #     glNewList(self.skybox, GL_COMPILE)
    #     tex = load_texture(os.path.join('resources', 'maps', 'celestialsphere4.jpg'))
        
    #     qobj = gluNewQuadric()
    #     gluQuadricTexture(qobj, GL_TRUE)
        
    #     glEnable(GL_TEXTURE_2D)
    #     glBindTexture(GL_TEXTURE_2D, tex)
    #     glBegin(GL_TRIANGLES)
    #     gluSphere(qobj, self.zfar - 0.1, 1000, 1000)        ## Yes, it isn't a box.
    #     gluDeleteQuadric(qobj)
    #     glDisable(GL_TEXTURE_2D)
    #     glEndList()


    # def draw_skybox(self):
    #     glScale(-1,-1,-1)
    #     glCallList(self.skybox)
    #     glScale(-1,-1,-1)


    def draw(self):
        # Reset The View
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Draw Sky Box
        # glRotatef(self.x, 1.0, 1.0, 1.0)
        # self.draw_skybox()
        # glRotatef(-self.x, 0.0, 0.0, 1.0)
        
        # Set title
        time, timeunit = getTimeUnit(self.dt)
        glutSetWindowTitle(self.title + bytes(": dt = " + str(time), 'utf-8') + timeunit)
        

        # Make copy of Nbody class
        nBody = self.NBody.__copy__()

        #CAMERA
        if nBody.N > 0:
            glTranslatef(-nBody[self.centeredBodyIndex].pos.x/self.unitscale, -nBody[self.centeredBodyIndex].pos.y/self.unitscale, -(nBody[self.centeredBodyIndex].pos.z + self.zoomout)/self.unitscale)
            glPushMatrix()
            glRotatef(0, 1.0, 0.0, 0.0)


        # Draw all display lists
        for i, dl in enumerate(self.displaylists):
            # Get position
            x, y, z = nBody[i].pos.x/self.unitscale, nBody[i].pos.y/self.unitscale, nBody[i].pos.z/self.unitscale
            
            # Get scaling
            scale = self.bodyscale * nBody[i].radius / self.unitscale
            if nBody[i].body_type == 'star':     ## --TEMP--
                scale *= self.focusscale

            glPushMatrix()
           
            # Update position and scale
            glTranslatef(x, y, z)
            glScalef(scale, scale, scale)

            # Update rotation
            glRotatef(nBody[i].obliquity,-0.25,-1.0,0.0)
            glRotatef(nBody[i].angle, 0.0, 0.0, 1.0)
            
            # Display body
            glCallList(dl)
            
            glPopMatrix()

        # Clean up
        glPopMatrix()
        glFlush()

        glutSwapBuffers()


    def physics_thread(self):
        self.lastTime = time.clock()         # for physics deltatime calulation (in seconds)
        while not self.done:
            t = time.clock()
            if not self.static:
                self.dt = (t - self.lastTime) * self.unittime
                self.NBody.update(self.dt)
            self.lastTime = t
        glutLeaveMainLoop()


    # def prephysics_thread(self):
    #     while not self.done:
    #         self.predictedLine = []
    #         body = self.NBody.__copy__()
    #         for i in range(self.preiterations):
    #             body.update(self.pretime)
    #             self.predictedLine.append((body.pos.x, body.pos.y, body.pos.z))
            

    def main(self):
        self.setup()                                            # Initialize openGL
        
        phys = threading.Thread(target=self.physics_thread)     # Create physics thread
        #prephys = threading.Thread(target=self.prephysics_thread)
        
        phys.start()            # Start physics thread
        #prephys.start()
        
        glutMainLoop()          # Start graphics loop on main thread

        #prephys.join()
        phys.join()             # Clean up physics thread when done


    def mouse_callback(self, *args):
        zoomspeed = 1.2

        if args[0] == 4 and args[1] == 0:
            self.zoomout *= zoomspeed
        elif (args[0] == 3 and args[1] == 0) and self.zoomout > (2 * self.znear + self.NBody[self.centeredBodyIndex].radius/self.unitscale):
            self.zoomout /= zoomspeed


    def keyboard_callback(self, *args):
        speedspeed, scalespeed = 1.2, 1.2
        
        if args[0] == b'\x1b':
            self.done = True
        
        elif args[0] == b' ':
            self.static = not self.static
        
        elif args[0] == b'+':
            self.centeredBodyIndex += 1
            if (self.centeredBodyIndex >= self.NBody.N):
                self.centeredBodyIndex = 0
        elif args[0] == b'-':
            self.centeredBodyIndex -= 1
            if (self.centeredBodyIndex < 0):
                self.centeredBodyIndex = self.NBody.N - 1
        
        elif args[0] == b't':
            self.unittime *= speedspeed
        elif args[0] == b'g':
            self.unittime /= speedspeed

        elif args[0] == b'u':
            self.bodyscale *= scalespeed
        elif args[0] == b'j':
            self.bodyscale /= scalespeed

        elif args[0] == b'o':
            self.focusscale *= scalespeed
        elif args[0] == b'l':
            self.focusscale /= scalespeed


    def reshape_callback(self, width, height):
        if height == 0:
            height = 1
        glViewport(0,0,width,height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, self.zfar, self.zfar)
        gluPerspective(45.0, float(width) / float(height), self.znear, self.zfar)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()



def load_texture(filename):
    img = Image.open(filename).rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
    img_data = img.tobytes()
    textID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textID)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return textID


def getTimeUnit(time):
    # Returns (time, timeunit)
    if (time < 3600):
        return (time, b' s')
    elif (time < 86400):
        return (time/3600, b' h')
    elif (time < 604800):
        return (time/86400, b' d')
    elif (time < 31556736):
        return (time/604800, b' w')
    elif (time < 3155673600):
        return (time/31556736, b' y')
    else:
        return (time/3155673600, b' c')

