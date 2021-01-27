# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect

import config

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, validators

import random, datetime
from os import environ



__author__ = 'BorisRubin'



class Riddler(object):
    '''
    Класс Riddler (singleton) будет загадывать числа
    '''
    __instance = None

    number = None

    def __new__(cls):
        if Riddler.__instance is None:
            Riddler.__instance = object.__new__(cls)

        return Riddler.__instance

    @classmethod
    def new_number(cls, limit):
        cls.number = random.randint(1, limit)
        print('Загадано число',cls.number)


class GuessForm(FlaskForm):
    riddle_number = DecimalField(label='Number is', validators=[validators.Required()])



app = Flask(__name__)
app.config.from_object(config)



@app.route('/', methods=['GET'])
def home():
    '''
    Начальная страница
    '''
    print(session)
    if 'username' in session:
        Riddler.new_number(100)
        session['riddle_number'] = Riddler.number
        print(session)
        return '<a href="/guess">Пользователю {} загадано целое число от 1 до 100. Перейдите к угадыванию!</a>'.format(session['username'])
    
    return '<a href="/login">Не выполнен вход!</a>'


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    cсылка для входа пользователя
    '''
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['riddle_number'] = 0
        session['guess_count'] = 0

        return redirect(url_for('home'))

    return '''
        <form method="post">
            <p><strong>Введите имя пользователя</strong></p>
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    '''
    cсылка для разлогирования
    '''
    session.pop('username', None)
    session.pop('riddle_number', None)
    session.pop('guess_count', None)

    return redirect(url_for('home'))    


@app.route('/guess', methods=['GET', 'POST'])
def guess():

    print(session)

    user_riddle_number = session['riddle_number']

    if Riddler.number is None:
        return '<a href="/">Вы не загадали число</a>' 
    
    if request.method == 'POST':

        form = GuessForm(request.form)

        if form.validate():
            user_number = form.riddle_number.data

            if user_number == user_riddle_number:
                Riddler.new_number(100)
                session['riddle_number'] = Riddler.number
                session['guess_count'] = 0
                return '<a href="/guess">Угадали! Загадано еще одно число</a>'
            elif user_number > user_riddle_number:
                session['guess_count'] += 1
                return '<a href="/guess">Ваше число больше загаданного (>), попробуйте еще раз!</a>'
            elif user_number < user_riddle_number:
                session['guess_count'] += 1
                return '<a href="/guess">Ваше число меньше загаданного (<), попробуйте еще раз!</a>'
        else:
            return str(form.errors)
        
    else:
        return'''
        <form method="post">
            <p><strong>Введите число</strong></p>
            <p><input type=number name=riddle_number>
            <p><input type=submit value="Попробовать">
        </form>
        '''


if __name__ == '__main__':
    
    seed_number = environ.get('FLASK_RANDOM_SEED')
    
    if seed_number is None:
        print('FLASK_RANDOM_SEED is not assigned. Aborted!')
        exit()
    
    seed_shift = random.randint(1,100)

    random.seed(int(seed_number) + seed_shift)

    print('FLASK_RANDOM_SEED =', seed_number)
    print('MY SEED =', (int(seed_number) + seed_shift))

    app.run()

