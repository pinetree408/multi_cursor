#!/usr/bin/env python

import os
from flask import Flask, render_template, session, redirect, url_for
from flask_socketio import SocketIO, emit
from base64 import b64encode

import json
from LanguageModelMulti import *

app = Flask(__name__)
app.secret_key = "secret"
socketio = SocketIO(app)

user_no = 1

@app.before_request
def before_request():
    global user_no
    if 'session' in session and 'user-id' in session:
        pass
    else:
        session['session'] = os.urandom(24)
        session['username'] = 'user'+str(user_no)
        user_no += 1

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/mynamespace')
def connect():
    input_data = []
    words, multiAlphaFreqs = getWordsAndMultiAlphaFreqsFromMultiAlphaPrefixHybrid(input_data)
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
    data = {
            'letter': ', '.join(multiAlphaFreqs),
            'word': ', '.join(words[:5])
            }
    emit("response", {'data': data})

@socketio.on("logging", namespace='/mynamespace')
def logging(message):
    filename = session['username']
    with open("logs/log_" + filename + ".csv","a+") as f:
        log = \
            str(message['session']) + ',' + \
            str(message['block']) + ',' + \
            str(message['target']) + ',' + \
            str(message['time']) + ',' + \
            str(message['input']) + ',' + \
            str(message['word']) + ',' + \
            str(message['key']) + ',' + \
            str(message['visible']) + ',' + \
            str(message['type']) + '\n'
        f.write(log)

@app.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('create_user.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
