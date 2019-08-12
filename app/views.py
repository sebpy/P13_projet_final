#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, redirect, url_for
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
    stat.read_conf()

    return render_template('pages/index.html')


@app.route('/error')
def error():
    return render_template('errors/404.html')


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/config')
def config():
    stat = Statistics()
    show_cfg = stat.read_conf()
    nbgpu = ""
    minetime = ""
    uptime = ""
    pwtotal = ""
    hashtotal = ""
    api_key = ""
    type = ""

    for cfgs in show_cfg:
        if cfgs.show_nbGpu == "1":
            nbgpu = "checked"
        if cfgs.show_mineTime == "1":
            minetime = "checked"
        if cfgs.show_uptime == "1":
            uptime = "checked"
        if cfgs.show_totalpw == "1":
            pwtotal = "checked"
        if cfgs.show_hashTotal == "1":
            hashtotal = "checked"
        if cfgs.show_type == "1":
            type = "selected"

        api_key = cfgs.emos_api_key

    return render_template('pages/config.html',
                           nbgpu=nbgpu,
                           minetime=minetime,
                           uptime=uptime,
                           pwtotal=pwtotal,
                           hashtotal=hashtotal,
                           API_KEY=api_key,
                           type=type)


@app.route('/_answer', methods=['GET'])
def answer():
    api_answer = Statistics()
    cfg_block = api_answer.read_conf_block()
    api_resp = api_answer.get_status(cfg_block)

    return jsonify(api_resp)


@app.route("/_save_conf", methods=["GET", "POST"])
def save_conf():

    save = SaveConfig()
    save.save_conf()

    return redirect(url_for('config_save'))
