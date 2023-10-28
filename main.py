from sgp4.api import jday, Satrec
import matplotlib.pyplot as plt
import numpy as np
import math
from sat import *

satArr = []
satArr.append(Satellite(0,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  0 0.4627 0000000 130.5360 325.0288 5',
                        30))
satArr.append(Satellite(1,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  45 0.4627 0000000 130.5360 325.0288 11.2125391563537',
                        30))
satArr.append(Satellite(2,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  15 150.4627 0000000 100 50.0288 10.2125391563537',
                        30))
satArr.append(Satellite(3,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  30 50.4627 0000000 100 50.0288 10.2125391563537',
                        30))
satArr.append(Satellite(4,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  17 35.4627 0000000 100 50.0288 7.2125391563537',
                        30))
satArr.append(Satellite(5,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  2 230.4627 0000000 100 50.0288 10.2125391563537',
                        30))
satArr.append(Satellite(6,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  19 78.4627 0000000 100 50.0288 8.2125391563537',
                        30))
satArr.append(Satellite(7,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  1 93.4627 0000000 100 50.0288 10.2125391563537',
                        30))
satArr.append(Satellite(2,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  95 3.4627 0000000 100 50.0288 6.2125391563537',
                        30))
satArr.append(Satellite(8,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  82 81.4627 0000000 100 50.0288 10.2125391563537',
                        30))
satArr.append(Satellite(9,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  42 8.4627 0000000 100 50.0288 10.2125391563537',
                        30))
satArr.append(Satellite(10,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  36 95.4627 0000000 100 50.0288 10.2125391563537',
                        30))
satArr.append(Satellite(11,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  15 300.4627 0000000 100 50.0288 10.2125391563537',
                        30))
satArr.append(Satellite(12,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  69 240.4627 0000000 100 50.0288 10.2125391563537',
                        30))
satArr.append(Satellite(13,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  72 310.4627 0000000 100 50.0288 10.2125391563537',
                        30))
satArr.append(Satellite(14,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  83 63.4627 0000000 100 50.0288 6.2125391563537',
                        45))
satArr.append(Satellite(15,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  85 63.4627 0000000 100 50.0288 6.2125391563537',
                        45))
satArr.append(Satellite(16,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  88 63.4627 0000000 100 50.0288 6.2125391563537',
                        45))
satArr.append(Satellite(17,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  91 63.4627 0000000 100 50.0288 6.2125391563537',
                        45))

badZones = [
    (72.243807, -41.896169, 1200)
]

points = [(55.094670, 37.897833),
          (58.789068, 35.857587),
          (59.093784, 46.832241),
          (54.014399, 43.481651)]

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
                print(id, satellite.maxDist, dist, time)
                minTime[ip] = min(minTime[ip], time)

    if (max(minTime) == 1e20):
        print("Спутники не могут получить фото.")
    else:
        print("Спутники получат фото через", max(minTime), "минут.")

    ax.set_aspect('equal')
    ax.set_adjustable('box')
    plt.show()

print(checkBadPoints(points, badZones))