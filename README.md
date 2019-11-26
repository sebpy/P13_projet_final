# Project 13: Final Project

## What is EMOS-Live?
EMOS-Live is a monitoring application developed in python.
It allows to display in real time the data of its mining drilling by the site easy-mining-os.com

## Prerequisites

- Python 3.6
- Flask
- Sqlite database
- nginx
- All the other required modules are in the requirements.txt file to install before launching the app.


## How to install

# Update your local package index and then install the packages by typing:
```
sudo apt-get update
sudo apt-get install python-pip python-dev nginx sqlite3
```

# Create a Python Virtual Environment

Next, we’ll set up a virtual environment in order to isolate our Flask application from the other Python files on the system.
Start by installing the virtualenv package using pip:
```
sudo pip install virtualenv
```

Clone or download the project.
(VirtualEnv is recommended to install the requirements)
```bash
cd "P13_projet_final"
pip install -r requirements.txt
```

## Configuring Nginx to Proxy Requests

## Cronjob
Run the crontab -e command and add the following line:
```
* * * * * python3 /home/{USERNAME}/PycharmProjects/emos-monitoring/cron.py > /dev/null 2>&1
```

## First connexion
Log on to the address http://{your_ip}:8080 and enter the following login and password:
```
Login: admin
Password: emoslive
```

## Configuration
Click on the button with login at the top right then select parameter.
Enter your EMOS API key in the "API Key" field and save

Wait a few seconds and your rig information will appear.
