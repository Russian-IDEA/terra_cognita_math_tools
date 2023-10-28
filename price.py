from sat import Point
from mathutils import distFromTo
import math

def getPrice(geoPoints, costMultiplier):
    points = []
    for geoPoint in geoPoints:
        points.append(Point(geoPoint[0], geoPoints[1]))

    # делим четырехугольник на два треугольника
    triangles = [[points[0], points[1], points[2]], [points[0], points[2], points[3]]]

    s = 0
    # считаем длины сторон треугольников, считаем площади по герону
    for triangle in triangles:
        a = distFromTo(triangle[0].x, triangle[0].y, triangle[0].z,
                          triangle[1].x, triangle[1].y, triangle[1].z)
        b = distFromTo(triangle[1].x, triangle[1].y, triangle[1].z,
                          triangle[2].x, triangle[2].y, triangle[2].z)
        c = distFromTo(triangle[2].x, triangle[2].y, triangle[2].z,
                          triangle[0].x, triangle[0].y, triangle[0].z)

        p = a + b + c

        s += math.sqrt(p * (p - a) * (p - b) * (p - c))
    return s * costMultiplier