#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module utilisés par EMOS-Live  """

import json
import requests
import config as cfg
import datetime

from app.models import *


class Statistics:
    """ Class pour récupérer les éléments de l'api EMOS """

    def __init__(self):
        self.get_stats = ""
        self.annee = "2019"
        self.cfg_block = ""
        self.json = ""
        self.show_nbgpu = "1"

        if cfg.API_KEY_EMOS != "":
            pass

    def read_conf_block(self):
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

    def availability_total(self):
        """ Calculation of the availability rate """

        nb_rigs = Rigs.query.count()
        minutes = 43200  # 30 jours
        total_time = (minutes * nb_rigs)
        real_time = StatsRigs.query.count()
        availability = ((real_time / total_time) * 100)

        return availability

    @staticmethod
    def read_conf():
        """ Read block configuration """
        conf = ConfBlock.query.all()

        return conf

    @staticmethod
    def read_stats():
        """ Read rigs statistiques """
        stats_gpu = StatsRigs.query.all()

        return stats_gpu

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
            self.json = {'stats': self.get_stats, 'cfg': cfg_block, 'availability': round(self.availability_total(),2)}

            return self.json

        else:
            return 'Pas de rigs existant'

    @staticmethod
    def list_rigs(data):
        """ Verifie si l'id du rig est deja en base de donnée et l'ajoute s'il n'existe pas """

        contents = Rigs.query.all()
        for (k, v) in data['stats'].items():
            mac_rig = v['mac'][5:].replace(':', '')
            idrig_exist = Rigs.query.filter(Rigs.idRig == mac_rig).count()
            if idrig_exist == 0:
                for ruche in contents:
                    rig = Rigs(v['nom_rig'], mac_rig, v['nb_gpu'], v['type_gpu'],
                               v['total_hash'], v['total_pw'], v['uptime'], v['mine_time'])

                    db.session.add(rig)
                    db.session.commit()
                    print('Record was successfully added')
            else:
                i = 0
                for stat in contents:
                    while i < int(v['nb_gpu']):
                        gpu = str(i)
                        stats = StatsRigs(mac_rig, v['model_gpu'][gpu], v['hashrate'][gpu], v['temperature'][gpu],
                                          v['fans'][gpu], v['pw'][gpu], v['pw'][gpu], v['oc_mem'][gpu],
                                          v['oc_core'][gpu], v['undervolt'][gpu], v['mem_freq'][gpu],
                                          v['core_freq'][gpu], round(datetime.datetime.now().timestamp()))

                        db.session.add(stats)
                        db.session.commit()
                        i += 1
                        if i == v['nb_gpu']:
                            i = 0

    def delete_old_stats(self):
        """ Delete stats after 30 days """
        date = int(round(datetime.datetime.now().timestamp()))
        StatsRigs.query.filter(StatsRigs.date_time + 259200 < date).delete()  # 259200 // 30 jours
        db.session.commit()
        #stat_gpu = StatsRigs.query.filter(StatsRigs.date_time + 7200 < date).count()
        #print(stat_gpu)


if __name__ == '__main__':
    st = Statistics()


