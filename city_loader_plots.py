import codecs
import numpy as np
import math
import matplotlib.pyplot as plt
import pickle
from stops_net_preparer import Relation, distance_in_m
from scipy.special import erf
from scipy.optimize import curve_fit
import scipy.stats as stats


def special_function(x, mi, sd, fi):
    return (1 + erf((x - mi) / sd / np.sqrt(2))) / 2 * (1 - np.exp(-fi * x))


def ro(x, mi, sd, fi):
    return np.exp(-(x-mi)**2/(2*sd**2))*(1-np.exp(-fi*x))/(np.sqrt(2*np.pi)*sd)+np.exp(-fi*x)/2*fi*(1 + erf((x - mi) / sd / np.sqrt(2)))


def distance_distribution(city):
    points = []
    for line in enumerate(open('{}_points.txt'.format(city), encoding="utf8")):
        m = line[1].split(",")
        points.append(np.array([float(m[0]), float(m[1])]))

    points = np.array(points)
    relations = []
    for i in range(points.shape[0]):
        for j in range(i + 1, points.shape[0]):
            relations.append(Relation(i, j, distance_in_m(points[i], points[j])))

    relations.sort(reverse=False)
    dist = []
    for rel in relations:
        dist.append(rel.distance)

    empiric_dist = []
    for line in enumerate(open('{}_net.txt'.format(city), encoding="utf8")):
        s_line = line[1].split(";")
        empiric_dist.append(int(s_line[4]))

    empiric_dist.sort(reverse=False)
    #plt.figure(num=0, figsize=(8, 6), dpi=80)
    plt.plot(np.array(dist)/max(dist), np.linspace(0, 1, num=len(dist), endpoint=True), label='Warszawa')
    plt.plot(np.array(empiric_dist)/max(empiric_dist), np.linspace(0, 1, num=len(empiric_dist), endpoint=True), label='Warszawa (empiryczna)')
    x = np.linspace(-2, 3, num=1000, endpoint=True)
    # plt.figure(num=1, figsize=(8, 6), dpi=80)
    sd = 0.8
    mi = 0
    plt.plot((x + 2) / 5, (1 + erf((x - mi) / sd / np.sqrt(2))) / 2, label="dystrybuanta")
    # plt.plot(x, erf(x))
    plt.legend(title=city)
    plt.show()


def experiment(jj, city):
    #porównanie która metoda opisu jest lepsza, dystrybuantą czy gęstością prawdopodobieństwa, wygląda na to że dystrybuantą
    points = []
    for line in enumerate(open('{}_points.txt'.format(city), encoding="utf8")):
        m = line[1].split(",")
        points.append(np.array([float(m[0]), float(m[1])]))

    points = np.array(points)
    relations = []
    for i in range(points.shape[0]):
        for j in range(i + 1, points.shape[0]):
            relations.append(Relation(i, j, distance_in_m(points[i], points[j])))

    relations.sort(reverse=False)
    dist = []
    for rel in relations:
        dist.append(rel.distance)

    dist = np.array(dist) / 1000
    '''
    plt.plot(dist, np.linspace(0, 1, num=len(dist), endpoint=True), label='Warszawa')
    popt, pcov = curve_fit(special_function, dist, np.linspace(0, 1, num=len(dist), endpoint=True))
    print(popt)
    plt.plot(dist, special_function(dist, popt[0], popt[1], popt[2]), label='Warszawa')
    '''
    plt.figure(num=jj, figsize=(8, 6), dpi=80)
    n, bins, patches = plt.hist(dist, bins=32, normed=1, label="Rozkład empiryczny")
    #print(n)
    #print(bins)
    w_bins = []
    for ii in range(len(n)):
        w_bins.append((bins[ii]+bins[ii+1])/2)
    popt, pcov = curve_fit(special_function, dist, np.linspace(0, 1, num=len(dist), endpoint=True))
    popt1, pcov1 = curve_fit(ro, w_bins, n)#[10.62927336  6.98632564  0.20269433]
    #print(popt)
    plt.title("Porównanie dopasowań dla metryki euklidejskiej")
    plt.xlabel("Odległość (km)")
    plt.ylabel("P")
    plt.plot(np.linspace(0, max(dist), num=1000, endpoint=True), ro(np.linspace(0, max(dist), num=1000, endpoint=True), popt[0], popt[1], popt[2]), label="Dopasowanie z dystrybuanty")
    plt.plot(np.linspace(0, max(dist), num=1000, endpoint=True),
             ro(np.linspace(0, max(dist), num=1000, endpoint=True), popt1[0], popt1[1], popt1[2]),
             label="Dopasowanie z gęstości")
    plt.legend(title=city)
    chi2, p, dof, expected = stats.chi2_contingency(np.array([n, ro(np.array(w_bins), popt[0], popt[1], popt[2])]))
    print(city)
    print("Z dystrybuanty, chi^2={0}, dof={1}".format(chi2, dof))
    chi21, p1, dof1, expected1 = stats.chi2_contingency(np.array([n, ro(np.array(w_bins), popt1[0], popt1[1], popt1[2])]))
    print("Z gęstości, chi^2={0}, dof={1}".format(chi21, dof1))


