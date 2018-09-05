import pickle
import matplotlib.pyplot as plt
import numpy as np
from city_loader import normalize


def histogram_p(city):
    x_array = pickle.load(open('perkolacja_czasowa/x_array_{}.p'.format(city), 'rb'))
    y_array = pickle.load(open('perkolacja_czasowa/y_array_{}.p'.format(city), 'rb'))
    plt.plot(x_array, y_array)
    plt.show()


def histogram_of_mean_velocity():

    pass


def histogram_of_duration_distribution(junctions):
    pass


def all_cities_percolation_histogram():
    x_array = pickle.load(open('perkolacja_czasowa/x_array_olsztyn.p', 'rb'))
    y_array = pickle.load(open('perkolacja_czasowa/y_array_olsztyn.p', 'rb'))
    x2_array = pickle.load(open('perkolacja_czasowa/x_array_lublin.p', 'rb'))
    y2_array = pickle.load(open('perkolacja_czasowa/y_array_lublin.p', 'rb'))
    x3_array = pickle.load(open('perkolacja_czasowa/x_array_wroclaw.p', 'rb'))
    y3_array = pickle.load(open('perkolacja_czasowa/y_array_wroclaw.p', 'rb'))
    x4_array = pickle.load(open('perkolacja_czasowa/x_array_krakow.p', 'rb'))
    y4_array = pickle.load(open('perkolacja_czasowa/y_array_krakow.p', 'rb'))
    x5_array = pickle.load(open('perkolacja_czasowa/x_array_warszawa.p', 'rb'))
    y5_array = pickle.load(open('perkolacja_czasowa/y_array_warszawa.p', 'rb'))
    x6_array = pickle.load(open('perkolacja_czasowa/x_array_warszawa_stops.p', 'rb'))
    y6_array = pickle.load(open('perkolacja_czasowa/y_array_warszawa_stops.p', 'rb'))
    plt.figure(num=0, figsize=(8, 6), dpi=80)
    plt.plot(x_array, y_array, label="Olsztyn")
    plt.plot(x2_array, y2_array, label="Lublin")
    plt.plot(x3_array, y3_array, label="Wrocław")
    plt.plot(x4_array, y4_array, label="Kraków")
    plt.plot(x5_array, y5_array, label="Warszawa")
    plt.plot(x6_array, y6_array, label="Warszawa(przystanki)")
    plt.legend(title='Miasto')
    plt.title("Wykres perkolacyjnej przemiany fazowej")
    plt.xlabel("t(s)")
    plt.ylabel("Rozmiar największego klastra dzielony na rozmiar sieci")
    plt.axis((0, 420, 0, 1.05))
    plt.show()


def all_cities_percolation2_histogram():
    x_array = pickle.load(open('perkolacja_czasowa2/x_array_olsztyn.p', 'rb'))
    y_array = pickle.load(open('perkolacja_czasowa2/y_array_olsztyn.p', 'rb'))
    x2_array = pickle.load(open('perkolacja_czasowa2/x_array_lublin.p', 'rb'))
    y2_array = pickle.load(open('perkolacja_czasowa2/y_array_lublin.p', 'rb'))
    x3_array = pickle.load(open('perkolacja_czasowa2/x_array_wroclaw.p', 'rb'))
    y3_array = pickle.load(open('perkolacja_czasowa2/y_array_wroclaw.p', 'rb'))
    x4_array = pickle.load(open('perkolacja_czasowa2/x_array_krakow.p', 'rb'))
    y4_array = pickle.load(open('perkolacja_czasowa2/y_array_krakow.p', 'rb'))
    x5_array = pickle.load(open('perkolacja_czasowa2/x_array_warszawa.p', 'rb'))
    y5_array = pickle.load(open('perkolacja_czasowa2/y_array_warszawa.p', 'rb'))
    x6_array = pickle.load(open('perkolacja_czasowa/x_array_warszawa_stops.p', 'rb'))
    y6_array = pickle.load(open('perkolacja_czasowa/y_array_warszawa_stops.p', 'rb'))
    plt.figure(num=0, figsize=(8, 6), dpi=80)
    plt.plot(x_array, y_array, label="Olsztyn")
    plt.plot(x2_array, y2_array, label="Lublin")
    plt.plot(x3_array, y3_array, label="Wrocław")
    plt.plot(x4_array, y4_array, label="Kraków")
    plt.plot(x5_array, y5_array, label="Warszawa")
    plt.plot(x6_array, y6_array, label="Warszawa(przystanki)")
    plt.legend(title='Miasto')
    plt.title("Wykres perkolacyjnej przemiany fazowej")
    plt.xlabel("t(s)")
    plt.ylabel("Rozmiar największego klastra dzielony na rozmiar sieci")
    plt.axis((0, 350, 0, 1.05))
    plt.show()


