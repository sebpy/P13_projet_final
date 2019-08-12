#!/usr/bin/env python

from app.emos import Statistics

api_answer = Statistics()
cfg_block = api_answer.read_conf_block()
api_resp = api_answer.get_status(cfg_block)
api_answer.list_rigs(api_resp)

api_answer.delete_old_stats()
