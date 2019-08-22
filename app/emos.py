#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module utilisés par EMOS-Live  """

import json
import requests
from sqlalchemy.sql import func, desc
from datetime import datetime as dt

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
        self.valid_json = ""
        self.stats_gpu = ""
        self.events = ""
        self.now = datetime.datetime.now()

    def read_full_conf(self):
        """ Read configuration """

        conf = ConfBlock.query.all()
        items = []
        for cfg in conf:
            items.append({'cfg_nb_gpu': cfg.show_nb_gpu,
                          'cfg_total_hash': cfg.show_total_hash,
                          'cfg_total_pw': cfg.show_total_pw,
                          'cfg_uptime': cfg.show_uptime,
                          'cfg_mine_time': cfg.show_mine_time,
                          'cfg_api_key': cfg.emos_api_key,
                          'cfg_type': cfg.show_type,
                          'cfg_range': cfg.show_range,
                          'first': cfg.first,
                          })

        self.conf_full = items

        return self.conf_full

    def get_status(self, datas):
        """ Récupére les statistique de l'api EMOS """

        get_stats = "https://rigcenter.easy-mining-os.com/api/" + datas[0]["cfg_api_key"]
        response = requests.get(get_stats)
        result = json.loads(response.text)

        if result != "":
            try:
                self.valid_json = result['0']['nom_rig']
            except KeyError:
                return "Pas de rigs existant"

            self.get_stats = result

            return self.get_stats

        else:
            return 'Pas de rigs existant'

    def list_rigs(self, data):
        """ Verifie si l'id du rig est deja en base de donnée et l'ajoute s'il n'existe pas """

        contents = Rigs.query.all()
        for (k, v) in data.items():
            mac_rig = v['mac'][5:].replace(':', '')  # generate rig_id
            if not contents:
                rig = Rigs(v['nom_rig'], mac_rig, v['nb_gpu'], v['type_gpu'],
                           v['total_hash'], v['total_pw'], v['uptime'], v['mine_time'], v['hash_unit'],
                           v['online'])

                db.session.add(rig)
                db.session.commit()
                #print('Record was successfully added')

            else:
                idrig_exist = Rigs.query.filter(Rigs.id_rig == mac_rig).count()
                if not idrig_exist:
                    for ruche in contents:
                        rig = Rigs(v['nom_rig'], mac_rig, v['nb_gpu'], v['type_gpu'],
                                   v['total_hash'], v['total_pw'], v['uptime'], v['mine_time'], v['hash_unit'],
                                   v['online'])

                        db.session.add(rig)
                        db.session.commit()
                        #print('Record was successfully added')
                else:

                    i = 0
                    for stat in contents:
                        while i < int(v['nb_gpu']):
                            gpu = str(i)
                            stats = StatsRigs(mac_rig, i, v['model_gpu'][gpu], v['hashrate'][gpu],
                                              v['temperature'][gpu], v['fans'][gpu], v['pw'][gpu], v['oc_mem'][gpu],
                                              v['oc_core'][gpu], v['undervolt'][gpu], v['mem_freq'][gpu],
                                              v['core_freq'][gpu], self.now,
                                              datetime.datetime.now().timestamp())

                            db.session.add(stats)
                            db.session.commit()
                            #print('Record was successfully added')
                            i += 1
                            if i == v['nb_gpu']:
                                i = 0

    def update_stats_rig(self, data):
        """ Update status rigs """
        for (k, v) in data.items():
            mac_rig = v['mac'][5:].replace(':', '')  # generate rig_id
            rig = Rigs.query.filter_by(id_rig=mac_rig).first()
            rig.nom_rig = v['nom_rig']
            rig.nb_gpu = v['nb_gpu']
            rig.type_gpu = v['type_gpu']
            rig.total_hash = v['total_hash']
            rig.total_pw = v['total_pw']
            rig.uptime = v['uptime']
            rig.mine_time = v['mine_time']
            rig.hash_unit = v['hash_unit']
            rig.online = v['online']

            db.session.commit()

    def read_stats(self):
        """ Read rigs statistiques """
        self.stats_gpu = StatsRigs.query.all()
        return self.stats_gpu

    def show_all_rigs_stats(self, cfg_data):
        list_of_rig = Rigs.query.all()
        items = []
        for rig in list_of_rig:
            items.append({'nom_rig': rig.nom_rig,
                          'nb_gpu': rig.nb_gpu,
                          'gpu_type': rig.gpu_type,
                          'total_hash': rig.total_hash,
                          'total_pw': rig.total_pw,
                          'uptime': rig.uptime,
                          'mine_time': rig.mine_time,
                          'hash_unit': rig.hash_unit,
                          'online': rig.online,
                          })

        self.json = {'stats': items, 'cfg': cfg_data, 'availability': self.availability_total()}
        return self.json

    def availability_total(self):
        """ Calculation of the availability rate """

        nb_rigs = Rigs.query.count()
        if not nb_rigs:
            availability = 0.00

        else:
            minutes = int(self.conf_full[0]['cfg_range'])  # 30 day
            total_time = (minutes * nb_rigs)  # total minutes for 100%
            real_time = round(StatsRigs.query.count() / nb_rigs, 2)  # total minutes in db
            if not real_time:
                availability = 0.00
            else:
                availability = round(((real_time / total_time) * 100), 2)
        return availability

    def graph_pw(self):
        """ Get stats for graph pw and power """

        qry = db.session.query(func.sum(StatsRigs.pw_gpu).label('total_pw'), StatsRigs.created_date)
        qry = qry.group_by(func.strftime("%Y-%m-%d %H-%m-%s", StatsRigs.created_date))
        items = []
        for res in qry.all():
            items.append({'date': str(res.created_date.replace(microsecond=0)),
                          'total_pw': str(res.total_pw),
                          })
        return items

    def events_save(self, data_json):
        """ Insert in Notifications all events """
        for (k, v) in data_json.items():
            mac_rig = v['mac'][5:].replace(':', '')  # generate rig_id
            if v['online'] == '0':
                event = Notifications(v['nom_rig'], mac_rig, self.now)

                db.session.add(event)
                db.session.commit()

    def events_read(self):
        """ Read all events in Notifications """
        list_of_events = Notifications.query.all()
        items = []
        for eve in list_of_events:
            items.append({'nom_rig': eve.nom_rig,
                          'create_at': eve.created_date,
                          })

        self.events = items
        return self.events

    def delete_old_stats(self):
        """ Delete stats after 30 days """
        secondes = int(self.conf_full[0]['cfg_range']) * 60
        date = int(round(datetime.datetime.now().timestamp()))
        StatsRigs.query.filter(StatsRigs.date_time + secondes < date).delete()  # 259200 // 30 jours
        db.session.commit()
        #stat_gpu = StatsRigs.query.filter(StatsRigs.date_time + 7200 < date).count()
        #print(secondes)


if __name__ == '__main__':
    st = Statistics()
    #st.delete_old_stats()
    read = st.read_full_conf()
    st.availability_total()