def experiment2(ii, city='warszawa'):
    #badanie transformacji rozkładu z jednej metryki w drugą
    points = []
    for line in enumerate(open('{}_points.txt'.format(city), encoding="utf8")):
        m = line[1].split(",")
        points.append(np.array([float(m[0]), float(m[1])]))

    points = np.array(points)
    relations = []
    for i in range(points.shape[0]):
        for j in range(i + 1, points.shape[0]):
            relations.append(Relation(i, j, distance_in_m(points[i], points[j])))

    relations.sort(reverse=False)
    dist = []
    for rel in relations:
        dist.append(rel.distance)

    dist = np.array(dist) / 1000
    plt.figure(num=0+2*ii, figsize=(8, 6), dpi=80)
    plt.plot(dist, np.linspace(0, 1, num=len(dist), endpoint=True), label='Warszawa')
    popt, pcov = curve_fit(special_function, dist, np.linspace(0, 1, num=len(dist), endpoint=True))
    print(popt)
    plt.plot(dist, special_function(dist, popt[0], popt[1], popt[2]), label='Warszawa')
    plt.title("Dystrybuanta euklidejska {}".format(city))

    empiric_dist = []
    for line in enumerate(open('{}_net.txt'.format(city), encoding="utf8")):
        s_line = line[1].split(";")
        empiric_dist.append(int(s_line[4]))

    empiric_dist.sort(reverse=False)
    empiric_dist = np.array(empiric_dist) / 1000
    plt.figure(num=1+2*ii, figsize=(8, 6), dpi=80)
    plt.title("Dystrybuanta empiryczna {}".format(city))
    plt.xlabel("Odległość (km)")
    plt.ylabel("P")
    plt.plot(empiric_dist, np.linspace(0, 1, num=len(empiric_dist), endpoint=True), label='{} (empiryczna)'.format(city))
    popt1, pcov1 = curve_fit(special_function, empiric_dist, np.linspace(0, 1, num=len(empiric_dist), endpoint=True))
    print(popt1)
    plt.plot(empiric_dist, special_function(empiric_dist, popt1[0], popt1[1], popt1[2]), label=city)
    print("{0} - delta_mi={1}%, delta_std={2}%".format(city, round(np.abs(popt1[0] - popt[0])/popt[0]*100, 2), round(np.abs(popt1[1] - popt[1])/popt[1]*100, 2))) #dmi = 59,42%, dsd = 32,76%


def experiment3():
    #to samo tylko dla danych z przystanków
    stops = []
    for line in enumerate(open('RA180310_centered_stops_final.txt', encoding="utf8")):
        m = line[1].split(" ")
        stops.append(np.array([float(m[len(m) - 5]), float(m[len(m) - 2])]))

    stops = np.array(stops)
    relations = []
    for i in range(stops.shape[0]):
        for j in range(i + 1, stops.shape[0]):
            relations.append(Relation(i, j, distance_in_m(stops[i], stops[j])))

    relations.sort(reverse=False)
    dist = []
    for rel in relations:
        dist.append(rel.distance)

    dist = np.array(dist) / 1000
    plt.figure(num=0, figsize=(8, 6), dpi=80)
    plt.plot(dist, np.linspace(0, 1, num=len(dist), endpoint=True), label='Warszawa')
    popt, pcov = curve_fit(special_function, dist, np.linspace(0, 1, num=len(dist), endpoint=True))
    print(popt)
    plt.plot(dist, special_function(dist, popt[0], popt[1], popt[2]), label='Warszawa')

    empiric_dist = []
    for line in enumerate(open('net.txt', encoding="utf8")):
        s_line = line[1].split(";")
        empiric_dist.append(int(s_line[4]))

    empiric_dist.sort(reverse=False)
    empiric_dist = np.array(empiric_dist) / 1000
    plt.figure(num=1, figsize=(8, 6), dpi=80)
    plt.title("Dystrybuanta empiryczna Warszawa (przystanki)")
    plt.plot(empiric_dist, np.linspace(0, 1, num=len(empiric_dist), endpoint=True), label='Warszawa (empiryczna)')
    plt.xlabel("Odległość (km)")
    plt.ylabel("P")
    popt1, pcov1 = curve_fit(special_function, empiric_dist, np.linspace(0, 1, num=len(empiric_dist), endpoint=True))
    print(popt1)
    plt.plot(empiric_dist, special_function(empiric_dist, popt1[0], popt1[1], popt1[2]), label='Warszawa')
    print("{0} - delta_mi={1}%, delta_std={2}%".format("Warszawa (przystanki)", round(np.abs(popt1[0] - popt[0]) / popt[0] * 100, 2),
                                                       round(np.abs(popt1[1] - popt[1]) / popt[1] * 100, 2)))# 52%, 41,22%


if __name__ == "__main__":
    #distance_distribution('warszawa')
    #for ii, city_name in enumerate(['warszawa', 'krakow', 'wroclaw', 'lublin', 'olsztyn']):
    #    experiment2(ii, city_name)
    experiment3()
    plt.show()
