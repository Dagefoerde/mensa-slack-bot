from requests_mock.contrib import fixture
from testtools import TestCase

import cron

interval = 60

scheduleRunner = cron.ScheduleRunner().start()


class TestCronBasic(TestCase):
    # Called before every test execution
    def setUp(self):
        super(TestCronBasic, self).setUp()
        self.requests_mock = self.useFixture(fixture.Fixture())
        cron.scheduleCleanAndSetup()

    def testSingleton(self):
        assert cron.ScheduleRunner() == cron.ScheduleRunner()
