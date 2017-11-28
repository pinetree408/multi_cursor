#!/usr/bin/env python

import os
from flask import Flask, render_template, session, redirect, url_for
from flask_socketio import SocketIO, emit

import json
from LanguageModelMulti import *

app = Flask(__name__)
app.secret_key = "secret"
socketio = SocketIO(app)

@app.before_request
def before_request():
    if 'session' in session:
        pass
    else:
        session['session'] = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/mynamespace')
def connect():
    input_data = []
    words, multiAlphaFreqs = getWordsAndMultiAlphaFreqsFromMultiAlphaPrefixHybrid(input_data)
    if len(words) < 5:
        for i in range(5 - len(words)):
            words.append('')
    data = {
            'letter': ', '.join(multiAlphaFreqs),
            'word': ', '.join(words[:5])
            }
    emit("response", {'data': data})

@socketio.on('disconnect', namespace='/mynamespace')
def disconnect():
    session.clear()
    print "Disconnected"

@socketio.on("request", namespace='/mynamespace')
def request(message):
    input_data = []
    if message['data'] != '':
        for item in message['data'].split(' '):
            input_data.append(str(item))
    words, multiAlphaFreqs = getWordsAndMultiAlphaFreqsFromMultiAlphaPrefixHybrid(input_data)
    if len(words) < 5:
        for i in range(5 - len(words)):
            words.append('')
    data = {
            'letter': ', '.join(multiAlphaFreqs),
            'word': ', '.join(words[:5])
            }
    emit("response", {'data': data})

@socketio.on("logging", namespace='/mynamespace')
def logging(message):
    print message

@app.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('create_user.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
