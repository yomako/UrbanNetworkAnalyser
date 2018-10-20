import codecs
import numpy as np
import math
import matplotlib.pyplot as plt
import pickle


class Stop:

    id = None
    coordinates = None

    def __init__(self, id, coordinates):
        self.id = id
        self.coordinates = coordinates


class Relation:

    i_id = None
    j_id = None
    distance = None

    def __init__(self, i, j, distance):
        self.i_id = i
        self.j_id = j
        self.distance = distance

    def __lt__(self, other):
        return self.distance < other.distance

    def print_relation(self):
        print(self.i_id, self.j_id, self.distance)


def distance_in_m(stop_a, stop_b):
    d_lat = abs(stop_a[0] - stop_b[0])
    d_lng = abs(stop_a[1] - stop_b[1])
    r_earth = 6370000
    return int(math.sqrt((d_lng * r_earth * math.pi * abs(math.cos(math.radians(stop_a[0]))) / 180) ** 2 + (
                d_lat * r_earth * math.pi / 180) ** 2))


def remove_stop_from_relations(relations):
    r_id = relations[-1].i_id
    ind = []
    for it, rel in enumerate(relations):
        if rel.i_id == r_id or rel.j_id == r_id:
            ind.append(it)
    ind.sort(reverse=True)
    for ii in ind:
        relations.pop(ii)


def wroclaw_net_loader(load_pickle=True):
    relations = None
    o_stops = None
    if load_pickle is False:
        stops = []
        for line in enumerate(codecs.open("WroclawWspolrzedne.txt", "r", "utf-8")):
            s_line = line[1].split(';')
            bus = False
            for i in range(len(s_line[3])-2):
                if s_line[3][i] == '3':
                    bus = True

            if bus is True:
                stops.append(np.array([float(s_line[1].replace(',', '.')), float(s_line[0].replace(',', '.'))]))

        stops = np.array(stops)
        o_stops = []
        relations = []
        for i in range(stops.shape[0]):
            o_stops.append(Stop(i, stops[i]))
            for j in range(i+1, stops.shape[0]):
                relations.append(Relation(i, j, distance_in_m(stops[i], stops[j])))

        relations.sort(reverse=True)
        print(relations[-1].distance)
        removed = []
        while relations[-1].distance < 65:
            removed.append(relations[-1].i_id)
            remove_stop_from_relations(relations)

        print(len(o_stops))
        for o_stop in o_stops:
            if o_stop.id in removed:
                o_stops.remove(o_stop)

        print(len(o_stops))

        pickle.dump(o_stops, open('stops_final/wroclaw_stops.p', 'wb'))
        pickle.dump(relations, open('stops_final/wroclaw_relations.p', 'wb'))

    else:
        relations = pickle.load(open('stops_final/wroclaw_relations.p', 'rb'))
        o_stops = pickle.load(open('stops_final/wroclaw_stops.p', 'rb'))
        f = open("wroclaw_stops_points.txt", 'w')
        for o_stop in o_stops:
            f.write("{0:.6f},{1:.6f}\n".format(o_stop.coordinates[0], o_stop.coordinates[1]))

        f.close()


if __name__ == "__main__":
    wroclaw_net_loader()
