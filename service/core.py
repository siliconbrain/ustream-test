from flask import jsonify, request, Response


def encode(s):
    return s and s.encode('utf-8')


def decode(b):
    return b and b.decode('utf-8')


class RedisWrapper:
    def __init__(self, host, port, db):
        from redis import StrictRedis
        self.rdb = StrictRedis(host=host, port=port, db=db)

    def get_all(self):
        keys = self.rdb.keys()
        values = self.rdb.mget(keys) if keys else []
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


def make_response(status_code):
    return Response(status=status_code)


def configure_app(app, url_path, db):
    """Configure the provided Flask application.

    :param app: Flask application to configure
    :param url_path: path string specifying the route
    :param db: database instance to use
    :returns: the specified Flask application
    """
    @app.route(url_path, methods=['POST'])
    def create_item():
        name = request.json['name']
        desc = request.json['description']

        if db.try_ins(name, desc):
            return make_response(200)
        else:
            return make_response(409)

    @app.route(url_path, methods=['GET'])
    def query_item_or_list_items():
        if request.json and 'name' in request.json:  # query item
            name = request.json['name']
            desc = db.try_get(name)
            if desc is None:
                return make_response(404)
            else:
                return jsonify({'name': name, 'description': desc})
        else:  # list items
            return jsonify({'items': [{'name': name, 'description': desc}
                                      for name, desc in db.get_all()]})

    @app.route(url_path, methods=['PUT'])
    def update_item():
        name = request.json['name']
        desc = request.json['description']

        if db.try_upd(name, desc):
            return make_response(200)
        else:
            return make_response(404)

    @app.route(url_path, methods=['DELETE'])
    def delete_item():
        name = request.json['name']

        if db.try_del(name):
            return make_response(200)
        else:
            return make_response(204)

    return app
