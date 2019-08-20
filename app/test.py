#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
from sqlalchemy.sql import func, desc
from datetime import datetime as dt

from app.models import *


def get_status():
    """ Récupére les statistique de l'api EMOS """

    list_of_rig = Rigs.query.all()
    print(list_of_rig[0].nom_rig)


if __name__ == '__main__':
    get_status()






