""" Package for WSGI deployment. """
from flask import Flask
import os

from core import configure_app, RedisWrapper


url_path = os.environ['URL_PATH']

redis_host = os.environ['REDIS_HOST']
redis_port = int(os.environ['REDIS_PORT'])
redis_db = int(os.environ['REDIS_DB'])

db = RedisWrapper(redis_host, redis_port, redis_db)

application = configure_app(Flask(__name__), url_path, db)
