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
    info = stat.get_status()
    rig_nb = stat.count_rig(info)
    pw_total = stat.total_power(info)
    hs_total = stat.total_hs(info)
    #rig = stat.list_rigs()

    return render_template('pages/index.html', nb_rig=rig_nb, pw_total=pw_total, hs_total=hs_total)


@app.route('/error')
def error():
    return render_template('errors/404.html')


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/_answer', methods=['GET'])
def answer():
    api_answer = Statistics()
    api_resp = api_answer.get_status()
    api_answer.list_rigs(api_resp)
    #api_answer.count_rig(api_answer.get_stats)
    #api_resp = api_answer.select_infos(api_answer.get_stats)

    return jsonify(api_resp)


