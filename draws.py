import numpy as np
import matplotlib.pyplot as plt
from consts import *

ax = plt.axes(projection='3d')
def drawSphere(x0, y0, z0, radius, color):
    u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    x = x0 + np.cos(u) * np.sin(v) * radius
    y = y0 + np.sin(u) * np.sin(v) * radius
    z = z0 + np.cos(v) * radius
    ax.plot_surface(x, y, z, color=color, alpha=0.3)

def showScene():
    ax.set_aspect('equal')
    ax.set_adjustable('box')
    plt.show()

def drawEarth():
    drawSphere(0, 0, 0, R, 'b')

def drawBadZone(badZone):
    drawSphere(badZone.x, badZone.y, badZone.z, badZone.radius, 'r')

def drawBadZones(badZones):
    for badZone in badZones:
        drawBadZone(badZone)

def drawPoint(point):
    ax.scatter(point.x, point.y, point.z)

def drawPoints(points):
    for point in points:
        drawPoint(point)

def drawPath(x, y, z):
    ax.plot3D(x, y, z)