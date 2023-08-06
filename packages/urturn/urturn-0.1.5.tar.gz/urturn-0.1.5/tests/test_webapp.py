import unittest
from urturn.scheduler import Scheduler
from urturn.trigger import ImmediateTrigger
from urturn.webapp import SchedulerWebApp


class TestSchedulerWebApp(unittest.TestCase):
    def setUp(self):
        self.scheduler = Scheduler()
        self.scheduler.add_job_config(
            name="TestJob",
            execution_cmd_args=["echo", "Hello, World!"],
            trigger=ImmediateTrigger()
        )
        self.webapp = SchedulerWebApp(self.scheduler)
        self.app = self.webapp.app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"TestJob", response.data)

    def test_job_config(self):
        response = self.app.get('/job_config/TestJob')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"TestJob", response.data)

    def test_job_config_not_found(self):
        response = self.app.get('/job_config/NonexistentJob')
        self.assertEqual(response.status_code, 404)
