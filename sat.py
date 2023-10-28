import math

R = 6370
g = 9.81
GM4pi2 = 1.009e13
class Satellite:
    def __init__(self, id, s, t, angle):
        self.id = id
        self.TLE = {
            's': s,
            't': t
        }
        self.angle = math.radians(angle)
        self.height = 1 / float(self.TLE['t'].split(" ")[-1]) * 24 * 60 * 60
        self.height = math.pow(self.height ** 2 * GM4pi2, 1/3) / 1000 - 6371
        self.maxDist = self.height / math.cos(self.angle / 2)

class Point:
    x = 0
    y = 0
    z = 0
    def __init__(self, lati, long):
        lati = math.radians(lati)
        long = math.radians(long)
        self.x = R * math.cos(lati) * math.cos(long)
        self.y = R * math.cos(lati) * math.sin(long)
        self.z = R * math.sin(lati)

    def set_coord(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class SatPoint:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class BadZone:
    def __init__(self, lati, long, radius):
        lati = math.radians(lati)
        long = math.radians(long)
        self.x = R * math.cos(lati) * math.cos(long)
        self.y = R * math.cos(lati) * math.sin(long)
        self.z = R * math.sin(lati)
        self.radius = radius

    def isInside(self, point):
        return (self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) <= self.radius ** 2