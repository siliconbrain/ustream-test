import unittest
from unittest.mock import patch

from main import create_item, delete_item, list_items, query_item, update_item


class MockResponse:
    def __init__(self, status_code, reason=None, json=None):
        self.status_code = status_code
        self.reason = reason
        self._json = json

    def json(self):
        return self._json


class MockRequests:
    def __init__(self, response):
        self.calls = []
        self.response = response

    def delete(self, url, timeout, json=None):
        self.calls.append(('delete', url, timeout, json))
        return self.response

    def get(self, url, timeout, json=None):
        self.calls.append(('get', url, timeout, json))
        return self.response

    def post(self, url, timeout, json=None):
        self.calls.append(('post', url, timeout, json))
        return self.response

    def put(self, url, timeout, json=None):
        self.calls.append(('put', url, timeout, json))
        return self.response


class ClientTestCase(unittest.TestCase):
    def setUp(self):
        self.service_url = object()
        self.timeout = object()

    def test_create_item_success(self):
        name = object()
        desc = object()
        mock_response = MockResponse(200)
        mock_requests = MockRequests(mock_response)
        with patch('main.requests', new=mock_requests):
            msg, code = create_item(self.service_url, self.timeout, name, desc)
            self.assertEqual(code, 0)
            self.assertEqual(len(mock_requests.calls), 1)
            self.assertEqual(mock_requests.calls[0][0], 'post')
            self.assertEqual(mock_requests.calls[0][1], self.service_url)
            self.assertEqual(mock_requests.calls[0][2], self.timeout)
            self.assertDictEqual(mock_requests.calls[0][3],
                                 dict(name=name, description=desc))

    def test_create_item_failure(self):
        name = object()
        desc = object()
        mock_response = MockResponse(409)
        mock_requests = MockRequests(mock_response)
        with patch('main.requests', new=mock_requests):
            msg, code = create_item(self.service_url, self.timeout, name, desc)
            self.assertEqual(code, 1)
            self.assertEqual(len(mock_requests.calls), 1)
            self.assertEqual(mock_requests.calls[0][0], 'post')
            self.assertEqual(mock_requests.calls[0][1], self.service_url)
            self.assertEqual(mock_requests.calls[0][2], self.timeout)
            self.assertDictEqual(mock_requests.calls[0][3],
                                 dict(name=name, description=desc))

    def test_delete_item_success(self):
        name = object()
        mock_response = MockResponse(200)
        mock_requests = MockRequests(mock_response)
        with patch('main.requests', new=mock_requests):
            msg, code = delete_item(self.service_url, self.timeout, name)
            self.assertEqual(code, 0)
            self.assertEqual(len(mock_requests.calls), 1)
            self.assertEqual(mock_requests.calls[0][0], 'delete')
            self.assertEqual(mock_requests.calls[0][1], self.service_url)
            self.assertEqual(mock_requests.calls[0][2], self.timeout)
            self.assertDictEqual(mock_requests.calls[0][3], dict(name=name))

    def test_delete_item_failure(self):
        name = object()
        mock_response = MockResponse(204)
        mock_requests = MockRequests(mock_response)
        with patch('main.requests', new=mock_requests):
            msg, code = delete_item(self.service_url, self.timeout, name)
            self.assertEqual(code, 1)
            self.assertEqual(len(mock_requests.calls), 1)
            self.assertEqual(mock_requests.calls[0][0], 'delete')
            self.assertEqual(mock_requests.calls[0][1], self.service_url)
            self.assertEqual(mock_requests.calls[0][2], self.timeout)
            self.assertDictEqual(mock_requests.calls[0][3], dict(name=name))

    def test_list_items(self):
        mock_response = MockResponse(200, json={
            'items': [
                dict(name='item1', description='desc1'),
                dict(name='item2', description='desc2'),
                dict(name='item3', description='desc3'),
            ]
        })
        mock_requests = MockRequests(mock_response)
        with patch('main.requests', new=mock_requests):
            msg, code = list_items(self.service_url, self.timeout)
            for item in mock_response.json()['items']:
                self.assertIn(item['name'], msg)
            self.assertEqual(code, 0)
            self.assertEqual(len(mock_requests.calls), 1)
            self.assertEqual(mock_requests.calls[0][0], 'get')
            self.assertEqual(mock_requests.calls[0][1], self.service_url)
            self.assertEqual(mock_requests.calls[0][2], self.timeout)
            self.assertEqual(mock_requests.calls[0][3], None)

    def test_query_item_success(self):
        name = object()
        mock_response = MockResponse(200, json=dict(name='testitem',
                                                    description='testdesc'))
        mock_requests = MockRequests(mock_response)
        with patch('main.requests', new=mock_requests):
            msg, code = query_item(self.service_url, self.timeout, name)
            self.assertIn(mock_response.json()['description'], msg)
            self.assertEqual(code, 0)
            self.assertEqual(len(mock_requests.calls), 1)
            self.assertEqual(mock_requests.calls[0][0], 'get')
            self.assertEqual(mock_requests.calls[0][1], self.service_url)
            self.assertEqual(mock_requests.calls[0][2], self.timeout)
            self.assertDictEqual(mock_requests.calls[0][3], dict(name=name))

    def test_query_item_failure(self):
        name = object()
        mock_response = MockResponse(404)
        mock_requests = MockRequests(mock_response)
        with patch('main.requests', new=mock_requests):
            msg, code = query_item(self.service_url, self.timeout, name)
            self.assertEqual(code, 1)
            self.assertEqual(len(mock_requests.calls), 1)
            self.assertEqual(mock_requests.calls[0][0], 'get')
            self.assertEqual(mock_requests.calls[0][1], self.service_url)
            self.assertEqual(mock_requests.calls[0][2], self.timeout)
            self.assertDictEqual(mock_requests.calls[0][3], dict(name=name))

    def test_update_item_success(self):
        name = object()
        desc = object()
        mock_response = MockResponse(200)
        mock_requests = MockRequests(mock_response)
        with patch('main.requests', new=mock_requests):
            msg, code = update_item(self.service_url, self.timeout, name, desc)
            self.assertEqual(code, 0)
            self.assertEqual(len(mock_requests.calls), 1)
            self.assertEqual(mock_requests.calls[0][0], 'put')
            self.assertEqual(mock_requests.calls[0][1], self.service_url)
            self.assertEqual(mock_requests.calls[0][2], self.timeout)
            self.assertDictEqual(mock_requests.calls[0][3],
                                 dict(name=name, description=desc))

    def test_update_item_failure(self):
        name = object()
        desc = object()
        mock_response = MockResponse(404)
        mock_requests = MockRequests(mock_response)
        with patch('main.requests', new=mock_requests):
            msg, code = update_item(self.service_url, self.timeout, name, desc)
            self.assertEqual(code, 1)
            self.assertEqual(len(mock_requests.calls), 1)
            self.assertEqual(mock_requests.calls[0][0], 'put')
            self.assertEqual(mock_requests.calls[0][1], self.service_url)
            self.assertEqual(mock_requests.calls[0][2], self.timeout)
            self.assertDictEqual(mock_requests.calls[0][3],
                                 dict(name=name, description=desc))


if __name__ == '__main__':
    unittest.main()
