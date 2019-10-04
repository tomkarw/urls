import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAYLOAD_MAX_SIZE = 10**6
    MIN_INTERVAL = 1
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    TIMEOUT = 5
