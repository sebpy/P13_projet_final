#!/usr/bin/env python

from app.emos import Statistics

from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()


def cron():
    """ Execute all commands for get stats without browser web open """
    api_answer = Statistics()
    cfg_block = api_answer.read_full_conf()
    api_resp = api_answer.get_status(cfg_block)
    api_answer.events_save(api_resp)
    api_answer.list_rigs(api_resp)
    api_answer.update_stats_rig(api_resp)
    api_answer.delete_old_stats()
    print(cfg_block)


sched.add_job(cron, "interval", seconds=60)
sched.start()
