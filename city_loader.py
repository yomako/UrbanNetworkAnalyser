import codecs
from pprint import pprint
import tic_toc
from cartographer import line_counter
import pickle
import numpy as np
import math
from percolation import *
from city_loader_histograms import *
from square_net import City
from astropy.visualization import make_lupton_rgb
import sys


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
        self.distance = int(records[4])
        self.subjunctions = []
        for i in range(len(records)-6):
            self.subjunctions.append(self.Subjunction(records[5+i]))
        if len(self.subjunctions) == 2:
            self.duration -= self.subjunctions[0].duration
            self.distance -= self.subjunctions[0].distance
        if len(self.subjunctions) > 2:
            self.duration -= self.subjunctions[0].duration
            self.duration -= self.subjunctions[-1].duration
            self.distance -= self.subjunctions[0].distance
            self.distance -= self.subjunctions[-1].distance


class Node:
    lat = None
    lng = None
    duration_input_force = None
    duration_output_force = None
    distance_input_force = None
    distance_output_force = None
    manoeuvres_input_force = None
    manoeuvres_output_force = None
    velocity_input_force = None
    velocity_output_force = None

    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng
        self.duration_input_force = 0
        self.duration_output_force = 0
        self.distance_input_force = 0
        self.distance_output_force = 0
        self.manoeuvres_input_force = 0
        self.manoeuvres_output_force = 0
        self.velocity_input_force = 0
        self.velocity_output_force = 0


def normalize(array):
    """
    Normalizes array.

    Args:
        array: array to normalization

    Returns:
         Normalized array.
    """
    array = np.array(array)
    return array / np.sum(array, axis=0)


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
    for line in enumerate(codecs.open("{}_net.txt".format(city), "r", "utf-8")):
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


def merge(junctions):
    len_before = len(junctions)
    for counter, i in enumerate(junctions):
        if i.duration == 0:
            erase_sub_list = []
            for pos, k in enumerate(junctions):
                if (k.origin_lat == i.origin_lat and k.origin_lng == i.origin_lng) or (
                        k.destination_lat == i.origin_lat and k.destination_lng == i.origin_lng):
                    erase_sub_list.append(pos)
            erase_sub_list.sort(reverse=True)
            for n in erase_sub_list:
                junctions.pop(n)
            break
    if len_before == len(junctions):
        return False
    else:
        return True


def merge_zero_duration_elements(junctions):
    while True:
        if merge(junctions) is False:
            break


def make_neighborhood_matrix(junctions, duration_hold):
    size = int(0.5*(1+math.sqrt(1+4*len(junctions))))
    points_strings = []
    points_lat = []
    points_lng = []
    for i in junctions:
        if "{0};{1}".format(i.origin_lat, i.origin_lng) not in points_strings:
            points_strings.append("{0};{1}".format(i.origin_lat, i.origin_lng))
            points_lat.append(i.origin_lat)
            points_lng.append(i.origin_lng)
    neighborhood_matrix = np.zeros(shape=(size, size))
    for i in junctions:
        x = points_strings.index("{0};{1}".format(i.origin_lat, i.origin_lng))
        y = points_strings.index("{0};{1}".format(i.destination_lat, i.destination_lng))
        if i.duration <= duration_hold:
            neighborhood_matrix[x][y] = 1
        else:
            neighborhood_matrix[x][y] = 0
    return neighborhood_matrix


def find_max_duration(junctions):
    durations = []
    for i in junctions:
        durations.append(i.duration)
    return max(durations)


def percolation_calculations(junctions, city):
    the_biggest_clusters_sizes = []
    durations = []
    max_duration = find_max_duration(junctions)
    for duration in range(max_duration+1):
        print(duration, max_duration)
        neighborhood_matrix = make_neighborhood_matrix(junctions, duration)
        clusters = clusters_identifier(neighborhood_matrix)
        the_biggest_clusters_sizes.append((the_biggest_cluster_size(clusters)/neighborhood_matrix.shape[0]))
        durations.append(duration)
        if the_biggest_cluster_size(clusters) == neighborhood_matrix.shape[0]:
            break
    pickle.dump(durations, open('perkolacja_czasowa/x_array_{}.p'.format(city), 'wb'))
    pickle.dump(the_biggest_clusters_sizes, open('perkolacja_czasowa/y_array_{}.p'.format(city), 'wb'))


