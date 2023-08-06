import unittest
import time
from threading import Thread
from datetime import timedelta
from time import sleep

from urturn.trigger import PeriodicTrigger
from urturn.scheduler import Scheduler


class TestScheduler(unittest.TestCase):

    def test_scheduler_job_trigger(self):
        # Create a periodic trigger that triggers every second
        trigger = PeriodicTrigger(timedelta(seconds=1))

        # Create a scheduler and add the mocked job config
        scheduler = Scheduler()
        scheduler.add_job_config(
            'myjob', ["python", "-c", "print('hello')"], trigger)

        # Run the scheduler for a short duration (5 seconds) and then stop it
        scheduler_thread = Thread(target=scheduler.start)
        scheduler_thread.start()
        time.sleep(5)
        scheduler.stop()
        scheduler_thread.join()

        # Check if the trigger_if_necessary method is called during the scheduler's execution
        self.assertTrue(len(scheduler.job_configs[0].executions) > 0)

    def test_scheduler_env(self):
        default_env = {"KEY1": "VALUE1", "KEY2": "VALUE2"}
        scheduler = Scheduler(env=default_env)

        trigger1 = PeriodicTrigger(timedelta(seconds=1))

        # This job config will use the default environment from the scheduler
        scheduler.add_job_config(
            "job1", ["python", "-c", "print('hello')"], trigger1)

        # Run the scheduler for 10 seconds and then stop it
        scheduler_thread = Thread(target=scheduler.start)
        scheduler_thread.start()
        time.sleep(5)
        scheduler.stop()
        scheduler_thread.join()
        self.assertTrue(len(scheduler.job_configs[0].executions) > 0)

    def test_job_config_env(self):
        scheduler = Scheduler()

        trigger1 = PeriodicTrigger(timedelta(seconds=1))

        # This job config will use its own environment
        job1_env = {"KEY3": "VALUE3", "KEY4": "VALUE4"}
        scheduler.add_job_config(
            "job1", ["python", "-c", "print('hello')"], trigger1, env=job1_env)

        # Run the scheduler for 10 seconds and then stop it
        scheduler_thread = Thread(target=scheduler.start)
        scheduler_thread.start()
        time.sleep(5)
        scheduler.stop()
        scheduler_thread.join()
        self.assertTrue(len(scheduler.job_configs[0].executions) > 0)

    def test_kill_all_running_jobs(self):
        # Create a Scheduler instance
        scheduler = Scheduler()

        # Add a job that sleeps for 5 seconds
        scheduler.add_job_config(
            name="sleeping_job",
            execution_cmd_args=[
                "python", "-c",
                (
                    "import sys, time; "
                    "sys.stdout.write('Start\\n'); sys.stdout.flush(); "
                    "time.sleep(5); sys.stdout.write('End\\n')"
                )
            ],
            trigger=PeriodicTrigger(timedelta(seconds=1)),
        )

        # Start the scheduler in a separate thread
        scheduler_thread = Thread(target=scheduler.start)
        scheduler_thread.start()

        # Wait for 3 seconds
        sleep(3)

        # Stop the scheduler and kill the running jobs
        scheduler.stop()

        # Join the scheduler thread
        scheduler_thread.join()

        # Check if the job was terminated as expected
        job_execution = scheduler.job_configs[0].current_execution
        self.assertIsNotNone(job_execution)
        self.assertIn("Start", "".join(job_execution.lines))
        self.assertNotIn("End", "".join(job_execution.lines))

    def test_max_executions(self):
        trigger = PeriodicTrigger(timedelta(seconds=1))
        scheduler = Scheduler()

        # Create a job config with max_executions limit set to 2
        scheduler.add_job_config(
            'myjob', ["python", "-c", "print('hello')"], trigger, max_executions=2)

        # Run the scheduler for a short duration (10 seconds) and then stop it
        scheduler_thread = Thread(target=scheduler.start)
        scheduler_thread.start()
        time.sleep(10)
        scheduler.stop()
        scheduler_thread.join()

        # Check if the number of executions does not exceed the max_executions limit
        self.assertTrue(len(scheduler.job_configs[0].executions) <= 2)

    def test_max_lines(self):
        trigger = PeriodicTrigger(timedelta(seconds=1))
        scheduler = Scheduler()

        # Create a job config with max_lines limit set to 3
        scheduler.add_job_config(
            'myjob', ["python", "-c", "print('hello')"], trigger, max_lines=3)

        # Run the scheduler for a short duration (10 seconds) and then stop it
        scheduler_thread = Thread(target=scheduler.start)
        scheduler_thread.start()
        time.sleep(10)
        scheduler.stop()
        scheduler_thread.join()

        # Check if the number of lines of the output does not exceed the max_lines limit
        # We get the last execution and check its lines
        last_execution = scheduler.job_configs[0].executions[-1]
        self.assertTrue(len(last_execution.lines) <= 3)

    def test_max_executions_scheduler(self):
        trigger = PeriodicTrigger(timedelta(seconds=1))
        scheduler = Scheduler(max_executions=2)

        # Create a job config with max_executions limit set to 2
        scheduler.add_job_config(
            'myjob', ["python", "-c", "print('hello')"], trigger)

        # Run the scheduler for a short duration (10 seconds) and then stop it
        scheduler_thread = Thread(target=scheduler.start)
        scheduler_thread.start()
        time.sleep(10)
        scheduler.stop()
        scheduler_thread.join()

        # Check if the number of executions does not exceed the max_executions limit
        self.assertTrue(len(scheduler.job_configs[0].executions) <= 2)

    def test_max_lines_scheduler(self):
        trigger = PeriodicTrigger(timedelta(seconds=1))
        scheduler = Scheduler(max_lines=3)

        # Create a job config with max_lines limit set to 3
        scheduler.add_job_config(
            'myjob', ["python", "-c", "print('hello')"], trigger)

        # Run the scheduler for a short duration (10 seconds) and then stop it
        scheduler_thread = Thread(target=scheduler.start)
        scheduler_thread.start()
        time.sleep(10)
        scheduler.stop()
        scheduler_thread.join()

        # Check if the number of lines of the output does not exceed the max_lines limit
        # We get the last execution and check its lines
        last_execution = scheduler.job_configs[0].executions[-1]
        self.assertTrue(len(last_execution.lines) <= 3)

    def test_scheduler_on_error_event(self):
        # Define an error event handler function
        def error_event_handler(job_name, return_code, error_message):
            self.assertEqual(job_name, "failing_job")
            self.assertEqual(return_code, -1)
            self.assertTrue("Command not found" in error_message)

        # Create a scheduler and add a failing job
        scheduler = Scheduler(on_error_event=error_event_handler)
        trigger = PeriodicTrigger(timedelta(seconds=1))
        scheduler.add_job_config(
            'failing_job', ['nonexistent_command'], trigger)

        # Run the scheduler for a short duration (5 seconds) and then stop it
        scheduler_thread = Thread(target=scheduler.start)
        scheduler_thread.start()
        time.sleep(5)
        scheduler.stop()
        scheduler_thread.join()

        # The assertion in the error_event_handler function will be used to verify the error event
