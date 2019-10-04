import datetime
import unittest
from unittest import mock

from app import app, db
from app.models import Url, Response


class BaseTestCaseWithDatabase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class UrlModelTestCase(BaseTestCaseWithDatabase):
    def test_to_dict(self):
        pass


class RoutesTestCase(BaseTestCaseWithDatabase):
    def test_bad_path(self):
        pass

    def test_get_urls(self):
        with app.test_client() as c:
            # no Urls
            response = c.get('/api/fetcher')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                [],
                response.json
            )

            # one Url
            u1 = Url(url='url #1', interval=60)
            db.session.add(u1)
            db.session.commit()

            response = c.get('/api/fetcher')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                [{'id': 1, 'interval': 60, 'url': 'url #1'}],
                response.json
            )

            # many Urls
            u2 = Url(url='url #2', interval=60)
            u3 = Url(url='url #3', interval=60)
            db.session.add_all([u2, u3])
            db.session.commit()

            response = c.get('/api/fetcher')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                [{'id': 1, 'interval': 60, 'url': 'url #1'},
                 {'id': 2, 'interval': 60, 'url': 'url #2'},
                 {'id': 3, 'interval': 60, 'url': 'url #3'}],
                response.json
            )

    def test_create_or_update_url(self):
        with app.test_client() as c:
            # no url key
            response = c.post('/api/fetcher', data={'interval': '30'})
            self.assertEqual(400, response.status_code)

            # no interval key
            response = c.post('/api/fetcher', data={'url': 'some url'})
            self.assertEqual(400, response.status_code)

            # interval is not int
            response = c.post('/api/fetcher',
                              data={'url': 'some url', 'interval': 'aaa'})
            self.assertEqual(400, response.status_code)

            # interval <= 0
            response = c.post('/api/fetcher',
                              data={'url': 'some url', 'interval': '-1'})
            self.assertEqual(400, response.status_code)

            # request larger than PAYLOAD_MAX_SIZE
            payload = b'0' * 2 * app.config['PAYLOAD_MAX_SIZE']
            response = c.post('/api/fetcher', data=payload)
            self.assertEqual(413, response.status_code)

            # successful create
            response = c.post('/api/fetcher',
                              json={'url': 'some url', 'interval': '30'})
            self.assertEqual(200, response.status_code)
            self.assertEqual(
                {'id': 1},
                response.json
            )
            self.assertEqual(
                {'id': 1, 'interval': 30, 'url': 'some url'},
                Url.query.get(1).to_dict()
            )

            # successful modify
            response = c.post('/api/fetcher',
                              json={'url': 'some url', 'interval': '60'})
            self.assertEqual(200, response.status_code)
            self.assertEqual(
                {'id': 1},
                response.json
            )
            self.assertEqual(
                {'id': 1, 'interval': 60, 'url': 'some url'},
                Url.query.get(1).to_dict()
            )

    def test_get_url(self):
        with app.test_client() as c:
            # no Urls
            response = c.get('/api/fetcher/1')
            self.assertEqual(response.status_code, 404)

            # successful get
            u1 = Url(url='url #1', interval=60)
            db.session.add(u1)
            db.session.commit()

            response = c.get('/api/fetcher/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                {'id': 1, 'interval': 60, 'url': 'url #1'},
                response.json
            )

    def test_delete_url(self):
        with app.test_client() as c:
            # no Urls
            response = c.delete('/api/fetcher/1')
            self.assertEqual(response.status_code, 404)

            # successful delete
            u1 = Url(url='url #1', interval=60)
            db.session.add(u1)
            db.session.commit()

            response = c.delete('/api/fetcher/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                {'id': 1},
                response.json
            )
            self.assertEqual(
                None,
                Url.query.get(1)
            )

    def test_get_url_history(self):
        # TODO: mock date to check create_at initialization
        mock_datetime = datetime.datetime(2019, 10, 4, 9, 30, 0)

        with app.test_client() as c:
            # no Urls
            response = c.get('/api/fetcher/1/history')
            self.assertEqual(response.status_code, 404)

            # no Responses
            u1 = Url(url='url #1', interval=60)
            db.session.add(u1)
            db.session.commit()

            response = c.get('/api/fetcher/1/history')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                [],
                response.json
            )

            # one Response
            r1 = Response(response='test response #1', duration=1, url=u1)
            r1.created_at = mock_datetime
            db.session.add(r1)
            db.session.commit()

            response = c.get('/api/fetcher/1/history')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                [{'created_at': 'Fri, 04 Oct 2019 09:30:00 GMT',
                  'duration': '1.000',
                  'response': 'test response #1'}],
                response.json
            )

            # many Responses
            r2 = Response(response='test response #2', duration=2, url=u1)
            r3 = Response(response='test response #3', duration=3, url=u1)
            r2.created_at = mock_datetime
            r3.created_at = mock_datetime
            db.session.add_all([r2, r3])
            db.session.commit()

            response = c.get('/api/fetcher/1/history')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                [{'created_at': 'Fri, 04 Oct 2019 09:30:00 GMT',
                  'duration': '1.000',
                  'response': 'test response #1'},
                 {'created_at': 'Fri, 04 Oct 2019 09:30:00 GMT',
                  'duration': '2.000',
                  'response': 'test response #2'},
                 {'created_at': 'Fri, 04 Oct 2019 09:30:00 GMT',
                  'duration': '3.000',
                  'response': 'test response #3'}],
                response.json
            )


if __name__ == '__main__':
    unittest.main(verbosity=2)
