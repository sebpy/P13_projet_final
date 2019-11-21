# Project 13: Final Project

## What is EMOS-Live?
EMOS-Live is a monitoring application developed in python.
It allows to display in real time the data of its mining drilling by the site easy-mining-os.com

## Prerequisites

- Python 3.6
- Flask
- Sqlite database
- All the other required modules are in the requirements.txt file to install before launching the app.


## How to install

First clone or download the project.
(VirtualEnv is recommended to install the requirements)
```bash
$ cd "project/folder"
$ pip install -r requirements.txt
```
## Cronjob
Run the crontab -e command and add the following line:
```
* * * * * python3 /home/zelix/PycharmProjects/emos-monitoring/cron.py > /dev/null 2>&1
```

## First connexion
Log on to the address 127.0.0.1:8080 and enter the following login and password:
```
Login: admin
Password: emoslive
```

## Configuration
Click on the button with login at the top right then select parameter.
Enter your EMOS API key in the "API Key" field and save

Wait a few seconds and your rig information will appear.
