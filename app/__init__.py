import rq
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.redis = Redis.from_url(app.config['REDIS_URL'])
app.task_queue = rq.Queue('urls_wp-tasks', connection=app.redis)

from app import routes, models
