#!/usr/bin/env python3
from argparse import ArgumentParser
from flask import Flask
import os

from core import configure_app, RedisWrapper


parser = ArgumentParser("The Items Service standalone server.")
parser.add_argument('--host', default='localhost',
                    help="IP or hostname of the service. "
                         "Default is localhost.")
parser.add_argument('--port', type=int, required=True)
parser.add_argument('--path', required=True,
                    help="URL path of the service. E.g.: /items")
parser.add_argument('--debug', action='store_true',
                    help="Start the service in debug mode.")


if __name__ == '__main__':
    args = parser.parse_args()

    redis_host = os.environ['REDIS_HOST']
    redis_port = int(os.environ['REDIS_PORT'])
    redis_db = int(os.environ['REDIS_DB'])

    db = RedisWrapper(redis_host, redis_port, redis_db)
    app = configure_app(Flask(__name__), args.path, db)
    app.run(host=args.host, port=args.port, debug=args.debug)