def calculate_mean_velocity(junctions):
    mean_velocity = 0.0
    for i in junctions:
        mean_velocity += float(i.distance)/float(i.duration)
    mean_velocity /= len(junctions)
    return mean_velocity


def generate_mean_velocity_data(junctions, city):
    x = []
    for i in junctions:
        x.append(float(i.distance) / float(i.duration))
    pickle.dump(x, open('mean_velocity/x_array_{}.p'.format(city), 'wb'))


def generate_duration_distribution(junctions, city):
    t = []
    x = []
    durations = []
    for i in junctions:
        t.append(i.duration)
    for duration in range(max(t)+1):
        y = 0
        print(duration)
        for i in junctions:
            if i.duration <= duration:
                y += 1
        y /= len(junctions)
        durations.append(duration)
        x.append(y)
    pickle.dump(durations, open('duration_distribution/x_array_{}.p'.format(city), 'wb'))
    pickle.dump(x, open('duration_distribution/y_array_{}.p'.format(city), 'wb'))


def generate_duration_distribution2(junctions, city):
    t = []
    x = []
    durations = []
    for i in junctions:
        t.append(i.duration)
    for duration in range(max(t)+1):
        y = 0
        print(duration)
        for i in junctions:
            if i.duration <= duration:
                y += 1
        y /= len(junctions)
        durations.append(duration)
        x.append(y)
    pickle.dump(durations, open('duration_distribution2/x_array_{}.p'.format(city), 'wb'))
    pickle.dump(x, open('duration_distribution2/y_array_{}.p'.format(city), 'wb'))


def make_nodes_list(junctions):
    coords = []
    nodes = []
    for i in junctions:
        if "{0},{1}".format(i.origin_lat, i.origin_lng) not in coords:
            coords.append("{0},{1}".format(i.origin_lat, i.origin_lng))
            nodes.append(Node(i.origin_lat, i.origin_lng))
    for i in junctions:
        input_index = coords.index("{0},{1}".format(i.destination_lat, i.destination_lng))
        output_index = coords.index("{0},{1}".format(i.origin_lat, i.origin_lng))
        nodes[input_index].distance_input_force += i.distance
        nodes[output_index].distance_output_force += i.distance
        nodes[input_index].duration_input_force += i.duration
        nodes[output_index].duration_output_force += i.duration
        nodes[input_index].manoeuvres_input_force += len(i.subjunctions)
        nodes[output_index].manoeuvres_output_force += len(i.subjunctions)
        if i.duration != 0:
            nodes[input_index].velocity_input_force += i.distance/i.duration
            nodes[output_index].velocity_output_force += i.distance/i.duration

    return nodes


def draw_velocity_map(city):
    image_r = pickle.load(open('velocity_arrays/image_r_array_{}.p'.format(city), 'rb'))
    image_g = pickle.load(open('velocity_arrays/image_g_array_{}.p'.format(city), 'rb'))
    image_b = pickle.load(open('velocity_arrays/image_b_array_{}.p'.format(city), 'rb'))
    image = make_lupton_rgb(image_r, image_g, image_b, stretch=0.5)
    plt.imsave('velocity_maps/{}_velocity_map.png'.format(city), image)


