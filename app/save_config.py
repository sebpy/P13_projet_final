#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from app.models import *

""" Save configuration - EMOS-Live  """


class SaveConfig:
    """ save all parameters """

    def __init__(self):
        self.show_nb_gpu = "1"
        self.show_hash = "1"
        self.show_pw = "1"
        self.show_uptime = "1"
        self.show_mine_time = "0"
        self.emos_api_key = ""
        self.show_type = "0"
        self.show_range = ""
        self.error = ""

    def nb_gpu_chk(self):
        """"""

        nb_gpu = False
        if request.form.get("nbgpu"):
            nb_gpu = True

        if nb_gpu is True:
            self.show_nb_gpu = "1"
        else:
            self.show_nb_gpu = "0"

        return self.show_nb_gpu

    def hash_chk(self):
        """"""

        total_hash = False
        if request.form.get("hashtotal"):
            total_hash = True
        if total_hash is True:
            self.show_hash = "1"
        else:
            self.show_hash = "0"

        return self.show_hash

    def pw_chk(self):
        """"""

        total_pw = False
        if request.form.get("pwtotal"):
            total_pw = True

        if total_pw is True:
            self.show_pw = "1"
        else:
            self.show_pw = "0"

        return self.show_pw

    def uptime_chk(self):
        """"""

        uptime = False
        if request.form.get("uptime"):
            uptime = True

        if uptime is True:
            self.show_uptime = "1"
        else:
            self.show_uptime = "0"

        return self.show_uptime

    def mine_time_chk(self):
        """"""

        mine_time = False
        if request.form.get("minetime"):
            mine_time = True

        if mine_time is True:
            self.show_mine_time = "1"
        else:
            self.show_mine_time = "0"

        return self.show_mine_time

    def save_conf(self):
        """ Function save config """

        if request.method == "POST":

            self.nb_gpu_chk()
            self.hash_chk()
            self.pw_chk()
            self.uptime_chk()
            self.mine_time_chk()

            self.emos_api_key = request.form['api_key']

            if self.emos_api_key == "":
                self.error = "Vous devez entrer votre clé API..."

            self.show_type = request.form['type']
            self.show_range = request.form['range']

            update_cfg = {'show_nb_gpu': self.show_nb_gpu,
                          'show_total_hash': self.show_hash,
                          'show_total_pw': self.show_pw,
                          'show_uptime': self.show_uptime,
                          'show_mine_time': self.show_mine_time,
                          'emos_api_key': self.emos_api_key,
                          'show_type': self.show_type,
                          'show_range': self.show_range,
                          }

            db.session.query(ConfBlock).update(update_cfg)
            db.session.commit()

        return self.error
