import unittest
from datetime import datetime, timedelta
import time

from urturn.job import JobExecution, JobConfig
from urturn.trigger import PeriodicTrigger


def dummy_logging_callback(event, job_name, **kwargs):
    pass


class TestJobExecution(unittest.TestCase):

    def test_job_execution(self):
        # The command to be executed; here, we use "echo" to print a string.
        cmd_args = ["python", "-c", "print('Hello, World!')"]

        # Create a JobExecution instance with the command arguments.
        job_execution = JobExecution(
            'name', cmd_args, None, dummy_logging_callback, 50)

        # Start the job execution.
        job_execution.start()

        # Wait for the job execution to complete.
        job_execution.join()

        # Check if the output is as expected.
        self.assertEqual(job_execution.lines, ["Hello, World!\n"])

        # Check if there are no errors.
        self.assertEqual(job_execution.error_message, '')

        # Check if the return code is zero, indicating success.
        self.assertEqual(job_execution.return_code, 0)

        # Check if the duration is not None, indicating that the job has completed.
        self.assertIsNotNone(job_execution.duration)

    def test_job_execution_error(self):
        # The command to be executed; here, we use a non-existent command to raise an error.
        cmd_args = ["non_existent_command"]

        # Create a JobExecution instance with the command arguments.
        job_execution = JobExecution(
            'name', cmd_args, None, dummy_logging_callback)

        # Start the job execution.
        job_execution.start()

        # Wait for the job execution to complete.
        job_execution.join()

        # Check if there is an error message.
        self.assertIsNotNone(job_execution.error_message)

        # Check if the return code is non-zero, indicating an error.
        self.assertNotEqual(job_execution.return_code, 0)

        # Check if the duration is not None, indicating that the job has completed.
        self.assertIsNotNone(job_execution.duration)

    def test_job_execution_command_error(self):
        # The command to be executed; here, we use the "grep" command with an invalid option.
        cmd_args = ["python", "--invalid-option"]

        # Create a JobExecution instance with the command arguments.
        job_execution = JobExecution(
            'name', cmd_args, None, dummy_logging_callback)

        # Start the job execution.
        job_execution.start()

        # Wait for the job execution to complete.
        job_execution.join()

        # Check if there is an error message.
        self.assertIsNotNone(job_execution.error_message)

        # Check if the error message contains the expected error text.
        self.assertIn("invalid-option", job_execution.error_message.lower())

        # Check if the return code is non-zero, indicating an error.
        self.assertNotEqual(job_execution.return_code, 0)

        # Check if the duration is not None, indicating that the job has completed.
        self.assertIsNotNone(job_execution.duration)


class TestJobConfig(unittest.TestCase):

    def test_trigger_if_necessary(self):
        # The command to be executed; here, we use "echo" to print a string.
        cmd_args = ["python", "-c",
                    "print('Hello, World!')", "&", "SLEEP", "1"]

        # Create a PeriodicTrigger instance with a very small time delta (e.g., 1 second).
        trigger = PeriodicTrigger(time_delta=timedelta(seconds=1))

        # Create a JobConfig instance with a name, command arguments, and trigger.
        job_config = JobConfig("Test Job", cmd_args,
                               trigger, None, dummy_logging_callback, 50, 50)

        # The initial next_trigger_datetime should be set.
        self.assertIsNotNone(job_config.next_trigger_datetime)

        # Wait for a moment to let the trigger fire.
        time.sleep(1.1)

        # Call trigger_if_necessary with the current datetime.
        job_config.trigger_if_necessary(datetime.utcnow())

        # Check if the job was triggered and started.
        self.assertIsNotNone(job_config.current_execution)
        self.assertTrue(job_config.current_execution.is_alive())

        # Wait for the job execution to complete.
        job_config.current_execution.join()

        # Call trigger_if_necessary again, after the job has completed.
        job_config.trigger_if_necessary(datetime.utcnow())

        # Check if the job was marked as finished and a new trigger time was set.
        self.assertIsNone(job_config.current_execution)
        self.assertIsNotNone(job_config.next_trigger_datetime)
