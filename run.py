#!/usr/bin/env python
from app import app
from cron import cron
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

    @sched.scheduled_job('interval', minutes=2)
    def timed_job():
        cron()
