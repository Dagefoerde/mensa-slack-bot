import testtools
from requests_mock.contrib import fixture
import requests

import slackMensaBot


class TestSlack(testtools.TestCase):
    def setUp(self):
        super(TestSlack, self).setUp()
        self.requests_mock = self.useFixture(fixture.Fixture())
        self.requests_mock.register_uri('POST', slackMensaBot.slackURL, json=dict(slack=1))

    def testSlackTimeout(self):
        self.requests_mock.register_uri('POST', slackMensaBot.slackURL, exc=requests.exceptions.Timeout)
        response = slackMensaBot.messageSlackWithMensaMessage({'test':'blub'})
        assert response is None

    def testNullEmptyHandling(self):
        result = slackMensaBot.messageSlackWithMensaMessage(None)
        assert result is None