from contextlib import contextmanager
import os
from redis import StrictRedis
from subprocess import call, Popen
from tempfile import TemporaryFile
import time
import unittest


REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = int(os.environ['REDIS_PORT'])
REDIS_DB = int(os.environ['REDIS_DB'])
SERVICE_PORT = int(os.environ['SERVICE_PORT'])


def call_client(*args, timeout=10):
    with TemporaryFile() as out:
        with TemporaryFile() as err:
            exit_code = call(('python', 'client/main.py') + args,
                             stdout=out,
                             stderr=err,
                             timeout=timeout)
            out.seek(0)
            err.seek(0)
            stdout = out.read().decode('utf-8')
            stderr = err.read().decode('utf-8')
            return exit_code, stdout, stderr


@contextmanager
def service_context():
    proc = Popen(('gunicorn',
                  '-w', '2',
                  '-b', 'localhost:%s' % SERVICE_PORT,
                  '--chdir', 'service',
                  'wsgi:application'))
    time.sleep(0.1)  # wait for the server to start
    try:
        yield
    finally:
        proc.terminate()
        proc.wait(timeout=5)


redis_db = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['URL_PATH'] = url_path = '/items'
        self.service_url = 'http://localhost:{port}{path}'.format(
            port=SERVICE_PORT, path=url_path
        )
        redis_db.flushdb()  # clear db

    def test_create_success(self):
        name = 'test item'
        desc = 'test desc'
        with service_context():
            code, out, err = call_client(self.service_url, '-c', name, desc)
            self.assertEqual(code, 0)
            self.assertEqual(redis_db.get(name.encode('utf-8')),
                             desc.encode('utf-8'))

    def test_create_collision(self):
        name = 'test item'
        desc = 'test desc'
        redis_db.set(name.encode('utf-8'), desc.encode('utf-8'))
        with service_context():
            code, out, err = call_client(self.service_url, '-c', name, desc)
            self.assertEqual(code, 1)

    def test_query_success(self):
        name = 'test item'
        desc = 'test desc'
        redis_db.set(name.encode('utf-8'), desc.encode('utf-8'))
        with service_context():
            code, out, err = call_client(self.service_url, '-q', name)
            self.assertEqual(code, 0)
            self.assertIn(desc, out)

    def test_query_not_found(self):
        name = 'unknown item'
        with service_context():
            code, out, err = call_client(self.service_url, '-q', name)
            self.assertEqual(code, 1)

    def test_update_success(self):
        name = 'test item'
        desc = 'new test'
        redis_db.set(name.encode('utf-8'), 'old test'.encode('utf-8'))
        with service_context():
            code, out, err = call_client(self.service_url, '-u', name, desc)
            self.assertEqual(code, 0)
            self.assertEqual(redis_db.get(name.encode('utf-8')),
                             desc.encode('utf-8'))

    def test_update_not_found(self):
        name = 'unknown item'
        desc = 'unknown desc'
        with service_context():
            code, out, err = call_client(self.service_url, '-u', name, desc)
            self.assertEqual(code, 1)
            self.assertEqual(redis_db.get(name.encode('utf-8')), None)
        
    def test_delete_success(self):
        name = 'test item'
        redis_db.set(name.encode('utf-8'), 'test desc'.encode('utf-8'))
        with service_context():
            code, out, err = call_client(self.service_url, '-d', name)
            self.assertEqual(code, 0)
            self.assertEqual(redis_db.get(name.encode('utf-8')), None)

    def test_delete_not_found(self):
        name = 'unknown item'
        with service_context():
            code, out, err = call_client(self.service_url, '-d', name)
            self.assertEqual(code, 1)

    def test_list_empty(self):
        with service_context():
            code, out, err = call_client(self.service_url, '-l')
            self.assertEqual(code, 0)

    def test_list_some(self):
        items = [
            dict(name='item1', description='desc1'),
            dict(name='item2', description='desc2'),
            dict(name='item3', description='desc3'),
        ]
        for item in items:
            redis_db.set(item['name'].encode('utf-8'),
                         item['description'].encode('utf-8'))
        with service_context():
            code, out, err = call_client(self.service_url, '-l')
            self.assertEqual(code, 0)
            for item in items:
                self.assertIn(item['name'], out)

    def tearDown(self):
        redis_db.flushdb()  # clear db


if __name__ == '__main__':
    unittest.main()
