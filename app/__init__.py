#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify
from app.view import Statistics

app = Flask(__name__)

app.config.from_object('config')


@app.route('/')
@app.route('/index')
def index():
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
    api_resp = api_answer.get_status()
    #api_answer.count_rig(api_answer.get_stats)
    #api_resp = api_answer.select_infos(api_answer.get_stats)

    return jsonify(api_resp)

