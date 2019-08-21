#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.models import *


nb_rigs = Notifications.query.count()
print(nb_rigs)