def calculate_forces(city):
    jun, ca = load(city)
    coords2 = []
    for ii in jun:
        if "{0},{1}".format(ii.origin_lat, ii.origin_lng) not in coords2:
            coords2.append("{0},{1}".format(ii.origin_lat, ii.origin_lng))
    merge_zero_duration_elements(jun)
    coords3 = []
    for ii in jun:
        if "{0},{1}".format(ii.origin_lat, ii.origin_lng) not in coords3:
            coords3.append("{0},{1}".format(ii.origin_lat, ii.origin_lng))
    for ll in coords3:
        if ll in coords2:
            coords2.remove(ll)
    diffs = []
    for uu in coords2:  # merdżowanie
        diff = -1
        for pp in range(len(coords3)):
            if diff == -1:
                sr = uu.split(',')
                st = coords3[pp].split(',')
                diffs.append(pp)
                diff = ((float(sr[0]) - float(st[0])) ** 2 + (float(sr[1]) - float(st[1])) ** 2)
            else:
                sr = uu.split(',')
                st = coords3[pp].split(',')
                if ((float(sr[0]) - float(st[0])) ** 2 + (float(sr[1]) - float(st[1])) ** 2) < diff:
                    diffs[-1] = pp
                    diff = ((float(sr[0]) - float(st[0])) ** 2 + (float(sr[1]) - float(st[1])) ** 2)

    blank_nodes = []
    for hh in coords2:
        sr = hh.split(',')
        blank_nodes.append(Node(float(sr[0]), float(sr[1])))
    nd = make_nodes_list(jun)
    man_in = []
    man_out = []
    dur_in = []
    dur_out = []
    dis_in = []
    dis_out = []
    vel_in = []
    vel_out = []
    for nn in nd:
        man_out.append(nn.manoeuvres_output_force)
        man_in.append(nn.manoeuvres_input_force)
        dur_in.append(nn.duration_input_force)
        dur_out.append(nn.duration_output_force)
        dis_in.append(nn.distance_input_force)
        dis_out.append(nn.distance_output_force)
        vel_in.append(nn.velocity_input_force)
        vel_out.append(nn.velocity_output_force)

    fig, axes = plt.subplots(nrows=2, ncols=4)

    axes[0][0].hist(dis_in, np.linspace(min(dis_in), max(dis_in), 20), alpha=0.5, normed=1)
    axes[0][0].set_title('Siła wejściowa dystansowa')
    axes[1][0].hist(dis_out, np.linspace(min(dis_out), max(dis_out), 20),  alpha=0.5, normed=1)
    axes[1][0].set_title('Siła wyjściowa dystansowa')
    axes[0][1].hist(dur_in, np.linspace(min(dur_in), max(dur_in), 20), alpha=0.5, normed=1)
    axes[0][1].set_title('Siła wejściowa czasowa')
    axes[1][1].hist(dur_out, np.linspace(min(dur_out), max(dur_out), 20), alpha=0.5, normed=1)
    axes[1][1].set_title('Siła wyjściowa czasowa')
    axes[0][2].hist(vel_in, np.linspace(min(vel_in), max(vel_in), 20), alpha=0.5, normed=1)
    axes[0][2].set_title('Siła wejściowa prędkościowa')
    axes[1][2].hist(vel_out, np.linspace(min(vel_out), max(vel_out), 20), alpha=0.5, normed=1)
    axes[1][2].set_title('Siła wyjściowa prędkościowa')
    axes[0][3].hist(man_in, np.linspace(min(man_in), max(man_in), 20), alpha=0.5, normed=1)
    axes[0][3].set_title('Siła wejściowa manewrowa')
    axes[1][3].hist(man_out, np.linspace(min(man_out), max(man_out), 20), alpha=0.5, normed=1)
    axes[1][3].set_title('Siła wyjściowa manewrowa')
    #plt.tight_layout()

    plt.show()


def make_velocity_distribution(city):
    jun, ca = load(city)
    velo = []
    for ii in jun:
        for sub_ii in ii.subjunctions:
            if sub_ii.duration != 0:
                velo.append(sub_ii.distance / sub_ii.duration)
    pickle.dump(velo, open('velocity_distribution/_{}.p'.format(city), 'wb'))


if __name__ == "__main__":
    #city_name = str(sys.argv[1:][0])
    city_name = "krakow"
    #make_velocity_arrays(city_name)
    calculate_forces(city_name)
