import unittest
from unittest.mock import patch

from core import configure_app


class MockApp:
    def __init__(self):
        self.routes = dict()

    def route(self, rule, methods=None):
        def decorator(func):
            for method in methods:
                key = (rule, method)
                if key in self.routes:
                    raise Exception('Route duplication')
                self.routes[key] = func

        return decorator


class MockDB:
    def __init__(self):
        self.calls = []
        self.result = None

    def get_all(self):
        self.calls.append(('get_all', ))
        return self.result

    def try_del(self, key):
        self.calls.append(('try_del', key))
        return self.result

    def try_get(self, key):
        self.calls.append(('try_get', key))
        return self.result

    def try_ins(self, key, value):
        self.calls.append(('try_ins', key, value))
        return self.result

    def try_upd(self, key, value):
        self.calls.append(('try_upd', key, value))
        return self.result


class MockRequest:
    def __init__(self, json):
        self.json = json


class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.url_path = object()
        self.db = MockDB()
        self.app = configure_app(MockApp(), self.url_path, self.db)

    def test_route_create(self):
        self.assertTrue((self.url_path, 'POST') in self.app.routes)

    def test_route_query_and_list(self):
        self.assertTrue((self.url_path, 'GET') in self.app.routes)

    def test_route_update(self):
        self.assertTrue((self.url_path, 'PUT') in self.app.routes)

    def test_route_delete(self):
        self.assertTrue((self.url_path, 'DELETE') in self.app.routes)

    def test_create_success(self):
        create_func = self.app.routes[(self.url_path, 'POST')]
        self.db.result = True
        name = object()
        desc = object()
        mock_request = MockRequest(dict(name=name, description=desc))
        with patch('core.request', new=mock_request):
            with patch('core.make_response', new=lambda c: c):
                self.assertEqual(create_func(), 200)
                self.assertEqual(len(self.db.calls), 1)
                self.assertEqual(self.db.calls[0], ('try_ins', name, desc))

    def test_create_failure(self):
        create_func = self.app.routes[(self.url_path, 'POST')]
        self.db.result = None
        name = object()
        desc = object()
        mock_request = MockRequest(dict(name=name, description=desc))
        with patch('core.request', new=mock_request):
            with patch('core.make_response', new=lambda c: c):
                self.assertEqual(create_func(), 409)
                self.assertEqual(len(self.db.calls), 1)
                self.assertEqual(self.db.calls[0], ('try_ins', name, desc))

    def test_query_success(self):
        query_and_list_func = self.app.routes[(self.url_path, 'GET')]
        self.db.result = object()
        name = object()
        mock_request = MockRequest(dict(name=name))
        with patch('core.request', new=mock_request):
            with patch('core.jsonify', new=lambda c: c):
                self.assertDictEqual(query_and_list_func(), {
                    'name': name,
                    'description': self.db.result
                })
                self.assertEqual(len(self.db.calls), 1)
                self.assertEqual(self.db.calls[0], ('try_get', name))

    def test_query_failure(self):
        query_and_list_func = self.app.routes[(self.url_path, 'GET')]
        self.db.result = None
        name = object()
        mock_request = MockRequest(dict(name=name))
        with patch('core.request', new=mock_request):
            with patch('core.make_response', new=lambda c: c):
                self.assertEqual(query_and_list_func(), 404)
                self.assertEqual(len(self.db.calls), 1)
                self.assertEqual(self.db.calls[0], ('try_get', name))

    def test_update_success(self):
        update_func = self.app.routes[(self.url_path, 'PUT')]
        self.db.result = True
        name = object()
        desc = object()
        mock_request = MockRequest(dict(name=name, description=desc))
        with patch('core.request', new=mock_request):
            with patch('core.make_response', new=lambda c: c):
                self.assertEqual(update_func(), 200)
                self.assertEqual(len(self.db.calls), 1)
                self.assertEqual(self.db.calls[0], ('try_upd', name, desc))

    def test_update_failure(self):
        update_func = self.app.routes[(self.url_path, 'PUT')]
        self.db.result = None
        name = object()
        desc = object()
        mock_request = MockRequest(dict(name=name, description=desc))
        with patch('core.request', new=mock_request):
            with patch('core.make_response', new=lambda c: c):
                self.assertEqual(update_func(), 404)
                self.assertEqual(len(self.db.calls), 1)
                self.assertEqual(self.db.calls[0], ('try_upd', name, desc))

    def test_delete_success(self):
        delete_func = self.app.routes[(self.url_path, 'DELETE')]
        self.db.result = True
        name = object()
        mock_request = MockRequest(dict(name=name))
        with patch('core.request', new=mock_request):
            with patch('core.make_response', new=lambda c: c):
                self.assertEqual(delete_func(), 200)
                self.assertEqual(len(self.db.calls), 1)
                self.assertEqual(self.db.calls[0], ('try_del', name))

    def test_delete_failure(self):
        delete_func = self.app.routes[(self.url_path, 'DELETE')]
        self.db.result = False
        name = object()
        mock_request = MockRequest(dict(name=name))
        with patch('core.request', new=mock_request):
            with patch('core.make_response', new=lambda c: c):
                self.assertEqual(delete_func(), 204)
                self.assertEqual(len(self.db.calls), 1)
                self.assertEqual(self.db.calls[0], ('try_del', name))

    def test_list(self):
        query_and_list_func = self.app.routes[(self.url_path, 'GET')]
        self.db.result = [(object(), object()), (object(), object())]
        mock_request = MockRequest(None)
        with patch('core.request', new=mock_request):
            with patch('core.jsonify', new=lambda c: c):
                self.assertDictEqual(query_and_list_func(), {
                    'items': [{'name': n, 'description': d}
                              for n, d in self.db.result]
                })
                self.assertEqual(len(self.db.calls), 1)
                self.assertEqual(self.db.calls[0], ('get_all', ))


if __name__ == '__main__':
    unittest.main()
