#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify
from flask_moment import Moment

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

from app.emos import Statistics


@app.route('/')
@app.route('/index')
def index():
    stat = Statistics()
    cfg_block = stat.read_conf()
    info = stat.get_status(cfg_block)
    #rig_nb = stat.count_rig(info)
    #pw_total = stat.total_power(info)
    #hs_total = stat.total_hs(info)
    stat.read_conf()
    #rig = stat.list_rigs()

    return render_template('pages/index.html')


@app.route('/error')
def error():
    return render_template('errors/404.html')


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/_answer', methods=['GET'])
def answer():
    api_answer = Statistics()
    cfg_block = api_answer.read_conf()
    api_resp = api_answer.get_status(cfg_block)
    api_answer.list_rigs(api_resp)
    #api_answer.count_rig(api_answer.get_stats)
    #api_resp = api_answer.select_infos(api_answer.get_stats)

    return jsonify(api_resp)


