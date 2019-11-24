#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module utilisés par EMOS-Live  """

import json
import requests
from sqlalchemy.sql import func, desc
from flask import request
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
        self.error = ""

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
                    if v['online'] == '1':
                        i = 0
                        for stat in contents:
                            while i < int(v['nb_gpu']):
                                gpu = str(i)
                                stats = StatsRigs(mac_rig, i, v['model_gpu'][gpu], v['temperature'][gpu],
                                                  v['fans'][gpu], v['hashrate'][gpu], v['pw'][gpu], v['oc_mem'][gpu],
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
        self.availability_save()  # save availability

    def read_stats(self):
        """ Read rigs statistiques """
        self.stats_gpu = StatsRigs.query.all()
        return self.stats_gpu

    def show_all_rigs_stats(self, cfg_data):
        """ Show all stats by rigs """
        list_of_rig = Rigs.query.all()
        availability = Availability.query.order_by(Availability.id.desc()).first()
        items = []
        for rig in list_of_rig:
            items.append({'nom_rig': rig.nom_rig,
                          'id_rig': rig.id_rig,
                          'nb_gpu': rig.nb_gpu,
                          'gpu_type': rig.gpu_type,
                          'total_hash': rig.total_hash,
                          'total_pw': rig.total_pw,
                          'uptime': rig.uptime,
                          'mine_time': rig.mine_time,
                          'hash_unit': rig.hash_unit,
                          'online': rig.online,
                          })

        self.json = {'stats': items, 'cfg': cfg_data, 'availability': str(availability.availability)}
        return self.json

    def availability_save(self):
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

        save_availability = Availability(availability, self.now, datetime.datetime.now().timestamp())

        db.session.add(save_availability)
        db.session.commit()
        #return availability

    @staticmethod
    def availability_total():
        """ Return availability by date """
        qry = db.session.query(Availability.availability, Availability.created_date)
        items = []
        for av in qry.all():
            items.append({'date': str(av.created_date.replace(microsecond=0)),
                          'availability': str(av.availability),
                          })
        return items

    @staticmethod
    def graph_pw():
        """ Get stats for graph pw and power """

        qry = db.session.query(func.sum(StatsRigs.pw_gpu).label('total_pw'), StatsRigs.created_date)
        qry = qry.group_by(func.strftime("%Y-%m-%d %H-%m-%s", StatsRigs.created_date))
        items = []
        for res in qry.all():
            items.append({'date': str(res.created_date.replace(microsecond=0)),
                          'total_pw': str(res.total_pw),
                          })
        return items

    @staticmethod
    def graph_rig(id_rig):
        """ Get stats for graph pw and power """

        qry = db.session.query(func.sum(StatsRigs.pw_gpu).label('total_pw'),
                               func.sum(StatsRigs.hash_gpu).label('total_hash'),
                               func.sum(StatsRigs.fan_gpu).label('total_fan'),
                               func.sum(StatsRigs.temp_gpu).label('total_temp'),
                               StatsRigs.created_date)
        qry = qry.group_by(func.strftime("%Y-%m-%d %H-%m-%s", StatsRigs.created_date))
        items = []
        for res in qry.filter_by(id_rig=id_rig):
            items.append({'total_pw': str(res.total_pw),
                          'total_hash': str(res.total_hash),
                          #'total_fan': str(res.total_fan),
                          #'total_temp': str(res.total_temp),
                          'date': str(res.created_date.replace(microsecond=0)),
                          })
        return items

    def events_save(self, data_json):
        """ Insert in Notifications all events """
        for (k, v) in data_json.items():

            mac_rig = v['mac'][5:].replace(':', '')  # generate rig_id
            if v['online'] == '0':
                off_rig = Notifications.query.filter(Notifications.id_rig == mac_rig,
                                                     Notifications.valid == '0').order_by(Notifications.id.desc()).first()

                if not off_rig:
                    self.events = Notifications(v['nom_rig'], mac_rig, '0', self.now,
                                                datetime.datetime.now().timestamp(), '0')
                    db.session.add(self.events)
                    db.session.commit()

                elif off_rig.event == '1':
                    self.events = Notifications(v['nom_rig'], mac_rig, '0', self.now,
                                                datetime.datetime.now().timestamp(), '0')

                    db.session.add(self.events)
                    db.session.commit()

            if v['online'] == '1':
                rig_up = Notifications.query.filter(Notifications.id_rig == mac_rig,
                                                    Notifications.valid == '0').order_by(Notifications.id.desc()).first()
                if not rig_up:
                    self.events = Notifications(v['nom_rig'], mac_rig, '1', self.now,
                                                datetime.datetime.now().timestamp(), '0')
                    db.session.add(self.events)
                    db.session.commit()
                elif rig_up.event == '0':
                    self.events = Notifications(v['nom_rig'], mac_rig, '1', self.now,
                                                datetime.datetime.now().timestamp(), '0')

                    db.session.add(self.events)
                    db.session.commit()

    def events_read(self):
        """ Read all events in Notifications """
        list_of_events = Notifications.query.filter(Notifications.valid == 0).order_by(desc(Notifications.id)).limit(20)
        total_active_event = Notifications.query.filter(Notifications.valid == 0).count()

        items = []
        for eve in list_of_events:
            items.append({'id': eve.id,
                          'nom_rig': eve.nom_rig,
                          'event': eve.event,
                          'create_at': eve.created_date,
                          })

        self.events = {'events_items': items, 'total_active_event': total_active_event}
        return self.events

    def delete_old_stats(self):
        """ Delete stats after 30 days """
        secondes = int(self.conf_full[0]['cfg_range']) * 60
        date = int(round(datetime.datetime.now().timestamp()))
        StatsRigs.query.filter(StatsRigs.date_time + secondes < date).delete()
        Notifications.query.filter(Notifications.date_time + secondes < date).delete()
        Availability.query.filter(Availability.date_time + secondes < date).delete()

        db.session.commit()
        stat_gpu = StatsRigs.query.filter(StatsRigs.date_time).first()

    def discharge(self):
        """ Discharge all events in list """

        if request.method == "POST":
            valid_events = {'valid': '1'}
            db.session.query(Notifications).update(valid_events)
            db.session.commit()

        else:
            return self.error

    def detail_rig(self, id_rig):
        """ Detail all stats for rig """
        gpu_count = Rigs.query.filter(Rigs.id_rig == id_rig).first()
        stats_rig = StatsRigs.query.filter(StatsRigs.id_rig == id_rig).order_by(desc(StatsRigs.created_date))\
            .limit(gpu_count.nb_gpu)

        hash_unit = ""
        uptime = ""
        active_events = ""
        rig_name = ""
        items = []
        for detail in stats_rig:
            items.append({
                            'id_gpu': detail.id_gpu,
                            'model': detail.model_gpu,
                            'temp': detail.temp_gpu,
                            'fan': detail.fan_gpu,
                            'hash': str(detail.hash_gpu),
                            'pw': str(detail.pw_gpu),
                            'mem_freq': detail.mem_freq,
                            'core_freq': detail.core_freq,
                            'date_create': detail.created_date,
                            'date_time': detail.date_time,
            })
            rig = Rigs.query.filter_by(id_rig=detail.id_rig).first()
            active_events = Notifications.query.filter_by(id_rig=detail.id_rig, valid=0).count()
            rig_name = rig.nom_rig
            hash_unit = rig.hash_unit
            uptime = rig.uptime

        stats = {'stats_rig': items, 'hash_unit': hash_unit, 'uptime': uptime, 'rig_name': rig_name,
                 'event': active_events}
        return stats

    def events_list(self):
        """ List all events """
        list_of_events = Notifications.query.order_by(desc(Notifications.created_date)).all()
        return list_of_events


if __name__ == '__main__':
    st = Statistics()
    #st.delete_old_stats()
    read = st.events_list()
