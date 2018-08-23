import codecs
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
from complement import complement


class Square:
    """

    """
    lat_max = None
    lat_min = None
    lng_max = None
    lng_min = None
    presence = None
    part_of_the_city = None

    def __init__(self, lat_max, lat_min, lng_max, lng_min):
        self.lat_max = lat_max
        self.lat_min = lat_min
        if self.lat_max < self.lat_min:
            self.lat_max, self.lat_min = self.lat_min, self.lat_max
        self.lng_max = lng_max
        self.lng_min = lng_min
        if self.lng_max < self.lng_min:
            self.lng_max, self.lng_min = self.lng_min, self.lng_max
        self.part_of_the_city = False

    def contains(self, tlat, tlng):
        if (self.lat_min <= tlat <= self.lat_max) and (self.lng_min <= tlng <= self.lng_max):
            return True
        else:
            return False

    def print_nodes(self):
        print("lat_max={0}, lat_min={1}, lng_max={2}, lng_min={3}".format(self.lat_max, self.lat_min, self.lng_max, self.lng_min))

    def presence_checker(self, lat, lng):
        self.presence = False
        for i in range(len(lat)):
            if (self.lat_min <= lat[i] <= self.lat_max) and (self.lng_min <= lng[i] <= self.lng_max):
                self.presence = True
                break

    def get_random(self):
        return random.uniform(self.lat_min, self.lat_max), random.uniform(self.lng_min, self.lng_max)

    def get_field(self):
        d_lat = abs(self.lat_max-self.lat_min)
        d_lng = abs(self.lng_max-self.lng_min)
        r_earth = 6370000
        return d_lng*d_lat*(r_earth**2)*(math.pi**2)*(abs(math.cos(math.radians(self.lat_max)))+abs(math.cos(math.radians(self.lat_min))))/64800


