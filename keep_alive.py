import os
from flask import Flask
from threading import Thread
import random

app = Flask('')


@app.route('/')
def home():
    return 'Im in!'


def run():
    port = 5000
    if(bool(os.getenv('debug'))):
        port = random.randint(2000, 9000)

    app.run(
		host='0.0.0.0',
		port=port
	)


def keep_alive():
    '''
    Creates and starts new thread that runs the function run.
    '''
    t = Thread(target=run)
    t.start()
