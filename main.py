import pygame
from pygame.locals import *

import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image

import math
import numpy as np

FPS = 60

MOVEMENT_SPEED = 1

# Sun and planets radius
radius_earth = 0.01276
radius_sun = 109 * radius_earth
radius_mercury = 0.3825 * radius_earth
radius_venus = 0.9489 * radius_earth
radius_mars = 0.5335 * radius_earth
radius_jupiter = 11.2092 * radius_earth
radius_saturn = 9.4494 * radius_earth
radius_uranus = 4.0074 * radius_earth
radius_neptun = 3.8827 * radius_earth

# Planets distance from sun
distance_earth = 149
distance_mercury = 0.3871 * distance_earth
distance_venus = 0.7233 * distance_earth
distance_mars = 1.5237 * distance_earth
distance_jupiter = 5.2034 * distance_earth
distance_saturn = 9.5371 * distance_earth
distance_uranus = 19.1913 * distance_earth
distance_neptun = 30.069 * distance_earth

# Planets rotation speed over sun
rotation_main_earth = 1
rotation_main_mercury = rotation_main_earth / 0.2408
rotation_main_venus = rotation_main_earth / 0.6152
rotation_main_mars = rotation_main_earth / 1.8808
rotation_main_jupiter = rotation_main_earth / 11.8637
rotation_main_saturn = rotation_main_earth / 29.4484
rotation_main_uranus = rotation_main_earth / 84.0711
rotation_main_neptun = rotation_main_earth / 164.8799

rotation_self_earth = rotation_main_earth * 365
rotation_self_sun = rotation_self_earth / 25.375
rotation_self_mercury = rotation_self_earth / 58.625
rotation_self_venus = rotation_self_earth / 243
rotation_self_mars = rotation_self_earth / 1.0208
rotation_self_jupiter = rotation_self_earth / 0.4167
rotation_self_saturn = rotation_self_earth / 0.4375
rotation_self_uranus = rotation_self_earth / 0.7083
rotation_self_neptun = rotation_self_earth / 0.6667

angle_mercury = 0.0
angle_venus = 0.0
angle_earth = 0.0
angle_mars = 0.0
angle_jupiter = 0.0
angle_saturn = 0.0
angle_uranus = 0.0
angle_neptun = 0.0

angle_self_sun = 0.0
angle_self_mercury = 0.0
angle_self_venus = 0.0
angle_self_earth = 0.0
angle_self_mars = 0.0
angle_self_jupiter = 0.0
angle_self_saturn = 0.0
angle_self_uranus = 0.0
angle_self_neptun = 0.0

pygame.init()
glutInit()
display = (900, 800)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glShadeModel(GL_SMOOTH)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])

sphere = gluNewQuadric()
quadratic = gluNewQuadric()

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0] / display[1]), 0.01, 50000.0)

glMatrixMode(GL_MODELVIEW)
# Init camera start position
gluLookAt(0, -100, 0, 0, 0, 0, 0, 0, 1)
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()

# init mouse movement and center mouse on screen
displayCenter = [screen.get_size()[i] // 2 for i in range(2)]
mouseMove = [0, 0]
pygame.mouse.set_pos(displayCenter)

up_down_angle = 0.0
paused = False
run = True

BACKGROUND = pygame.image.load("stars.bmp")


def loadTexture(file):
    img = Image.open(file)
    ix = img.size[0]
    iy = img.size[1]
    image = img.tobytes("raw", "RGBX", 0, -1)
    # Create Texture
    textID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textID)  # 2d texture (x and y size)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    return textID


dict_of_textures = {"sun": loadTexture("sun.tga"), "mercury": loadTexture("mercurymap.bmp"),
                    "venus": loadTexture("venusmap.bmp"), "earth": loadTexture("earthmap.bmp"),
                    "mars": loadTexture("marsmap.bmp"), "jupiter": loadTexture("jupitermap.bmp"),
                    "saturn": loadTexture("saturnmap.bmp"), "uranus": loadTexture("uranusmap.bmp"),
                    "neptune": loadTexture("neptunemap.bmp")}


