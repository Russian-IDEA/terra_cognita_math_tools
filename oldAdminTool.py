from sgp4.api import jday, Satrec
import matplotlib.pyplot as plt
import numpy as np
import math
from sat import *
from data import *



ax = plt.axes(projection='3d')

def distFromTo(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

def drawSphere(x0, y0, z0, radius, color):
    u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    x = x0 + np.cos(u) * np.sin(v) * radius
    y = y0 + np.sin(u) * np.sin(v) * radius
    z = z0 + np.cos(v) * radius
    ax.plot_surface(x, y, z, color=color, alpha=0.3)

def checkBadPoints(geoPoints, geoBadZones):
    points = []
    for geoPoint in geoPoints:
        points.append(Point(geoPoint[0], geoPoint[1]))

    badZones = []
    for badZone in geoBadZones:
        badZones.append(BadZone(badZone[0], badZone[1], badZone[2]))

    for point in points:
        for badZone in badZones:
            if (badZone.isInside(point)):
                return -1

    # draw bad zones
    for badZone in badZones:
        drawSphere(badZone.x, badZone.y, badZone.z, badZone.radius, 'r')

    calculate_time(points)

def calculate_time(points):
    # генерируем доп поинты, чтобы отсканить всю область.
    for i in range(4):
        for j in range(i + 1, 4):
            x = (points[i].x + points[j].x) / 2
            y = (points[i].y + points[j].y) / 2
            z = (points[i].z + points[j].z) / 2
            P = Point(0, 0)
            P.set_coord(x, y, z)
            points.append(P)

    # draw points
    for point in points:
        ax.scatter(point.x, point.y, point.z)

    # draw Earth
    drawSphere(0, 0, 0, R, "b")

    # orbits
    # список дистанций от спутников до точек в формате
    # [спутник][точка][дистанция до нее, изначальная точка]
    dists = []
    for id, sat in enumerate(satArr):
        satellite = Satrec.twoline2rv(sat.TLE['s'], sat.TLE['t'])
        x = []
        y = []
        z = []
        # 1 / v = T (суток на оборот), T * 24 * 60 + 1 (минут на оборот)
        time = int(1 / float(sat.TLE['t'].split(" ")[-1]) * 24 * 60) + 1
        # добавляем спутник
        dists.append([])
        # заранее добавляем нужное кол-во точек
        # формат [наименьшее расстояние, координаты на орбите, время]
        for ip, _ in enumerate(points):
            dists[id].append([1e20, 0, 0])
        for i in range(time):
            if (i % 2 == 0):
                jd, fr = jday(2023, 10, int(0 + i / 60 / 24 % 30), int(i / 60 % 24), int(i % 60), 0)
                e, r, v = satellite.sgp4(jd, fr)
                x.append([r[0]])
                y.append([r[1]])
                z.append([r[2]])

                # перебираем точки
                for ip, point in enumerate(points):
                    distToPoint = distFromTo(r[0], r[1], r[2], point.x, point.y, point.z)
                    # если дист < минДист и дист < максДист
                    if (dists[id][ip][0] > distToPoint and sat.maxDist >= distToPoint):
                        dists[id][ip][0] = distToPoint
                        dists[id][ip][1] = SatPoint(r[0], r[1], r[2])
                        dists[id][ip][2] = i
        # рисуем весь путь
        ax.plot3D(x, y, z)

    minTime = []
    for i in range(len(points)):
        minTime.append(1e20)
    for id, sat in enumerate(dists):
        for ip, satData in enumerate(sat):
            dist, point, time = satData
            if point != 0:
                ax.scatter(point.x, point.y, point.z)
                satellite = satArr[id]
                #print(id, satellite.maxDist, dist, time)
                minTime[ip] = min(minTime[ip], time)

    if (max(minTime) == 1e20):
        print("Спутники не могут получить фото.")
    else:
        print("Спутники получат фото через", max(minTime), "минут.")

    ax.set_aspect('equal')
    ax.set_adjustable('box')
    plt.show()

    return minTime

print(checkBadPoints(geoPoints, geoBadZones))