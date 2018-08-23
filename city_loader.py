import codecs
from pprint import pprint
import tic_toc
from cartographer import line_counter
import pickle
import matplotlib.pyplot as plt
import numpy as np


class Junction:
    origin_lat = None
    origin_lng = None
    origin_name = None
    destination_lat = None
    destination_lng = None
    destination_name = None
    duration = None
    distance = None
    subjunctions = None

    class Subjunction:
        origin_lat = None
        origin_lng = None
        destination_lat = None
        destination_lng = None
        distance = None
        duration = None

        def __init__(self, sline):
            srecords = sline.split(':')
            origin_coords = srecords[0].split(',')
            self.origin_lat = float(origin_coords[0])
            self.origin_lng = float(origin_coords[1])
            destination_coords = srecords[1].split(',')
            self.destination_lat = float(destination_coords[0])
            self.destination_lng = float(destination_coords[1])
            self.duration = int(srecords[2])
            self.distance = int(srecords[3])

    def __init__(self, fline):
        records = fline.split(';')
        origin_fline = records[1].split(':')
        self.origin_name = origin_fline[0]
        origin_coords = origin_fline[1].split(',')
        self.origin_lat = float(origin_coords[0])
        self.origin_lng = float(origin_coords[1])
        destination_fline = records[2].split(':')
        self.destination_name = destination_fline[0]
        destination_coords = destination_fline[1].split(',')
        self.destination_lat = float(destination_coords[0])
        self.destination_lng = float(destination_coords[1])
        self.duration = int(records[3])
        if self.duration == 0:
            pprint(fline)
        self.distance = int(records[4])
        self.subjunctions = []
        for i in range(len(records)-6):
            self.subjunctions.append(self.Subjunction(records[5+i]))


def normalize(array):
    """
    Normalizes array.

    Args:
        array: array to normalization

    Returns:
         Normalized array.
    """
    normalized_array = []

    for s in array:
        normalized_array.append(s/sum(array))
    return normalized_array


def mean_velocity(junctions):
    mean = 0.0
    for i in junctions:
        mean += (i.distance/i.duration)
    print('{} m/s'.format(mean))
    print('{} km/h'.format(mean * 3.6))
    return mean


def load(city):
    TicToc = tic_toc.TicTocGenerator()
    tic_toc.tic(TicToc)
    junctions = []
    subjun = []
    for line in enumerate(codecs.open(city, "r", "utf-8")):
        junctions.append(Junction(line[1]))
        subjun.append(len(junctions[-1].subjunctions))
    city_array = np.array(subjun)
    tic_toc.toc(TicToc)
    return junctions, city_array


def maneuver(city_array, city):
    step = 1
    checked = 0
    y_array = []
    x_array = []
    while checked < city_array.size:
        TicToc = tic_toc.TicTocGenerator()
        tic_toc.tic(TicToc)
        x_array.append(step)
        y_array.append(0)
        y_array[-1] += np.extract(city_array == step, city_array).size
        checked += y_array[-1]
        tic_toc.toc(TicToc)
        print(step, checked, city_array.size)
        step += 1
    pickle.dump(x_array, open('histogram_a/x_array_{}.p'.format(city), 'wb'))
    pickle.dump(y_array, open('histogram_a/y_array_{}.p'.format(city), 'wb'))


def histogram_a_a(city):
    x_array = pickle.load(open('histogram_a/x_array_{}.p'.format(city), 'rb'))
    y_array = normalize(pickle.load(open('histogram_a/y_array_{}.p'.format(city), 'rb')))
    x_array_stops = pickle.load(open('histogram_a/x_array_{}_stops.p'.format(city), 'rb'))
    y_array_stops = normalize(pickle.load(open('histogram_a/y_array_{}_stops.p'.format(city), 'rb')))
    plt.plot(x_array, y_array, x_array_stops, y_array_stops)
    plt.show()


def histogram_a(city):
    x_array = pickle.load(open('histogram_a/x_array_{}.p'.format(city), 'rb'))
    y_array = normalize(pickle.load(open('histogram_a/y_array_{}.p'.format(city), 'rb')))
    plt.plot(x_array, y_array)
    plt.show()
