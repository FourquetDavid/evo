import csv
from lxml import etree
import networkx as nx
from numpy.linalg import eig
import numpy as np
import math
import os


def analysed():
    try:
        tree = etree.parse(path_to_file + "_results.xml")
        return tree.getroot().find("estrada") is not None
    except IOError:
        return False


def add_results_estrada(eplus, eminus, classe):
    print "adding_results", "estrada_score", " e+ ", eplus, " e- ", eminus, " classe ", classe
    if not os.path.isfile(path_to_file + "_results.xml"):
        results = etree.Element('results')
        tree = etree.ElementTree(results)
    else:
        tree = etree.parse(path_to_file + "_results.xml")
        results = tree.getroot()
        try:
            results.remove(results.find("estrada_score"))
        except TypeError:
            pass

    nouvel_element = etree.Element("estrada_score")
    results.append(nouvel_element)
    eplus_element = etree.Element("eplus")
    eplus_element.attrib["score"] = str(eplus)
    nouvel_element.append(eplus_element)
    eminus_element = etree.Element("eplus")
    eminus_element.attrib["score"] = str(eminus)
    nouvel_element.append(eminus_element)
    eminus_element = etree.Element("classe")
    eminus_element.attrib["score"] = str(classe)
    nouvel_element.append(eminus_element)

    f = open(path_to_file + "_results.xml", "w")
    tree.write(f, pretty_print=True)


def mean(liste):
    return sum(liste) / float(len(liste)) if len(liste) > 0 else 0


def write_estrada():
    graphe = nx.read_gexf(path_to_file + ".gexf")
    if type(graphe) == nx.MultiDiGraph:
        print 'has_multiple_edges'
        graphe = nx.DiGraph(graphe)
    if type(graphe) == nx.MultiGraph:
        print 'has_multiple_edges'
        graphe = nx.Graph(graphe)

    adj_mat = nx.to_numpy_matrix(graphe, weight=None)
    adj_mat = adj_mat.tolist()
    w, v = eig(adj_mat)
    argmax = np.argmax(w)
    sh = np.sinh(w)
    square = np.square(v)
    gamma = square[:, argmax]
    gammaideal = np.dot(square, sh) / sh[argmax]
    delta = 0.5 * np.log10(gamma / gammaideal)
    deltaplus = delta[(delta > 0)]
    deltaminus = delta[(delta < 0)]
    eplus = math.sqrt(mean(deltaplus ** 2))
    eminus = math.sqrt(mean(deltaminus ** 2))
    if math.isnan(eplus) or math.isnan(eminus) or eplus == float('inf') or eminus == float('inf'):
        print gamma
        print gammaideal
        print deltaplus
        print deltaminus

    classe = 1
    if eminus > 0.01: classe += 1
    if eplus > 0.01: classe += 2

    add_results_estrada(eplus, eminus, classe)


with open("../work/done.csv") as csvfile:
    network_dict = csv.DictReader(csvfile, delimiter=";")
    numero = 0
    for network in network_dict:
        path_to_file = "../work/files/" + network['number'] + "-" + network['name'] + "/" + network['name']
        if int(network['nb_nodes']) < 1000 and network['is_directed'] == 'False' and 'moreno' in network['name']:
            try:
                print network['name']
                write_estrada()
                print numero
                numero += 1
            except IOError:
                pass
