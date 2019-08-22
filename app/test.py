#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.models import *

nb_rigs = Rigs.query.all()
for on in nb_rigs:
    print(on.online)
