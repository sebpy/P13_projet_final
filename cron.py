#!/usr/bin/env python

from app.emos import Statistics


def cron():
    """ Execute all commands for get stats without browser web open"""
    api_answer = Statistics()
    cfg_block = api_answer.read_full_conf()
    api_resp = api_answer.get_status(cfg_block)
    api_answer.events_save(api_resp)
    api_answer.list_rigs(api_resp)
    api_answer.update_stats_rig(api_resp)

    api_answer.delete_old_stats()


if __name__ == "__main__":
    cron()
