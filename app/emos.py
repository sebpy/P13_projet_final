#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module utilisés par EMOS-Live  """

import json
import requests
import datetime

from app.models import *


class Statistics:
    """ Class pour récupérer les éléments de l'api EMOS """

    def __init__(self):
        self.get_stats = ""
        self.annee = "2019"
        self.cfg_block = ""
        self.conf_full = ""
        self.json = ""
        self.show_nbgpu = "1"

    def read_full_conf(self):
        """ Read configuration """

        conf = ConfBlock.query.all()
        items = []
        for cfg in conf:
            items.append({'cfg_nbGpu': cfg.show_nbGpu,
                          'cfg_hashTotal': cfg.show_hashTotal,
                          'cfg_totalpw': cfg.show_totalpw,
                          'cfg_uptime': cfg.show_uptime,
                          'cfg_mineTime': cfg.show_mineTime,
                          'cfg_api_key': cfg.emos_api_key,
                          'cfg_type': cfg.show_type,
                          'cfg_range': cfg.show_range,
                          'first': cfg.first,
                          })

        self.conf_full = items

        return self.conf_full

    def availability_total(self):
        """ Calculation of the availability rate """

        nb_rigs = Rigs.query.count()
        minutes = int(self.conf_full[0]['cfg_range'])  # 30 jours
        total_time = (minutes * nb_rigs)
        real_time = StatsRigs.query.count()
        if not real_time:
            availability = 0
        else:
            availability = round(((real_time / total_time) * 100), 2)

        return availability

    @staticmethod
    def read_stats():
        """ Read rigs statistiques """
        stats_gpu = StatsRigs.query.all()
        return stats_gpu

    def get_status(self, datas):
        """ Récupére les statistique de l'api EMOS """

        date = datetime.datetime.now()
        self.annee = date.year
        get_stats = "https://rigcenter.easy-mining-os.com/api/" + datas[0]["cfg_api_key"]
        response = requests.get(get_stats)
        result = json.loads(response.text)

        items = []
        for cfg in datas:
            items.append({'cfg_nbGpu': cfg["cfg_nbGpu"],
                          'cfg_hashTotal': cfg["cfg_hashTotal"],
                          'cfg_totalpw': cfg["cfg_totalpw"],
                          'cfg_uptime': cfg["cfg_uptime"],
                          'cfg_mineTime': cfg["cfg_mineTime"],
                          })

        self.get_stats = result
        if self.get_stats != "":

            #try:
            #    self.get_stats = result[0]['NomRig']
            #except KeyError:
            #    return "Pas de rigs existant"
            self.json = {'stats': self.get_stats, 'cfg': items, 'availability': self.availability_total()}

            return self.json

        else:
            return 'Pas de rigs existant'

    @staticmethod
    def list_rigs(data):
        """ Verifie si l'id du rig est deja en base de donnée et l'ajoute s'il n'existe pas """

        contents = Rigs.query.all()
        for (k, v) in data['stats'].items():
            mac_rig = v['mac'][5:].replace(':', '')  # generate rig_id
            if not contents:
                rig = Rigs(v['nom_rig'], mac_rig, v['nb_gpu'], v['type_gpu'],
                           v['total_hash'], v['total_pw'], v['uptime'], v['mine_time'])

                db.session.add(rig)
                db.session.commit()
                #print('Record was successfully added')

            else:
                idrig_exist = Rigs.query.filter(Rigs.idRig == mac_rig).count()
                if not idrig_exist:
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
    #st.delete_old_stats()
    read = st.read_full_conf()
    st.availability_total()

