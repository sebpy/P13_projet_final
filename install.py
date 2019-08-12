#!/usr/bin/env python

from crontab import CronTab

cron = CronTab(user='zelix')
job = cron.new(command='python3 cron.py')
job.minute.every(1)

cron.write()