def all_cities_duration_distribution():
    x_array = pickle.load(open('duration_distribution/x_array_olsztyn.p', 'rb'))
    y_array = pickle.load(open('duration_distribution/y_array_olsztyn.p', 'rb'))
    x2_array = pickle.load(open('duration_distribution/x_array_lublin.p', 'rb'))
    y2_array = pickle.load(open('duration_distribution/y_array_lublin.p', 'rb'))
    x3_array = pickle.load(open('duration_distribution/x_array_wroclaw.p', 'rb'))
    y3_array = pickle.load(open('duration_distribution/y_array_wroclaw.p', 'rb'))
    x4_array = pickle.load(open('duration_distribution/x_array_krakow.p', 'rb'))
    y4_array = pickle.load(open('duration_distribution/y_array_krakow.p', 'rb'))
    x5_array = pickle.load(open('duration_distribution/x_array_warszawa.p', 'rb'))
    y5_array = pickle.load(open('duration_distribution/y_array_warszawa.p', 'rb'))
    x6_array = pickle.load(open('duration_distribution/x_array_warszawa_stops.p', 'rb'))
    y6_array = pickle.load(open('duration_distribution/y_array_warszawa_stops.p', 'rb'))
    plt.figure(num=0, figsize=(8, 6), dpi=80)
    plt.plot(x_array, y_array, label="Olsztyn")
    plt.plot(x2_array, y2_array, label="Lublin")
    plt.plot(x3_array, y3_array, label="Wrocław")
    plt.plot(x4_array, y4_array, label="Kraków")
    plt.plot(x5_array, y5_array, label="Warszawa")
    plt.plot(x6_array, y6_array, label="Warszawa(przystanki)")
    plt.legend(title='Miasto')
    plt.title("Wykres dystrybuanty czasowej")
    plt.xlabel("t(s)")
    plt.ylabel("Dystrybuanta")
    plt.axis((0, 3000, 0, 1.05))
    plt.show()


def all_cities_duration_distribution2():
    x_array = pickle.load(open('duration_distribution2/x_array_olsztyn.p', 'rb'))
    y_array = pickle.load(open('duration_distribution2/y_array_olsztyn.p', 'rb'))
    x2_array = pickle.load(open('duration_distribution2/x_array_lublin.p', 'rb'))
    y2_array = pickle.load(open('duration_distribution2/y_array_lublin.p', 'rb'))
    x3_array = pickle.load(open('duration_distribution2/x_array_wroclaw.p', 'rb'))
    y3_array = pickle.load(open('duration_distribution2/y_array_wroclaw.p', 'rb'))
    x4_array = pickle.load(open('duration_distribution2/x_array_krakow.p', 'rb'))
    y4_array = pickle.load(open('duration_distribution2/y_array_krakow.p', 'rb'))
    x5_array = pickle.load(open('duration_distribution2/x_array_warszawa.p', 'rb'))
    y5_array = pickle.load(open('duration_distribution2/y_array_warszawa.p', 'rb'))
    x6_array = pickle.load(open('duration_distribution/x_array_warszawa_stops.p', 'rb'))
    y6_array = pickle.load(open('duration_distribution/y_array_warszawa_stops.p', 'rb'))
    plt.figure(num=0, figsize=(8, 6), dpi=80)
    plt.plot(x_array, y_array, label="Olsztyn")
    plt.plot(x2_array, y2_array, label="Lublin")
    plt.plot(x3_array, y3_array, label="Wrocław")
    plt.plot(x4_array, y4_array, label="Kraków")
    plt.plot(x5_array, y5_array, label="Warszawa")
    plt.plot(x6_array, y6_array, label="Warszawa(przystanki)")
    plt.legend(title='Miasto')
    plt.title("Wykres dystrybuanty czasowej po redukcji")
    plt.xlabel("t(s)")
    plt.ylabel("Dystrybuanta")
    plt.axis((0, 3000, 0, 1.05))
    plt.show()


