'''
- - - - - - - - - - - - - - - - - - - - -
Name -
Goal -
Author - Tomasz Bałdyga
- - - - - - - - - - - - - - - - - - - - -
'''

import numpy as np
import math
from PIL import Image
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from operator import itemgetter


class Cluster:

    points = None

    def __init__(self):
        self.points = []


def is_neighbour(aa, bb):
    if math.sqrt((aa[0]-bb[0])**2+(aa[1]-bb[1])**2) <= math.sqrt(2):
        return True
    else:
        return False


def sub_complement(aa, bb, clusters, p):
    if abs(aa[0] - bb[0]) > abs(aa[1] - bb[1]):
        for pp in range(abs(aa[0] - bb[0]) - 1):
            xx = 0
            yy = 0
            if aa[0] < bb[0] and aa[1] < bb[1]:
                xx = aa[0] + 1 + pp
                yy = aa[1] + math.ceil(
                    ((pp + 1) / (abs(aa[0] - bb[0]) - 1) * (abs(aa[1] - bb[1]) - 1)))
                if abs(aa[1] - bb[1]) == 0:
                    yy = aa[1]
            if aa[0] >= bb[0] and aa[1] < bb[1]:
                xx = bb[0] + 1 + pp
                yy = aa[1] + math.ceil(
                    ((pp + 1) / (abs(aa[0] - bb[0]) - 1) * (abs(aa[1] - bb[1]) - 1)))
                if abs(aa[1] - bb[1]) == 0:
                    yy = aa[1]
            if aa[0] < bb[0] and aa[1] >= bb[1]:
                xx = aa[0] + 1 + pp
                yy = bb[1] + math.ceil(
                    ((pp + 1) / (abs(aa[0] - bb[0]) - 1) * (abs(aa[1] - bb[1]) - 1)))
                if abs(aa[1] - bb[1]) == 0:
                    yy = bb[1]
            if aa[0] >= bb[0] and aa[1] >= bb[1]:
                xx = bb[0] + 1 + pp
                yy = bb[1] + math.ceil(
                    ((pp + 1) / (abs(aa[0] - bb[0]) - 1) * (abs(aa[1] - bb[1]) - 1)))
                if abs(aa[1] - bb[1]) == 0:
                    yy = bb[1]
            clusters[0].points.append([xx, yy])
            p[xx][yy][0] = 255
            p[xx][yy][1] = 255
            p[xx][yy][2] = 255
            p[xx][yy][3] = 255
    else:
        for pp in range(abs(aa[1] - bb[1]) - 1):
            xx = 0
            yy = 0
            if aa[0] < bb[0] and aa[1] < bb[1]:
                yy = aa[1] + 1 + pp
                xx = aa[0] + math.ceil(
                    ((pp + 1) / (abs(aa[1] - bb[1]) - 1) * (abs(aa[0] - bb[0]) - 1)))
                if abs(aa[0] - bb[0]) == 0:
                    xx = aa[0]
            if aa[0] >= bb[0] and aa[1] < bb[1]:
                yy = aa[1] + 1 + pp
                xx = bb[0] + math.ceil(
                    ((pp + 1) / (abs(aa[1] - bb[1]) - 1) * (abs(aa[0] - bb[0]) - 1)))
                if abs(aa[0] - bb[0]) == 0:
                    xx = bb[0]
            if aa[0] < bb[0] and aa[1] >= bb[1]:
                yy = bb[1] + 1 + pp
                xx = aa[0] + math.ceil(
                    ((pp + 1) / (abs(aa[1] - bb[1]) - 1) * (abs(aa[0] - bb[0]) - 1)))
                if abs(aa[0] - bb[0]) == 0:
                    xx = aa[0]
            if aa[0] >= bb[0] and aa[1] >= bb[1]:
                yy = bb[1] + 1 + pp
                xx = bb[0] + math.ceil(
                    ((pp + 1) / (abs(aa[1] - bb[1]) - 1) * (abs(aa[0] - bb[0]) - 1)))
                if abs(aa[0] - bb[0]) == 0:
                    xx = bb[0]
            clusters[0].points.append([xx, yy])
            p[xx][yy][0] = 255
            p[xx][yy][1] = 255
            p[xx][yy][2] = 255
            p[xx][yy][3] = 255


def complement(p):
    squares = []
    for ii in range(p.shape[0]):
        for jj in range(p.shape[1]):
            if p[ii][jj][0] == 255:
                squares.append([ii, jj])

    clusters = []
    while len(squares) != 0:
        clusters.append(Cluster())
        random_square = squares[random.randrange(len(squares))]
        clusters[-1].points.append(random_square)
        squares.remove(random_square)
        layer = [random_square]
        while len(layer) != 0:
            neighbours = []
            for ii in layer:
                for jj in range(3):
                    for kk in range(3):
                        try:
                            if p[ii[0]-1+jj][ii[1]-1+kk][0] == 255 \
                                    and [ii[0]-1+jj, ii[1]-1+kk] not in clusters[-1].points \
                                    and (jj != 1 or kk != 1) \
                                    and [ii[0]-1+jj, ii[1]-1+kk] not in neighbours \
                                    and [ii[0]-1+jj, ii[1]-1+kk] in squares:
                                neighbours.append([ii[0]-1+jj, ii[1]-1+kk])
                                squares.remove([ii[0]-1+jj, ii[1]-1+kk])
                        except IndexError:
                            pass

            clusters[-1].points.extend(neighbours)
            layer = list(neighbours)

    while len(clusters) != 1:
        distance = 0
        first = [0, 0]
        second = [0, 0]
        second_pos = 0
        for point in clusters[0].points:
            for ii in range(len(clusters)-1):
                for jj in clusters[ii+1].points:
                    a_distance = (abs(point[0] - jj[0]) + abs(point[1] - jj[1]))
                    if distance == 0 or a_distance < distance:
                        distance = a_distance
                        first = point
                        second = jj
                        second_pos = ii + 1

        sub_complement(first, second, clusters, p)

        clusters[0].points.extend(clusters[second_pos].points)
        clusters.pop(second_pos)

    order = []
    main_iteration = 0
    for ii in clusters[0].points:
        iteration = 0
        layer = [ii]
        was = []
        while len(layer) != 0:
            temp = []
            iteration += 1
            for la in layer:
                for jj in range(3):
                    for kk in range(3):
                        try:
                            if p[la[0]-1+jj][la[1]-1+kk][0] == 255 and (jj != 1 or kk != 1) and [la[0]-1+jj, la[1]-1+kk] not in was and [la[0]-1+jj, la[1]-1+kk] not in temp and 0 <= (la[0]-1+jj) < p.shape[0] and 0 <= (la[1]-1+kk) < p.shape[1]:
                                temp.append([la[0]-1+jj, la[1]-1+kk])
                        except IndexError:
                            pass
            layer = list(temp)
            was.extend(temp)
        order.append([main_iteration, iteration])
        main_iteration += 1
    order = sorted(order, key=itemgetter(1), reverse=True)
    iteration = 1
    while True:
        if is_neighbour(clusters[0].points[order[0][0]], clusters[0].points[order[iteration][0]]) is False:
            break
        else:
            iteration += 1
    sub_complement(clusters[0].points[order[0][0]], clusters[0].points[order[iteration][0]], clusters, p)

    return p
