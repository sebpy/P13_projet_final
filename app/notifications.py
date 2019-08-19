#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from app.models import *

""" Module notifications - EMOS-Live  """


class Events:
    """ save all notifications in db """

    def __init__(self):
        self.nom_rig = "EM-TEST"
        self.date = ""

    def save_event(self):
        event = Notifications(self.nom_rig, datetime.datetime.now())

        db.session.add(event)
        db.session.commit()

    def read(self):
        ev = StatsRigs.query.first()
        print(ev.created_date)


if __name__ == '__main__':
    ev = Events()
    ev.save_event()
    ev.read()

