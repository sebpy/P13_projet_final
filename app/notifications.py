#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from app.models import *

""" Module notifications - EMOS-Live  """


class Events:
    """ save all notifications in db """

    def __init__(self):
        self.nom_rig = ""
        self.date = ""

