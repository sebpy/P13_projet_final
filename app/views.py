#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, redirect, url_for, flash, request, session, abort, Response
from flask_moment import Moment
from werkzeug.security import check_password_hash

from flask_login import LoginManager, login_required, login_user, logout_user

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)

from app.emos import Statistics
from app.models import User
from app.save_config import SaveConfig


@app.route('/')
@app.route('/index')
@login_required
def index():
    stat = Statistics()
    read = stat.read_full_conf()
    type = read[0]["cfg_type"]

    #if read[0]['first'] == "0":
    #    flash('Pour activer EMOS LIVE, veuillez entré votre clé privé dans la page de configuration.')

    return render_template('pages/index.html', type=type)


@app.route('/error')
def error():
    return render_template('errors/404.html')


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/config')
@login_required
def config():
    stat = Statistics()
    show_cfg = stat.read_full_conf()
    nbgpu = ""
    minetime = ""
    uptime = ""
    pwtotal = ""
    hashtotal = ""
    api_key = ""
    type = ""
    day = ""

    for cfgs in show_cfg:
        if cfgs["cfg_nb_gpu"] == "1":
            nbgpu = "checked"
        if cfgs["cfg_mine_time"] == "1":
            minetime = "checked"
        if cfgs["cfg_uptime"] == "1":
            uptime = "checked"
        if cfgs["cfg_total_pw"] == "1":
            pwtotal = "checked"
        if cfgs["cfg_total_hash"] == "1":
            hashtotal = "checked"

        type = cfgs["cfg_type"]
        api_key = cfgs["cfg_api_key"]
        day = cfgs["cfg_range"]

    return render_template('pages/config.html',
                           nbgpu=nbgpu,
                           minetime=minetime,
                           uptime=uptime,
                           pwtotal=pwtotal,
                           hashtotal=hashtotal,
                           API_KEY=api_key,
                           type=type,
                           day=day)


@app.route('/_answer', methods=['GET'])
def answer():
    api_answer = Statistics()
    cfg_full = api_answer.read_full_conf()
    api_resp = api_answer.show_all_rigs_stats(cfg_full)

    return jsonify(api_resp)


@app.route('/_graph', methods=['GET'])
def graph():
    stats = Statistics()
    stats_pw = stats.graph_pw()

    return jsonify(stats_pw)


@app.route('/_events', methods=['GET'])
def events():
    stats = Statistics()
    events = stats.events_read()

    return jsonify(events)


@app.route("/_save_conf", methods=["GET", "POST"])
def save_conf():

    save = SaveConfig()
    save.save_conf()
    flash('Paramètres enregistré avec succès.')

    return redirect(url_for('config'))


@app.route("/_valid_events", methods=["GET", "POST"])
def discharge():

    update = Statistics()
    update.discharge()
    flash('Notifications acquittés avec succès.')

    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/pages/login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(url_for('index'))


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logout in successfully')
    return render_template('/pages/login.html')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return render_template('/pages/login.html')


# callback to reload the user object
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
