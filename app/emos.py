#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module utilisés par EMOS-Live  """

import json
import requests
import datetime
import config as cfg

from app.models import *


class Statistics:
    """ Class pour récupérer les éléments de l'api EMOS """

    def __init__(self):
        self.get_stats = ""
        self.annee = "2019"
        self.nb_rigs = "0"
        self.cfg_block = ""
        self.json = ""

        if cfg.API_KEY_EMOS != "":
            pass

    def read_conf(self):
        """ Lis la table conf_block pour afficher les infos ou les cacher """

        conf = ConfBlock.query.all()
        items = []
        for cfgs in conf:
            items.append({'cfg_nbGpu': cfgs.show_nbGpu,
                          'cfg_hashTotal': cfgs.show_hashTotal,
                          'cfg_totalpw': cfgs.show_totalpw,
                          'cfg_uptime': cfgs.show_uptime,
                          'cfg_mineTime': cfgs.show_mineTime
                          })

        self.cfg_block = items
        return self.cfg_block

    def get_status(self, cfg_block):
        """ Récupére les statistique de l'api EMOS """

        date = datetime.datetime.now()
        self.annee = date.year
        get_stats = "https://rigcenter.easy-mining-os.com/api/" + cfg.API_KEY_EMOS
        response = requests.get(get_stats)
        result = json.loads(response.text)

        self.get_stats = result
        if self.get_stats != "":
            #try:
            #    self.get_stats = result[0]['NomRig']
            #except KeyError:
            #    return "Pas de rigs existant"
            self.json = {'stats': self.get_stats, 'cfg': cfg_block}

            return self.json

        else:
            return 'Pas de rigs existant'

    #def count_rig(self, infos):
    #    """ Calcule le nombre de rigs présent """
    #    count_nb_rig = len(infos.items())
    #    self.nb_rigs = count_nb_rig

    #    return self.nb_rigs

    #def total_power(self, data):
    #    """ Additionne la puissance consomé total """
    #    pwt = 0
    #    for (k, v) in data.items():
    #        pwt += float(v['totalpw'])

    #   return round(pwt, 2)

    #def total_hs(self, data):
    #    """ Additionne la puissance consomé total """
    #    hs = 0
    #    for (k, v) in data.items():
    #        if v['enLigne'] == "0":
    #            hs += int(v['enLigne'])

    #    return hs

    def list_rigs(self, data):
        """ Verifie si l'id du rig est deja en base de donnée et l'ajoute s'il n'existe pas """
        contents = Rigs.query.all()
        for (k, v) in data['stats'].items():
            mac_rig = v['macAdresse'][5:].replace(':', '')
            idrig_exist = Rigs.query.filter(Rigs.idRig == mac_rig).count()
            if idrig_exist == 0:
                for ruche in contents:
                    rig = Rigs(v['NomRig'], mac_rig, v['nbGpu'], v['typeGpu'],
                               v['HashTotal'], v['totalpw'], v['uptime'], v['mineTime'])

                    db.session.add(rig)
                    db.session.commit()
                    #print('Record was successfully added')
            else:
                pass


if __name__ == '__main__':
    st = Statistics()
    cfg_block = st.read_conf()
    st.get_status(cfg_block)
    print(st.nb_rigs)