def DrawSun(rot):
    glColor3f(1.0, 1.0, 1.0)
    glBindTexture(GL_TEXTURE_2D, dict_of_textures["sun"])
    glEnable(GL_TEXTURE_2D)

    Q = gluNewQuadric()
    gluQuadricNormals(Q, GL_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glRotatef(rot, 0.0, 0.0, 1.0)
    gluSphere(Q, radius_sun, 32, 16)

    glColor4f(1.0, 1.0, 1.0, 0.4)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)

    gluSphere(Q, radius_sun, 32, 16)

    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)
    glDisable(GL_BLEND)
    gluDeleteQuadric(Q)


def DrawMercury(rot):
    glColor3f(1.0, 1.0, 1.0)
    glBindTexture(GL_TEXTURE_2D, dict_of_textures["mercury"])

    Q = gluNewQuadric()
    gluQuadricNormals(Q, GL_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    glPushMatrix()
    glTranslatef(distance_mercury, 0.0, 0.0)  # Center The Cylinder
    glRotatef(rot, 0.0, 0.0, 1.0)
    gluSphere(Q, radius_mercury, 32, 16)
    glPopMatrix()

    gluDeleteQuadric(Q)


def DrawVenus(rot):
    glColor3f(1.0, 1.0, 1.0)
    glBindTexture(GL_TEXTURE_2D, dict_of_textures["venus"])

    Q = gluNewQuadric()
    gluQuadricNormals(Q, GL_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    glPushMatrix()
    glTranslatef(distance_venus, 0.0, 0.0)  # Center The Cylinder
    glRotatef(rot, 0.0, 0.0, 1.0)
    gluSphere(Q, radius_venus, 32, 16)
    glPopMatrix()

    gluDeleteQuadric(Q)


# def DrawMoon(rot):
#     glColor3f(1.0, 1.0, 1.0)
#     glBindTexture(GL_TEXTURE_2D, dict_of_textures["earth"])
#
#     Q = gluNewQuadric()
#     glPushMatrix()
#     glTranslatef(0.0, 0.0, 1.0) # Create distance between earth and moon
#     glRotatef(rot, 1.0, 0.0, 0.0) # Rotate moon itself
#     gluSphere(Q, 0.05, 32, 16)
#     gluDeleteQuadric(Q)
#     glPopMatrix()


def DrawEarth(rot):
    glColor3f(1.0, 1.0, 1.0)
    glBindTexture(GL_TEXTURE_2D, dict_of_textures["earth"])

    Q = gluNewQuadric()
    gluQuadricNormals(Q, GL_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    glPushMatrix()
    glTranslatef(distance_earth, 0.0, 0.0)  # Center The Cylinder
    glRotatef(rot, 0.0, 0.0, 1.0) # Rotate earth itself
    gluSphere(Q, radius_earth, 32, 16)
    gluDeleteQuadric(Q)

    # DrawMoon(rot)
    #
    # # Draw moon orbit
    # glPushMatrix()
    # glRotatef(90, 0, 1, 0)
    # glColor3f(1.0, 1.0, 1.0)
    # glutSolidTorus(0.005, 1.0, 5, 90)
    # glPopMatrix()

    glPopMatrix()


def DrawMars(rot):
    glColor3f(1.0, 1.0, 1.0)
    glBindTexture(GL_TEXTURE_2D, dict_of_textures["mars"])

    Q = gluNewQuadric()
    gluQuadricNormals(Q, GL_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    glPushMatrix()
    glTranslatef(distance_mars, 0.0, 0.0)  # Center The Cylinder
    glRotatef(rot, 0.0, 0.0, 1.0)
    gluSphere(Q, radius_mars, 32, 16)
    gluDeleteQuadric(Q)
    glPopMatrix()


def DrawJupiter(rot):
    glColor3f(1.0, 1.0, 1.0)
    glBindTexture(GL_TEXTURE_2D, dict_of_textures["jupiter"])

    Q = gluNewQuadric()
    gluQuadricNormals(Q, GL_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    glPushMatrix()
    glTranslatef(distance_jupiter, 0.0, 0.0)  # Center The Cylinder
    glRotatef(rot, 0.0, 0.0, 1.0)
    gluSphere(Q, radius_jupiter, 32, 16)
    glPopMatrix()

    gluDeleteQuadric(Q)


def DrawSaturn(rot):
    glColor3f(1.0, 1.0, 1.0)
    glBindTexture(GL_TEXTURE_2D, dict_of_textures["saturn"])

    Q = gluNewQuadric()
    gluQuadricNormals(Q, GL_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    glPushMatrix()
    glTranslatef(distance_saturn, 0.0, 0.0)
    glRotatef(rot, 0.0, 0.0, 1.0)
    glPushMatrix()
    glScalef(1.1, 1, 1)  # Center The Cylinder
    glutWireTorus(0.10, 0.67, 100, 50)
    glPopMatrix()
    gluSphere(Q, radius_saturn, 32, 16)
    glPopMatrix()
    gluDeleteQuadric(Q)


def DrawUranus(rot):
    glColor3f(1.0, 1.0, 1.0)
    glBindTexture(GL_TEXTURE_2D, dict_of_textures["uranus"])

    Q = gluNewQuadric()
    gluQuadricNormals(Q, GL_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    glPushMatrix()
    glTranslatef(distance_uranus, 0.0, 0.0)  # Center The Cylinder
    glRotatef(rot, 0.0, 0.0, 1.0)
    gluSphere(Q, radius_uranus, 32, 16)
    glPopMatrix()
    gluDeleteQuadric(Q)


def DrawNeptune(rot):
    glColor3f(1.0, 1.0, 1.0)
    glBindTexture(GL_TEXTURE_2D, dict_of_textures["neptune"])

    Q = gluNewQuadric()
    gluQuadricNormals(Q, GL_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    glPushMatrix()
    glTranslatef(distance_neptun, 0.0, 0.0)  # Center The Cylinder
    glRotatef(rot, 0.0, 0.0, 1.0)
    gluSphere(Q, radius_neptun, 32, 16)
    glPopMatrix()
    gluDeleteQuadric(Q)


while run:
    # screen.blit(BACKGROUND, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                run = False
            if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                paused = not paused
                pygame.mouse.set_pos(displayCenter)
        if not paused:
            if event.type == pygame.MOUSEMOTION:
                mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]
            pygame.mouse.set_pos(displayCenter)

    if not paused:
        # get keys
        keypress = pygame.key.get_pressed()
        # mouseMove = pygame.mouse.get_rel()

        # init model view matrix
        glLoadIdentity()

        # apply the look up and down
        up_down_angle += mouseMove[1] * 0.1
        glRotatef(up_down_angle, 1.0, 0.0, 0.0)

        # init the view matrix
        glPushMatrix()
        glLoadIdentity()

        # apply the movment
        if keypress[pygame.K_w]:
            glTranslatef(0, 0, MOVEMENT_SPEED)
        if keypress[pygame.K_s]:
            glTranslatef(0, 0, -MOVEMENT_SPEED)
        if keypress[pygame.K_d]:
            glTranslatef(-MOVEMENT_SPEED, 0, 0)
        if keypress[pygame.K_a]:
            glTranslatef(MOVEMENT_SPEED, 0, 0)
        if keypress[pygame.K_z]:
            glTranslatef(0, -MOVEMENT_SPEED, 0)
        if keypress[pygame.K_x]:
            glTranslatef(0, MOVEMENT_SPEED, 0)

        # apply speed changes
        if keypress[pygame.K_1]:
            MOVEMENT_SPEED -= 0.01
            print("Movement speed: ", MOVEMENT_SPEED)
        if keypress[pygame.K_2]:
            MOVEMENT_SPEED += 0.01
            print("Movement speed: ", MOVEMENT_SPEED)
        if keypress[pygame.K_3]:
            rotation_main_earth -= 0.001
            rotation_main_mercury = rotation_main_earth / 0.2408
            rotation_main_venus = rotation_main_earth / 0.6152
            rotation_main_mars = rotation_main_earth / 1.8808
            rotation_main_jupiter = rotation_main_earth / 11.8637
            rotation_main_saturn = rotation_main_earth / 29.4484
            rotation_main_uranus = rotation_main_earth / 84.0711
            rotation_main_neptun = rotation_main_earth / 164.8799

            rotation_self_earth = rotation_main_earth * 365
            rotation_self_sun = rotation_self_earth / 25.375
            rotation_self_mercury = rotation_self_earth / 58.625
            rotation_self_venus = rotation_self_earth / 243
            rotation_self_mars = rotation_self_earth / 1.0208
            rotation_self_jupiter = rotation_self_earth / 0.4167
            rotation_self_saturn = rotation_self_earth / 0.4375
            rotation_self_uranus = rotation_self_earth / 0.7083
            rotation_self_neptun = rotation_self_earth / 0.6667
            print("Base rotation ratio: ", rotation_main_earth)
        if keypress[pygame.K_4]:
            rotation_main_earth += 0.001
            rotation_main_mercury = rotation_main_earth / 0.2408
            rotation_main_venus = rotation_main_earth / 0.6152
            rotation_main_mars = rotation_main_earth / 1.8808
            rotation_main_jupiter = rotation_main_earth / 11.8637
            rotation_main_saturn = rotation_main_earth / 29.4484
            rotation_main_uranus = rotation_main_earth / 84.0711
            rotation_main_neptun = rotation_main_earth / 164.8799

            rotation_self_earth = rotation_main_earth * 365
            rotation_self_sun = rotation_self_earth / 25.375
            rotation_self_mercury = rotation_self_earth / 58.625
            rotation_self_venus = rotation_self_earth / 243
            rotation_self_mars = rotation_self_earth / 1.0208
            rotation_self_jupiter = rotation_self_earth / 0.4167
            rotation_self_saturn = rotation_self_earth / 0.4375
            rotation_self_uranus = rotation_self_earth / 0.7083
            rotation_self_neptun = rotation_self_earth / 0.6667
            print("Base rotation ratio: ", rotation_main_earth)
        if keypress[pygame.K_5]:
            # Planets distance from sun
            distance_earth -= 1
            distance_mercury = 0.3871 * distance_earth
            distance_venus = 0.7233 * distance_earth
            distance_mars = 1.5237 * distance_earth
            distance_jupiter = 5.2034 * distance_earth
            distance_saturn = 9.5371 * distance_earth
            distance_uranus = 19.1913 * distance_earth
            distance_neptun = 30.069 * distance_earth
            print("Distance (earth to sun) [mln km]: ", distance_earth)
        if keypress[pygame.K_6]:
            # Planets distance from sun
            distance_earth += 1
            distance_mercury = 0.3871 * distance_earth
            distance_venus = 0.7233 * distance_earth
            distance_mars = 1.5237 * distance_earth
            distance_jupiter = 5.2034 * distance_earth
            distance_saturn = 9.5371 * distance_earth
            distance_uranus = 19.1913 * distance_earth
            distance_neptun = 30.069 * distance_earth
            print("Distance (earth to sun) [mln km]: ", distance_earth)
        if keypress[pygame.K_7]:
            # Sun and planets radius
            radius_earth -= 0.001
            radius_sun = 109 * radius_earth
            radius_mercury = 0.3825 * radius_earth
            radius_venus = 0.9489 * radius_earth
            radius_mars = 0.5335 * radius_earth
            radius_jupiter = 11.2092 * radius_earth
            radius_saturn = 9.4494 * radius_earth
            radius_uranus = 4.0074 * radius_earth
            radius_neptun = 3.8827 * radius_earth
            print("Earth radius [km]: ", radius_earth)
        if keypress[pygame.K_8]:
            # Sun and planets radius
            radius_earth += 0.001
            radius_sun = 109 * radius_earth
            radius_mercury = 0.3825 * radius_earth
            radius_venus = 0.9489 * radius_earth
            radius_mars = 0.5335 * radius_earth
            radius_jupiter = 11.2092 * radius_earth
            radius_saturn = 9.4494 * radius_earth
            radius_uranus = 4.0074 * radius_earth
            radius_neptun = 3.8827 * radius_earth
            print("Earth radius [km]: ", radius_earth)
        # apply the left and right rotation
        glRotatef(mouseMove[0] * 0.1, 0.0, 1.0, 0.0)

        # multiply the current matrix by the get the new view matrix and store the final vie matrix
        glMultMatrixf(viewMatrix)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # apply view matrix
        glPopMatrix()
        glMultMatrixf(viewMatrix)

        glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw Mercury
        glPushMatrix()
        glRotatef(angle_mercury, 0.0, 0.0, 1.0)  # Rotate The Cube On It's X Axis
        DrawMercury(angle_self_mercury)
        glPopMatrix()

        glPushMatrix()
        # glRotatef(0, 0, 0, 1)
        glColor3f(1.0, 1.0, 1.0)
        glutSolidTorus(0.0005, distance_mercury, 5, 90)
        glPopMatrix()

        # Draw Venus
        glPushMatrix()
        glRotatef(angle_venus, 0.0, 0.0, 1.0)  # Rotate The Cube On It's X Axis
        DrawVenus(-angle_self_venus)
        glPopMatrix()

        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        glutSolidTorus(0.0005, distance_venus, 5, 90)
        glPopMatrix()

        # Draw Earth
        glPushMatrix()
        glRotatef(angle_earth, 0.0, 0.0, 1.0)  # Rotate The Cube On It's X Axis
        DrawEarth(angle_self_earth)
        glPopMatrix()

        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        glutSolidTorus(0.0005, distance_earth, 5, 90)
        glPopMatrix()

        # Draw Mars
        glPushMatrix()
        glRotatef(angle_mars, 0.0, 0.0, 1.0)  # Rotate The Cube On It's X Axis
        DrawMars(angle_self_mars)
        glPopMatrix()

        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        glutSolidTorus(0.0005, distance_mars, 5, 90)
        glPopMatrix()

        # Draw Jupiter
        glPushMatrix()
        glRotatef(angle_jupiter, 0.0, 0.0, 1.0)  # Rotate The Cube On It's X Axis
        DrawJupiter(angle_self_jupiter)
        glPopMatrix()

        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        glutSolidTorus(0.0005, distance_jupiter, 5, 90)
        glPopMatrix()

        # Draw Saturn
        glPushMatrix()
        glRotatef(angle_saturn, 0.0, 0.0, 1.0)  # Rotate The Cube On It's X Axis
        DrawSaturn(angle_self_saturn)
        glPopMatrix()

        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        glutSolidTorus(0.0005, distance_saturn, 5, 90)
        glPopMatrix()

        # Draw Uranus
        glPushMatrix()
        glRotatef(angle_uranus, 0.0, 0.0, 1.0)  # Rotate The Cube On It's X Axis
        DrawUranus(angle_self_uranus)
        glPopMatrix()

        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        glutSolidTorus(0.0005, distance_uranus, 5, 90)
        glPopMatrix()

        # Draw Neptune
        glPushMatrix()
        glRotatef(angle_neptun, 0.0, 0.0, 1.0)  # Rotate The Cube On It's X Axis
        DrawNeptune(angle_self_neptun)
        glPopMatrix()

        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        glutSolidTorus(0.0005, distance_neptun, 5, 90)
        glPopMatrix()

        # Draw Sun
        glPushMatrix()
        DrawSun(angle_self_sun)
        glPopMatrix()

        # Start Drawing The Cube
        angle_mercury = (angle_mercury + rotation_main_mercury) % 360  # rotation
        angle_venus = (angle_venus + rotation_main_venus) % 360
        angle_earth = (angle_earth + rotation_main_earth) % 360
        angle_mars = (angle_mars + rotation_main_mars) % 360
        angle_jupiter = (angle_jupiter + rotation_main_jupiter) % 360
        angle_saturn = (angle_saturn + rotation_main_saturn) % 360
        angle_uranus = (angle_uranus + rotation_main_uranus) % 360
        angle_neptun = (angle_neptun + rotation_main_neptun) % 360

        # Start Drawing The Cube
        angle_self_sun = (angle_self_sun + rotation_self_sun) % 360
        angle_self_mercury = (angle_self_mercury + rotation_self_mercury) % 360  # rotation
        angle_self_venus = (angle_self_venus + rotation_self_venus) % 360
        angle_self_earth = (angle_self_earth + rotation_self_earth) % 360
        angle_self_mars = (angle_self_mars + rotation_self_mars) % 360
        angle_self_jupiter = (angle_self_jupiter + rotation_self_jupiter) % 360
        angle_self_saturn = (angle_self_saturn + rotation_self_saturn) % 360
        angle_self_uranus = (angle_self_uranus + rotation_self_uranus) % 360
        angle_self_neptun = (angle_self_neptun + rotation_self_neptun) % 360

        pygame.display.flip()
        pygame.time.wait(int(1000 / FPS))

pygame.quit()
