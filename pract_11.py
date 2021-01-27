from flask import Flask , request
import numpy as np
from threading import Lock
from flask_wtf import FlaskForm
from wtforms import StringField, validators, ValidationError
import os
from os import environ



app = Flask(__name__)


app.config.update (
    DEBUG = True,
    WTF_CSRF_ENABLED = False,
)


class Ran (object):
    rand_num = 0
    seed = 2
       
    

def random_gen(sed):
    np.random.seed(sed)
    Ran.rand_num = np.random.randint(100)




@app.route ('/local')
def home():
    return 'The number is guessed! send POST with nambers at /home '

@app.route('/home', methods = ['GET', 'POST'])
def home_2 ():
    if request.method == 'POST':
        print(request.form)    # неизменяемый дикт состоящий из имени поля (полей), которое(ые) заполнил пользователь, и его(их) содержимое.
        user_dict = dict(request.form) # приводим ввод к обычному словарю.
        user_in = user_dict['name']
        print('random num is {}'.format(Ran.rand_num))
        print(user_dict['name']) # обращаемся к конкретному значению, которое ввел юзер в нужном нам поле по ключу (имени поля)
        while True:
            try:            
                Ran.seed += 1
                if int(user_in) > int (Ran.rand_num):
                    return 'Your namber too big!'
                if int(user_in) < int (Ran.rand_num):
                    return 'Yuur namber is too small!'
                if int(user_in) == int (Ran.rand_num):
                    print('Key is {}'.format(Ran.seed))
                    random_gen(Ran.seed)
                    print ('random num is {}'.format(Ran.rand_num))
                    return 'Got it!! it is {},  New number was guessed!'.format(user_in)
            except:
                return 'You mast gues is integeer num!'    
    if request.method == 'GET':
        return 'Hello, world!'
if True:
    app.run()    
    random_gen(Ran.seed)