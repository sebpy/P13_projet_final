#!/usr/bin/env python

from app.emos import Statistics

api_answer = Statistics()
cfg_block = api_answer.read_full_conf()
api_resp = api_answer.get_status(cfg_block)
api_answer.list_rigs(api_resp)
api_answer.update_stats_rig(api_resp)
api_answer.events(api_resp)

api_answer.delete_old_stats()
