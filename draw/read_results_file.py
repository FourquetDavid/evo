import csv
from lxml import etree



with open("../work/done.csv") as csvfile:

    network_dict = csv.DictReader(csvfile, delimiter=";")
    for network in network_dict:
        try :

            path_to_file = "../work/files/" + network['number'] + "-" + network['name'] + "/" + network['name']
            tree = etree.parse(path_to_file + "_results.xml")
            results = tree.getroot()

            if results.find("motifs") is not None and results.find("estrada_score") is not None :
                print network['name']
            #print(etree.tostring(results.find("motifs"), pretty_print=True))

            #print(etree.tostring(results.find("estrada_score"), pretty_print=True))
        except  :
            pass