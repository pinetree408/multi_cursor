#!/usr/bin/env python

import os
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit

import json
import LanguageModelMulti

app = Flask(__name__)
app.secret_key = "secret"
socketio = SocketIO(app)

user_no = 1

def get_word_list(input_data):
    word_set = {}
    if len(input_data) == 1:
        word_set = LanguageModelMulti.PREFIXLEN_ONE
    elif len(input_data) == 2:
        word_set = LanguageModelMulti.PREFIXLEN_TWO
    elif len(input_data) == 3:
        word_set = LanguageModelMulti.PREFIXLEN_THREE
    elif len(input_data) == 4:
        word_set = LanguageModelMulti.PREFIXLEN_FOUR
    elif len(input_data) == 5:
        word_set = LanguageModelMulti.PREFIXLEN_FIVE

    word_result = word_set[json.dumps(input_data)]
    return word_result

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
    letter_result = LanguageModelMulti.getStaticMultiAlphasFromPrefix(input_data)
    word_result = LanguageModelMulti.getWordsFromMultiAlphaPrefix(input_data)
    data = {
            'letter': ', '.join(letter_result),
            'word': ', '.join(word_result[:5])
            }
    emit("response", {'data': data, 'username': session['username']})

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
    letter_result = LanguageModelMulti.getStaticMultiAlphasFromPrefix(input_data)
    if len(input_data) != 0:
        word_result = get_word_list(input_data)
    else:
        word_result = LanguageModelMulti.getWordsFromMultiAlphaPrefix(input_data)
    data = {
            'letter': ', '.join(letter_result),
            'word': ', '.join(word_result[:5])
            }
    emit("response", {'data': data, 'username': session['username']}, broadcast=True)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    #app.config['DEBUG'] = True
    socketio.run(app, host='0.0.0.0')
