#!/usr/bin/env python
from app import app
from cron import cron

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
    cron()

