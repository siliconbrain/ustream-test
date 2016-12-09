from flask import Flask, jsonify, request
import os
from redis import StrictRedis


def encode(s):
    return s and s.encode('utf-8')

def decode(b):
    return b and b.decode('utf-8')


class RedisWrapper:
    def __init__(self, host, port, db):
        self.rdb = StrictRedis(host=host, port=port, db=db)

    def get_all(self):
        keys = self.rdb.keys()
        values = self.rbd.mget(keys)
        items = zip(keys, values)
        return [(decode(k), decode(v)) for k, v in items if v is not None]

    def try_del(self, key):
        return 0 < self.rdb.delete(encode(key))

    def try_get(self, key):
        return decode(self.rdb.get(encode(key)))

    def try_ins(self, key, value):
        return self.rdb.set(encode(key), encode(value), nx=True)

    def try_upd(self, key, value):
        return self.rdb.set(encode(key), encode(value), xx=True)

app = Flask(__name__)

url_path = os.environ['ITEMS_SERVICE_URL_PATH']

redis_host = os.environ['ITEMS_SERVICE_REDIS_HOST']
redis_port = int(os.environ['ITEMS_SERVICE_REDIS_PORT'])
redis_db = int(os.environ['ITEMS_SERVICE_REDIS_DB'])

db = RedisWrapper(redis_host, redis_port, redis_db)

@app.route(url_path, methods=['POST'])
def create_item():
    name = request.json['name']
    desc = request.json['description']

    if db.try_ins(name, desc):
        return "Created.", 200
    else:
        return "Already exists.", 409


@app.route(url_path, methods=['GET'])
def query_item_or_list_items():
    if request.json and 'name' in request.json:
        name = request.json['name']
        desc = db.try_get(name)
        if desc is None:
            return "Item not found.", 404
        else:
            return jsonify({'name': name, 'description': desc})
    else:
        return jsonify([{'name': name, 'description': desc} for name, desc in db.get_all()])


@app.route(url_path, methods=['PUT'])
def update_item():
    name = request.json['name']
    desc = request.json['description']

    if db.try_upd(name, desc):
        return "Updated.", 200
    else:
        return "Not found.", 404


@app.route(url_path, methods=['DELETE'])
def delete_item():
    name = request.json['name']

    if db.try_del(name):
        return "Deleted.", 200
    else:
        return "Not found.", 204


if __name__ == '__main__':
    host = os.getenv('ITEMS_SERVICE_HOST', '127.0.0.1')
    port = int(os.getenv('ITEMS_SERVICE_PORT', '5000'))
    debug = os.getenv('ITEMS_SERVICE_DEBUG', 'False').upper() == 'TRUE'
    app.run(host=host, port=port, debug=debug)
