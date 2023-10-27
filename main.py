from sgp4.api import jday, Satrec
import matplotlib.pyplot as plt
import numpy as np
import math
from sat import *

satArr = [];
satArr.append(Satellite(0,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  0 0.4627 0000000 130.5360 325.0288 16',
                        30))
satArr.append(Satellite(1,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  45 0.4627 0000000 130.5360 325.0288 11.2125391563537',
                        30))
satArr.append(Satellite(2,
                        '1 25544U 98067A   23299.67161777  .00013592  00000-0  24854-3 0  9993',
                        '2 25544  15 150.4627 0000000 100 50.0288 10.2125391563537',
                        30))

points = [Point(10.211426, -66.693956)]

ax = plt.axes(projection='3d')

def distFromTo(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

#draw points
for point in points:
    ax.scatter(point.x, point.y, point.z)

# make sphere
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
scale = R
x = np.cos(u)*np.sin(v) * scale
y = np.sin(u)*np.sin(v) * scale
z = np.cos(v) * scale
ax.plot_surface(x, y, z, color="r", alpha = 0.3)

#orbits
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
        if(i % 2 == 0):
            jd, fr = jday(2023, 10, int(0 + i / 60 / 24 % 30), int(i / 60 % 24), int(i % 60), 0)
            e, r, v = satellite.sgp4(jd, fr)
            x.append([r[0]])
            y.append([r[1]])
            z.append([r[2]])

            # перебираем точки
            for ip, point in enumerate(points):
                distToPoint = distFromTo(r[0], r[1], r[2], point.x, point.y, point.z)
                # если дист < минДист и дист < максДист
                if(dists[id][ip][0] > distToPoint and sat.maxDist >= distToPoint):
                    dists[id][ip][0] = distToPoint
                    dists[id][ip][1] = SatPoint(r[0], r[1], r[2])
                    print(i)
                    dists[id][ip][2] = i
    # рисуем весь путь
    ax.plot3D(x, y, z)

minTime = 1e20
for id, sat in enumerate(dists):
    for _, point, time in sat:
        if point != 0:
            ax.scatter(point.x, point.y, point.z)
            satellite = satArr[id]
            print(id, satellite.maxDist, _, time)
            minTime = min(minTime, time)

if(minTime == 1e20):
    print("Спутники не могут получить фото.")
else:
    print("Спутники получат фото через", minTime, "минут.")

ax.set_aspect('equal')
ax.set_adjustable('box')
plt.show()