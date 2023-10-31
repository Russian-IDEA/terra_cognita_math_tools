import requests
from sgp4.api import jday, Satrec
import matplotlib.pyplot as plt
import numpy as np
import math
from draws import *
from sat import *
from data import *

def distFromTo(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

def checkBadPoints(geoPoints, geoBadZones):
    points = []
    for geoPoint in geoPoints:
        points.append(Point(geoPoint[0], geoPoint[1]))

    badZones = []
    for badZone in geoBadZones:
        badZones.append(BadZone(badZone[0], badZone[1], badZone[2]))

    drawEarth()
    drawBadZones(badZones)
    for point in points:
        for badZone in badZones:
            if (badZone.isInside(point)):
                drawPoints(points)
                showScene()
                return -1
    return calculate_time(points)

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
    drawPoints(points)

    # orbits
    # список дистанций от спутников до точек в формате
    # [спутник][точка][дистанция до нее, изначальная точка]
    dists = []
    x = []
    y = []
    z = []
    for id, sat in enumerate(satArr):
        satellite = Satrec.twoline2rv(sat.TLE['s'], sat.TLE['t'])
        # 1 / v = T (суток на оборот), T * 24 * 60 + 1 (минут на оборот)
        time = int(1 / float(sat.TLE['t'].split(" ")[-1]) * 24 * 60) + 1
        # добавляем спутник
        dists.append([])
        # заранее добавляем нужное кол-во точек
        # формат [наименьшее расстояние, координаты на орбите, время, id спутника]
        x.append([])
        y.append([])
        z.append([])
        for ip, _ in enumerate(points):
            dists[id].append([1e20, 0, 0, 0])
        for i in range(time):
            if (i % 2 == 0):
                jd, fr = jday(2023, 10, int(0 + i / 60 / 24 % 30), int(i / 60 % 24), int(i % 60), 0)
                e, r, v = satellite.sgp4(jd, fr)
                x[id].append([r[0]])
                y[id].append([r[1]])
                z[id].append([r[2]])

                # перебираем точки
                for ip, point in enumerate(points):
                    distToPoint = distFromTo(r[0], r[1], r[2], point.x, point.y, point.z)
                    # если дист < минДист и дист < максДист
                    if (dists[id][ip][0] > distToPoint and sat.maxDist >= distToPoint):
                        dists[id][ip][0] = distToPoint
                        dists[id][ip][1] = SatPoint(r[0], r[1], r[2])
                        dists[id][ip][2] = i
                        dists[id][ip][3] = id
    minTime = []
    for i in range(len(points)):
        minTime.append([0, 0, 1e20, -1])
    for sat in dists:
        for ip, satData in enumerate(sat):
            dist, point, time, satID = satData
            if point != 0:
                if(time < minTime[ip][2]):
                    minTime[ip] = [dist, point, time, satID]

    print(minTime)
    allMinTime = 0
    for marks in minTime:
        print(marks)
        if(marks[3] == -1):
            continue
        px = x[marks[3]]
        py = y[marks[3]]
        pz = z[marks[3]]
        drawPath(px, py, pz)
        drawPoint(marks[1])
        allMinTime = max(allMinTime, marks[2])
    showScene()
    return allMinTime

print(checkBadPoints(geoPoints, geoBadZones))