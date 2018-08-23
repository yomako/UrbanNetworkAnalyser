from PIL import Image
import numpy as np
import codecs
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def get_coordinates(city_name):
    if city_name == "warszawa":
        return 52.098078, 21.080243, 52.201619, 20.851419
    elif city_name == "krakow":
        return 49.967842, 19.955868, 50.013001, 19.792355
    elif city_name == "wroclaw":
        return 51.043164, 17.028941, 51.139337, 16.807842
    elif city_name == "lublin":
        return 51.215286, 22.454251, 51.139756, 22.496754
    elif city_name == "olsztyn":
        return 53.723046, 20.474497, 53.780555, 20.365384
    else:
        raise ValueError


def borderer(city_name):
    try:
        s_lat, s_lng, z_lat, z_lng = get_coordinates(city_name)
    except ValueError:
        print("City name is not correct.")
        exit(1)
    im = Image.open("{0}.png".format(city_name))
    p = np.array(im)

    res_array = np.zeros(shape=[p.shape[0], p.shape[1], 4])
    for x in range(p.shape[0]):
        for y in range(p.shape[1]):
            if (219 <= p[x][y][0] <= 255) and 0 <= p[x][y][1] <= 180 and 0 <= p[x][y][2] <= 107:
                res_array[x][y][0] = 220
                res_array[x][y][1] = 72
                res_array[x][y][2] = 59
                res_array[x][y][3] = 225

    plt.imsave('{0}2.png'.format(city_name), res_array, cmap=cm.gray)

    war = Image.open("{0}2.png".format(city_name))
    f = np.array(war)
    pol_x = 0
    pol_y = 0
    zach_x = 0
    zach_y = f.shape[1]
    print(f.shape)
    for x in range(f.shape[0]):
        for y in range(f.shape[1]):
            if f[x][y][0] == 255 and f[x][y][1] == 255 and f[x][y][2] == 255 and x > pol_x:
                pol_y = y
                pol_x = x
            if f[x][y][0] == 255 and f[x][y][1] == 255 and f[x][y][2] == 255 and y < zach_y:
                zach_y = y
                zach_x = x

    plt.imsave('{0}4.png'.format(city_name), res_array, cmap=cm.viridis)

    delta_y = abs(s_lng - z_lng)/abs(pol_y-zach_y)
    delta_x = abs(z_lat - s_lat)/abs(pol_x-zach_x)
    print(delta_x, delta_y)
    y21 = s_lng - pol_y * delta_y
    x21 = s_lat + pol_x * delta_x

    file = codecs.open("{0}_kontur.txt".format(city_name), "w", "utf-8")
    for x1 in range(f.shape[0]):
        for y1 in range(f.shape[1]):
            if f[x1][y1][0] == 255:
                file.write("1. BANACHA, Y = {0} X = {1} \n".format((x21 - x1*delta_x), (y21 + y1*delta_y)))
