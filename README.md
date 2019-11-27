# Project 13: Final Project

## What is EMOS-Live?
EMOS-Live is a monitoring application developed in python.
It allows to display in real time the data of its mining drilling by the site easy-mining-os.com

## Prerequisites

- Python 3 last
- Flask last
- Sqlite3 last
- nginx last
- All the other required modules are in the requirements.txt file to install before launching the app.


## How to install

# Update your local package index and then install the packages by typing:
```
sudo apt update && sudo apt upgrade
sudo apt install python3 python3-pip python3-dev nginx sqlite3 supervisor -y
```

# Create a Python Virtual Environment

Next, we’ll set up a virtual environment in order to isolate our Flask application from the other Python files on the system.
Start by installing the virtualenv package using pip:
```
pip3 install virtualenv
cd "P13_projet_final"
virtualenv venv
source venv/bin/activate
```

Clone or download the project.
VirtualEnv is recommended to install the requirements
(you have to use the sudo command with pip3 to install the requieremets so you do not have problems with the cron job)
```bash
sudo mv P13_projet_final emoslive
cd "emoslive"
sudo pip3 install -r requirements.txt
```

## Configuring Nginx to Proxy Requests

#Create a new configuration file
```bash
sudo nano /etc/nginx/sites-enabled/emoslive
```

Then add the informations below

```bash
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /home/zelix25/emoslive;

        server_name {raspeberry_ip};

        location / {
            try_files $uri @wsgi;
        }

        location @wsgi {
            proxy_pass http://0.0.0.0:8080;
            proxy_set_header   Host             $host;
            proxy_set_header   X-Real-IP        $remote_addr;
            proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Proto $scheme;
        }

        location ~* .(ogg|ogv|svg|svgz|eot|otf|woff|mp4|ttf|css|rss|atom|js|jpg|                                                                                                                                                             jpeg|gif|png|ico|zip|tgz|gz|rar|bz2|doc|xls|exe|ppt|tar|mid|midi|wav|bmp|rtf)$ {
            access_log off;
            log_not_found off;
            expires max;
        }
}

```

## Cronjob
Run the crontab -e command and add the following line:
```bash
*\2 * * * * python3 /home/{USERNAME}/emoslive/cron.py > /dev/null 2>&1
```

## Configure Supervisor
# Create configuration file
```bash
sudo nano /etc/supervisor/conf.d/emoslive.conf
``` 
Then add the information below
```bash
[program:emoslive-gunicorn]

command = /home/{user_name}/emoslive/venv/bin/gunicorn --bind 0.0.0.0:8080 app:app
directory = /home/{user_name}/emoslive
user = root
autostart = true
autorestart = true
stderr_logfile = /var/log/emoslive.err.log
stdout_logfile = /var/log/emoslive.out.log

``` 
Then you have to re-read the configuration and then load it 
```bash
sudo supervisorctl reread
sudo supervisorctl reload
```

then to finish 
```bash
sudo supervisorctl status
```
You must obtain (ex.)
```bash
emoslive-gunicorn                RUNNING   pid 13322, uptime 0:00:10 
```

## First connexion
Log on to the address http://{your_ip} and enter the following login and password:
```bash
Login: admin
Password: emoslive
```

## Configuration
Click on the button with login at the top right then select parameter.
Enter your EMOS API key in the "API Key" field and save

Wait a few seconds and your rig information will appear.
