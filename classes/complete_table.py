import csv
from lxml import etree
with open("../work/done.csv") as csvfile:

    network_dict = csv.DictReader(csvfile, delimiter=";")
    dictionnaire_complet ={}
    for network in network_dict:
        if int(network['nb_nodes']) < 1000 :
                dictionnaire_complet[network['name']]={}
                path_to_file = "../work/files/" + network['number'] + "-" + network['name'] + "/" + network['name']
                tree = etree.parse(path_to_file + "_results.xml")
                results = tree.getroot()
                if results.find("estrada_score") is not None :
                    eplus = str(results.find("estrada_score").find("eplus").get("score"))
                    emoins =str(results.find("estrada_score").find("eminus").get("score"))
                    classe = str(results.find("estrada_score").find("classe").get("score"))
                    print network['name'],";", eplus,";",emoins,";", classe