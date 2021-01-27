# -*- coding: utf-8 -*-
from contextlib import contextmanager
from time import time, sleep

__author__ = 'BorisRubin'

# разделитель вывода заданий в консоль с комментариями
@contextmanager
def delimeter(comments, num):
    
    comment_length_extended = '-' * ( len(comments[num]) + 4)

    print('\n-----[ Task {} started ]---[ {} ]---\n'.format(num, comments[num]))
    yield
    print('\n-----[ Task {} ended   ]---{}---\n'.format(num, comment_length_extended))


# менеджер контекста, который может переопределить значение lock на True
@contextmanager
def locker(some_lock):
	some_lock.lock = True
	yield some_lock


class Lock(object):
    def __init__(self):
    	self.lock = False


# менеджер контекста, который проглатывает все исключения и пишет их в консоль
@contextmanager
def exception_logger():
    try:
        yield
    except Exception as e:
        print('logs => Error occured: ' + str(e))


# класс менеджер контекста, который измеряет время выполнения блока кода
class TimeIt():

    def __enter__(self):
        self.started = time()
        return self

    def __exit__(self, *args):
        self.ended = time()
        self.result = self.ended - self.started
        

if __name__ == '__main__':
    
    tasks = {1: 'Менеджер контекста, который может переопределить значение lock на True',
             2: 'Менеджер контекста, который проглатывает все исключения и пишет их в консоль',
             3: 'Класс менеджер контекста, который измеряет время выполнения блока кода'}

    lock1 = Lock()
    print(type(tasks[1]))
    print(tasks[1])

    with delimeter(tasks, 1), locker(lock1):
    	print('{} locked is {} '.format(lock1, lock1.lock))


    with delimeter(tasks, 2):
        with exception_logger():
            1 / 0 
            
        with exception_logger():
            's' / 2

        print('Error logging done!') 


    with delimeter(tasks,3):
        with TimeIt() as timer:
            sleep(1)
        
        print('Execution time was: ', timer.result)
