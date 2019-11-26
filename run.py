#!/usr/bin/env python
from app import app
from app . emos import Statistics
import time

def cron():
    """ Execute all commands for get stats without browser web open """
    api_answer = Statistics()
    cfg_block = api_answer.read_full_conf()
    api_resp = api_answer.get_status(cfg_block)
    api_answer.events_save(api_resp)
    api_answer.list_rigs(api_resp)
    api_answer.update_stats_rig(api_resp)
    api_answer.delete_old_stats()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

    try:
        while True:
            cron()
            time.sleep(60)
            print('wait 60 sec')
    except (KeyboardInterrupt, SystemExit):
        print('Error!')