class City:
    lat = None
    lng = None
    city = None
    d_lat = None
    d_lng = None
    area = None
    superficial_density_standard = None

    def __init__(self, city_name):
        self.lat = []
        self.lng = []
        self.city = city_name
        try:
            self.load_contour()
        except FileNotFoundError:
            print("Incorrect city name.")
            exit(3)
        self.area = self.area_of_city(self.make_square_net(6000))
        self.superficial_density_standard = 2.3394091954229875e-06

    def load_contour(self):
        for line in enumerate(codecs.open('{0}_kontur.txt'.format(self.city), "r", "utf-8")):
            splited = line[1].split(" ")
            self.lat.append(float(splited[len(splited) - 5]))
            self.lng.append(float(splited[len(splited) - 2]))

        self.d_lat = max(self.lat) - min(self.lat)
        self.d_lng = max(self.lng) - min(self.lng)

    def make_square_net(self, default_size, save_to_png=False):
        while True:
            h, w = self.sides(default_size)
            lat_step = self.d_lat / w
            lng_step = self.d_lng / h
            city_array = np.zeros([w, h, 4])
            matrix = [[Square(min(self.lat) + (w - y) * lat_step, min(self.lat) + (w - y - 1) * lat_step,
                              min(self.lng) + (x + 1) * lng_step, min(self.lng) + x * lng_step) for x in range(h)] for y in
                      range(w)]
            [[matrix[x][y].presence_checker(self.lat, self.lng) for x in range(w)] for y in range(h)]

            for i in range(w):
                for j in range(h):
                    if matrix[i][j].presence is True:
                        city_array[i][j][0] = 255
                        city_array[i][j][1] = 255
                        city_array[i][j][2] = 255
                        city_array[i][j][3] = 255

            city_array = complement(city_array)
            lista = []
            addons = []
            for i in [0, h - 1]:
                for j in range(w):
                    if city_array[j][i][0] != 255:
                        lista.append([j, i])

            for j in [0, w - 1]:
                for i in range(h):
                    if city_array[j][i][0] != 255:
                        lista.append([j, i])

            last_layer = list(lista)

            while True:
                for element in last_layer:
                    self.black_propagation(element[0], element[1], city_array, lista, last_layer, addons, h, w)
                lista = lista + last_layer
                last_layer = list(addons)
                addons = []
                if len(last_layer) == 0:
                    break

            border = []
            for element in lista:
                self.border_propagation(element[0], element[1],  lista, last_layer, addons, border, h, w)
            lista = lista + border
            cepkel = np.full([w, h, 4], 255)
            for element in lista:
                try:
                    cepkel[element[0]][element[1]][0] = 0
                    cepkel[element[0]][element[1]][1] = 0
                    cepkel[element[0]][element[1]][2] = 0
                    cepkel[element[0]][element[1]][3] = 0
                except Exception:
                    print(element[0], w, element[1], h)

            for i in [0, h - 1]:
                for j in range(w):
                    cepkel[j][i][0] = 0
                    cepkel[j][i][1] = 0
                    cepkel[j][i][2] = 0
                    cepkel[j][i][3] = 0

            for j in [0, w - 1]:
                for i in range(h):
                    cepkel[j][i][0] = 0
                    cepkel[j][i][1] = 0
                    cepkel[j][i][2] = 0
                    cepkel[j][i][3] = 0

            for i in range(h):
                for j in range(w):
                    if cepkel[j][i][0] == 255:
                        matrix[j][i].part_of_the_city = True
            if self.get_potc_count(matrix) > h*w/3:
                break

        if save_to_png is True:
            plt.imsave('{0}_test.png'.format(self.city), cepkel, cmap=cm.gray)
        return matrix

    @staticmethod
    def get_potc_count(matrix):
        count = 0
        for i in matrix:
            for j in i:
                if j.part_of_the_city is True:
                    count += 1
        return count

    def sides(self, default_size):
        c = math.sqrt(default_size/self.d_lat/self.d_lng)
        return round(self.d_lng*c), round(self.d_lat*c)

    def area_of_city(self, city_matrix, text=False):
        area = 0
        for y in city_matrix:
            for x in y:
                if x.part_of_the_city is True:
                    area += x.get_field()
        area *= 1.017
        if text is True:
            print("Field of city of {0} is in approximation {1}km^2".format(self.city, area/1000000))
        return area

    @staticmethod
    def black_propagation(x, y, city_array, lista, last_layer, addons, h, w):
        for i in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            try:
                if city_array[x + i[0]][y + i[1]][0] != 255 and not [x + i[0], y + i[1]] in lista and not [x + i[0], y + i[1]] in addons and not [x + i[0], y + i[1]] in last_layer and (x + i[0]) != -1 and (y + i[1]) != -1 and (x + i[0]) != w and (y + i[1]) != h:
                    addons.append([x + i[0], y + i[1]])
            except Exception:
                pass

    @staticmethod
    def border_propagation(x, y, lista, last_layer, addons, border, h, w):
        for i in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            try:
                if not [x + i[0], y + i[1]] in lista and not [x + i[0], y + i[1]] in addons and not [x + i[0], y + i[1]] in last_layer and (x + i[0]) != -1 and (y + i[1]) != -1 and (x + i[0]) != w and (y + i[1]) != h:
                    border.append([x + i[0], y + i[1]])
            except Exception:
                pass

    def generate_random_points(self, matrix):
        file = codecs.open("{0}_points.txt".format(self.city), "w", "utf-8")

        for i in matrix:
            for j in i:
                if j.part_of_the_city is True:
                    result = j.get_random()
                    file.write("{0:.6f},{1:.6f}\n".format(result[0], result[1]))

    def fit_matrix(self, step):
        dif = []
        previous_step = step
        while True:
            matrix = self.make_square_net(step)
            dif.append(abs((self.get_potc_count(matrix)/self.area) - self.superficial_density_standard))
            if ((self.get_potc_count(matrix)/self.area) - self.superficial_density_standard) > 0:
                if dif[-1] > dif[-2]:
                    matrix = self.make_square_net(previous_step)
                break
            else:
                previous_step = step
                step = self.next_step(step)
        return matrix

    def next_step(self, step):
        h, w = self.sides(step)
        while True:
            ho, wo = self.sides(step + 1)
            if (ho * wo) != (h * w):
                return (step + 1)
            else:
                step += 1


def field_of_the_earth():
    world_field = 0
    for la in range(-180, 180):
        for ln in range(-90, 90):
            sq = Square(la, la+1, ln, ln+1)
            world_field += sq.get_field()
    print("Field of the Earth is {} km^2".format(world_field/1000000))
