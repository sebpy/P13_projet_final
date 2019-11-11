#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, redirect, url_for, flash
from flask_moment import Moment

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

from app.emos import Statistics
from app.save_config import SaveConfig


@app.route('/')
@app.route('/index')
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