def two():
    x = pickle.load(open('mean_velocity/x_array_warszawa.p', 'rb'))
    y = pickle.load(open('mean_velocity/x_array_warszawa_stops.p', 'rb'))

    bins = np.linspace(2, 25, 100)

    plt.hist(x, bins, label="Siatka kwadratowa", alpha=0.5, normed=1)
    plt.hist(y, bins, label="Przystanki", alpha=0.5, normed=1)
    plt.legend(title='Warszawa')
    plt.title("Histogram prędkości połączeń w Warszawie")
    plt.xlabel("v(m/s)")
    plt.show()


def all():
    x = pickle.load(open('mean_velocity/x_array_olsztyn.p', 'rb'))
    x2 = pickle.load(open('mean_velocity/x_array_lublin.p', 'rb'))
    x3 = pickle.load(open('mean_velocity/x_array_wroclaw.p', 'rb'))
    x4 = pickle.load(open('mean_velocity/x_array_krakow.p', 'rb'))
    x5 = pickle.load(open('mean_velocity/x_array_warszawa.p', 'rb'))
    x6 = pickle.load(open('mean_velocity/x_array_warszawa_stops.p', 'rb'))

    bins = np.linspace(2, 25, 100)

    plt.hist(x, bins, label="Olsztyn", alpha=0.5, normed=1)
    plt.hist(x2, bins, label="Lublin", alpha=0.5, normed=1)
    plt.hist(x3, bins, label="Wrocław", alpha=0.5, normed=1)
    plt.hist(x4, bins, label="Kraków", alpha=0.5, normed=1)
    plt.hist(x5, bins, label="Warszawa", alpha=0.5, normed=1)
    plt.hist(x6, bins, label="Warszawa(przystanki)", alpha=0.5, normed=1)
    plt.legend(title='Miasta')
    plt.title("Histogram prędkości połączeń")
    plt.xlabel("v(m/s)")
    plt.show()


def histogram_a_a(city):
    x_array = pickle.load(open('histogram_a/x_array_{}.p'.format(city), 'rb'))
    y_array = normalize(pickle.load(open('histogram_a/y_array_{}.p'.format(city), 'rb')))
    x_array_stops = pickle.load(open('histogram_a/x_array_{}_stops.p'.format(city), 'rb'))
    y_array_stops = normalize(pickle.load(open('histogram_a/y_array_{}_stops.p'.format(city), 'rb')))
    plt.plot(x_array, y_array, label="Warszawa(siatka)")
    plt.plot(x_array_stops, y_array_stops, label="Warszawa(przystanki)")
    plt.title("Histogram manewrów przed redukcją")
    plt.xlabel("Ilość manewrów")
    plt.legend(title='Miasta')
    plt.show()


def histogram_a(city):
    x_array = pickle.load(open('histogram_a/x_array_{}.p'.format(city), 'rb'))
    y_array = normalize(pickle.load(open('histogram_a/y_array_{}.p'.format(city), 'rb')))
    plt.plot(x_array, y_array)
    plt.show()
