'''
- - - - - - - - - - - - - - - - - - - - -
Name - Maker of urban road graph
Goal - making a complete graph of urban road net, nodes symbolize points in a city, edges conform to route between that
points
Author - Tomasz Bałdyga
- - - - - - - - - - - - - - - - - - - - -
'''


import requests
import codecs
import json


class Edge:

    origin = None
    origin_name = None
    destination = None
    destination_name = None
    route = None

    def __init__(self, origin, destination, origin_name="", destination_name=""):
        '''
        :param origin: coordinates of starting point of route, example: xx.xxxx,yy.yyyy
        :param destination: coordinates of final point of route, example: xx.xxxx,yy.yyyy
        :param origin_name: name of starting point (optional)
        :param destination_name: name of final point (optional)
        '''
        self.origin = origin
        self.origin_name = origin_name
        self.destination = destination
        self.destination_name = destination_name
        self.route = []


def line_counter(file_name):
    # returning count of lines in text file
    try:
        num_lines = sum(1 for line in codecs.open(file_name, "r", "utf-8"))
        return num_lines
    except FileNotFoundError:
        return 0


def get_request(end, waypoints, key):
    request = "https://maps.googleapis.com/maps/api/directions/json?origin=" + end + "&destination=" + end + "&waypoints=" + waypoints[0]
    for i in range(len(waypoints)-1):
        request += "|" + end + "|" + waypoints[i+1]
    return request + "&key=" + key


def string_maker(edges, start, key, result_filename, square_net_mode):
    # making string of waypoints, sending requests, saving results to text file
    khy = 0
    for i in range(11):
        try:
            if edges[start].origin == edges[23+start-2*i].destination:
                khy = 11 - i
                break
        except Exception:
            pass

    origin = str(edges[start].origin)
    waypoints = []
    requests_list = []

    for i in range(khy+1):
        if (khy+1) == 1:
            waypoints.append(str(edges[start].destination))
            requests_list.append(get_request(origin, waypoints, key))
        else:
            if i == 0:
                waypoints.append(str(edges[start].destination))
            elif i == khy:
                waypoints.append(str(edges[start+2*khy].destination))
            else:
                waypoints.append(str(edges[start + 2*i].destination))
            requests_list.append(get_request(origin, waypoints, key))

    file = codecs.open(result_filename, "a", "utf-8")
    fails = 0
    j = None
    qr = 0
    try:
        for q in range(len(requests_list)):
            qr = q
            r = requests.get(requests_list[-1 - q])
            j = json.loads(r.text)
            if str(j['status']) == 'OK':
                break
    except Exception:
        return start
    while True:
        try:
            for k in range(2*(khy-qr+1)):
                line = ""
                origin = edges[start+k].origin
                origin_name = edges[start+k].origin_name
                destination = edges[start+k].destination
                destination_name = edges[start+k].destination_name
                if square_net_mode is True:
                    origin_name = j['routes'][0]['legs'][k]['start_address']
                    spl_origin = origin_name.split(",")
                    origin_name = spl_origin[0]
                    destination_name = j['routes'][0]['legs'][k]['end_address']
                    spl_destination = destination_name.split(",")
                    destination_name = spl_destination[0]

                duration = j['routes'][0]['legs'][k]['duration']['value']
                distance = j['routes'][0]['legs'][k]['distance']['value']
                line += str(start+k) + ";" + origin_name + ":" + str(origin) + ";" + destination_name + ":" + str(destination) + ";" + str(duration) + ";" + str(distance)
                i = 0
                while True:
                    try:
                        s_origin = "" + str(j['routes'][0]['legs'][k]['steps'][i]['start_location']['lat']) + "," + str(j['routes'][0]['legs'][k]['steps'][i]['start_location']['lng'])
                        s_destination = "" + str(j['routes'][0]['legs'][k]['steps'][i]['end_location']['lat']) + "," + str(j['routes'][0]['legs'][k]['steps'][i]['end_location']['lng'])
                        s_distance = j['routes'][0]['legs'][k]['steps'][i]['distance']['value']
                        s_duration = j['routes'][0]['legs'][k]['steps'][i]['duration']['value']
                        line += ";" + str(s_origin) + ":" + str(s_destination) + ":" + str(s_duration) + ":" + str(s_distance)
                        i += 1
                    except Exception:
                        break
                line += ";\n"
                file.write(line)
            break
        except Exception:
            fails += 1
            if fails > 20:
                print("Failure")
                exit(10)
                return start
            pass
    file.close()
    return start + 2*(khy - qr + 1)


def load_keys(not_accepted_keys=[]):
    # loading keys from text file
    temp = []
    i_accepted = 0
    for line in enumerate(codecs.open('keys.txt', "r", "utf-8")):
        if len(not_accepted_keys) == 0 or line[0] not in not_accepted_keys:
            temp.append(line[1][0:39])
            i_accepted += 1
    assert (1 - len(not_accepted_keys)) == i_accepted, "At least one key was not loaded."
    return temp


def stops_data_collector():
    source = "RA180310"
    keys = load_keys()
    s_edges = []
    s_names = []
    coordinates = []
    for s_line in enumerate(open('{0}_centered_stops_final.txt'.format(source), encoding="utf8")):
        m = s_line[1].split(" ")
        coordinates.append("" + m[len(m) - 5] + "," + m[len(m) - 2])
        s_name = ""
        for ii in range(len(m) - 8):
            if ii != 0:
                s_name += " "
                s_name += m[1 + ii]
        s_name = s_name[:-1]
        s_names.append(s_name)

    for ii in range(len(coordinates)):
        for jj in range(ii + 1, len(coordinates)):
            s_edges.append(Edge(coordinates[ii], coordinates[jj], s_names[ii], s_names[jj]))
            s_edges.append(Edge(coordinates[jj], coordinates[ii], s_names[jj], s_names[ii]))

    pointer = string_maker(s_edges, line_counter("net.txt"), True, keys[0])
    one = 1
    quest = 2500
    for s_key in keys:
        for ii in range(quest):
            if pointer < len(s_edges):
                pointer = string_maker(s_edges, pointer, True, s_key)
            else:
                print("Collection of data is finished.")
                break
            if ii % 10 == 0:
                print(one, ii)
        one += 1


def square_net_data_collector(city, quest):
    keys = load_keys()
    filename = "{0}_net.txt".format(city)
    s_edges = []
    coordinates = []
    for s_line in enumerate(open('{0}_points.txt'.format(city), encoding="utf8")):
        coordinates.append(s_line[1][0:-1])
    for ii in range(len(coordinates)):
        for jj in range(ii + 1, len(coordinates)):
            s_edges.append(Edge(coordinates[ii], coordinates[jj]))
            s_edges.append(Edge(coordinates[jj], coordinates[ii]))

    pointer = string_maker(s_edges, line_counter(filename), keys[0], filename, True)
    one = 1
    for s_key in keys:
        for ii in range(quest):
            if pointer < len(s_edges):
                pointer = string_maker(s_edges, pointer, s_key, filename, True)
            else:
                print("Collection of data is finished.")
                exit(11)
            if ii % 10 == 0:
                print("klucz", one, "postęp:", (float(pointer)/len(s_edges)*100), "%")
                if float(pointer)/len(s_edges) > 1:
                    print("Collection of data is finished.")
                    exit(12)

        one += 1
