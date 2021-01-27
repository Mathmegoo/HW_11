# -*- coding: utf-8 -*-
from flask import Flask, request, url_for



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
app.config.update (
    DEBUG = True,
    WTF_CSRF_ENABLED = False,
)



@app.route('/', methods=['GET'])
def home():
    Riddler.new_number(100)
    return 'Загадано целое число от 1 до 100'


@app.route('/guess', methods=['POST'])
def guess():

    if Riddler.number is None:
        return '<a href="/">Вы не загадали число</a>' 
    
    if request.method == 'POST':

        form = GuessForm(request.form)

        if form.validate():
            user_number = form.riddle_number.data

            if user_number == Riddler.number:
                Riddler.new_number(100)
                return 'Угадали! Загадано еще одно число'
            elif user_number > Riddler.number:
                return 'Ваше число больше загаданного (>)'
            elif user_number < Riddler.number:
                return 'Ваше число меньше загаданного (<)'
        else:
            return str(form.errors)
        
    else:
        return url_for('home')



if __name__ == '__main__':
    
    seed_number = environ.get('FLASK_RANDOM_SEED')
    
    if seed_number is None:
        print('FLASK_RANDOM_SEED is not assigned. Aborted!')
        exit()

    print('FLASK_RANDOM_SEED =', seed_number)

    random.seed(seed_number)
    
    app.run()

