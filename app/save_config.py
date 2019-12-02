#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, flash, Markup
from app.models import *
from werkzeug.security import generate_password_hash

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
        self.error = None
        self.login = ""

    def nb_gpu_chk(self):
        """ Check value nb_gpu """

        nb_gpu = False
        if request.form.get("nbgpu"):
            nb_gpu = True

        if nb_gpu is True:
            self.show_nb_gpu = "1"
        else:
            self.show_nb_gpu = "0"

        return self.show_nb_gpu

    def hash_chk(self):
        """ Check value total_hash """

        total_hash = False
        if request.form.get("hashtotal"):
            total_hash = True
        if total_hash is True:
            self.show_hash = "1"
        else:
            self.show_hash = "0"

        return self.show_hash

    def pw_chk(self):
        """ Check value total_pw """

        total_pw = False
        if request.form.get("pwtotal"):
            total_pw = True

        if total_pw is True:
            self.show_pw = "1"
        else:
            self.show_pw = "0"

        return self.show_pw

    def uptime_chk(self):
        """ Check value uptime """

        uptime = False
        if request.form.get("uptime"):
            uptime = True

        if uptime is True:
            self.show_uptime = "1"
        else:
            self.show_uptime = "0"

        return self.show_uptime

    def mine_time_chk(self):
        """ Check value mine_time """

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
                message = Markup("Vous devez entrer votre clé API...")
                self.error = flash(message, 'danger')

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

    def account_login(self):
        """ Get login name """
        login = User.query.filter(User.id == 1).first()
        self.login = login.username
        return self.login

    def account_save(self):
        """ Update account """

        if request.method == "POST":

            self.login = request.form['login']
            passwd = request.form['passwd']
            passwd2 = request.form['repasswd']

            if self.login == "":
                message = Markup("<strong>Erreur!</strong><br>Vous devez entrer un login")
                self.error = flash(message, 'danger')

            elif not passwd:
                message = Markup("<strong>Erreur!</strong><br>Vous devez entrer un mot de passe")
                self.error = flash(message, 'danger')

            elif len(passwd) < 6:
                message = Markup("<strong>Erreur!</strong><br>Le mot de passe doit contenir 6 caractères minimum")
                self.error = flash(message, 'danger')

            elif passwd != passwd2:
                message = Markup("<strong>Erreur!</strong><br>Les 2 mot de passe ne sont pas identique")
                self.error = flash(message, 'danger')

            else:

                update_account = {'username': self.login,
                                  'password': generate_password_hash(passwd),
                                  }

                db.session.query(User).update(update_account)
                db.session.commit()
                message = Markup('<strong>Succès!</strong><br>Paramètres enregistré avec succès.')
                flash(message, 'success')

        return self.error
