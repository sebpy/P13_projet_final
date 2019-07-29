#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module utilisés par EMOS-Monitor  """

import json
import jsonify
import requests
from config import API_KEY_EMOS


class Statistics:
    """ Class pour récupérer les éléments de l'api EMOS """

    def __init__(self):
        self.get_stats = ""
        self.nb_rigs = 0
        self.infos_use = ""
        self.nom_rig = ""
        self.hash_total_rig = ""
        self.power_total_rig = ""
        self.nb_gpu_rig = 0
        self.gpu_type_rig = ""
        self.hash_unit_rig = ""
        self.uptime_rig = 0
        self.uptime_miner_rig = ""
        self.stats_rigs = {}

        if API_KEY_EMOS != "":
            pass

    def get_status(self):
        """ Récupére les statistique de l'api EMOS """

        get_stats = "https://rigcenter.easy-mining-os.com/api/" + API_KEY_EMOS
        response = requests.get(get_stats)
        result = json.loads(response.text)

        self.get_stats = result
        if self.get_stats != "":
            #try:
            #    self.get_stats = result['0']
            #except KeyError:
            #    return "Pas de rigs existant"
            return self.get_stats
        else:
            return 'Pas de rigs existant'

    def count_rig(self, infos):
        """ Calcule le nombre de rigs présent """
        count_nb_rig = len(infos.items())
        self.nb_rigs = count_nb_rig

        return self.nb_rigs

    def select_infos(self, infos):
        """ Séléction des infos à afficher """

        for valeur in infos.values():
            pass
            #valeur['HashTotal'].append(valeur['HashTotal'])

            #self.hash_unit_rig = valeur['hashUnit']
            #self.power_total_rig = valeur['totalpw']
            #self.nb_gpu_rig = valeur['nbGpu']
            #self.gpu_type_rig = valeur['typeGpu']
            #self.uptime_rig = valeur['uptime']
            #self.uptime_miner_rig = valeur['mineTime'


if __name__ == '__main__':
    st = Statistics()
    st.get_status()
    st.count_rig(st.get_stats)
    st.select_infos(st.get_stats)
