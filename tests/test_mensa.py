import testtools
from requests_mock.contrib import fixture
import requests

import mensa


class TestSlack(testtools.TestCase):
    def setUp(self):
        super(TestSlack, self).setUp()
        self.requests_mock = self.useFixture(fixture.Fixture())
        self.requests_mock.register_uri('GET', mensa.leo_uri, json=dict(slack=1))

    def testSlackTimeout(self):
        self.requests_mock.register_uri('GET', mensa.leo_uri, exc=requests.exceptions.Timeout)
        response = mensa.getMenues()
        assert response is None