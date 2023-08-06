"""Define Jobs to be executed
"""

from typing import List, Dict, Optional
from threading import Thread
import subprocess
import io
import time
from datetime import datetime
from enum import Enum

from .trigger import Trigger


class JobEvent(Enum):
    """
    An enumeration representing the different types of events that can occur during the execution of
        a job.

    Attributes:
        STARTED (str): Represents the event when a job starts executing.
        NEW_LINE (str): Represents the event when a new line of output is produced by the job.
        STOPPED (str): Represents the event when a job stops executing.
        ERROR (str): Represents the event when an error occurs during the execution of a job.
    """
    STARTED = 'STARTED'
    NEW_LINE = 'NEW_LINE'
    STOPPED = 'STOPPED'
    ERROR = 'ERROR'


class JobExecution(Thread):
    """Class that executes a job for a single time in a separate thread.

    Attributes:
        execution_cmd_args (List[str]): The command arguments for executing the job.
        lines (List[str]): The output lines captured from the job execution.
        error_message (str): The error message captured from the job execution, if any.
        return_code (int): The return code from the job execution.
        duration (float): The duration of the job execution in seconds.
    """

    def __init__(
        self,
        job_name,
        execution_cmd_args: List[str],
        env: Optional[Dict[str, str]] = None,
        on_logging_event=None,
        max_lines: int = None,
    ) -> None:
        """Class that executes a job for a single time

        Attributes:
            execution_cmd_args (List[str]): The list of command arguments to be executed.
            env (Optional[Dict[str, str]]): A dictionary of environment variables to be used for
                this job execution.
        """
        super().__init__(target=self._trigger_and_log)
        self.job_name = job_name
        self.execution_cmd_args = execution_cmd_args
        self.max_lines = max_lines
        self.lines = []
        self.error_message = None
        self.return_code = None
        self.duration = None
        self.env = env
        self.process = None
        self.on_logging_event = on_logging_event

    def _execute(self) -> None:
        """Execute the job using a subprocess and yield the output lines.

        This method also captures the return code and error message, if any.
        """
        try:
            self.process = subprocess.Popen(  # pylint: disable=consider-using-with
                args=self.execution_cmd_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=self.env,
            )
        except FileNotFoundError:
            self.error_message = f"Command not found: {self.execution_cmd_args[0]}"
            self.return_code = -1
            return

        for line in io.TextIOWrapper(self.process.stdout, encoding="utf-8", errors='ignore'):
            yield line

        poll_ret = None
        while poll_ret is None:
            poll_ret = self.process.poll()

        self.return_code = self.process.returncode

        self.error_message = self.process.stderr.read().decode()

    def _trigger_and_log(self) -> None:
        """Execute the job, log its output lines, and measure its duration."""
        self.on_logging_event(JobEvent.STARTED, self.job_name)

        start_time = time.time()
        for line in self._execute():
            self.on_logging_event(JobEvent.NEW_LINE, self.job_name, line=line)
            self.lines.append(line)
            while len(self.lines) > self.max_lines:
                self.lines.pop(0)
        end_time = time.time()

        self.duration = end_time-start_time

        if self.return_code == 0:
            self.on_logging_event(
                JobEvent.STOPPED, self.job_name, duration=self.duration)
        else:
            self.on_logging_event(JobEvent.ERROR, self.job_name,
                                  return_core=self.return_code, error_message=self.error_message)


class JobConfig:
    """Class that configures a job execution and triggers it if necessary.

    Attributes:
        name (str): The name of the job.
        execution_cmd_args (List[str]): The command arguments for executing the job.
        trigger (Trigger): The trigger used to determine when the job should be executed.
        next_trigger_datetime (datetime): The next scheduled trigger time for the job.
        executions (List[JobExecution]): A list of past job executions.
        current_execution (JobExecution): The currently running job execution, if any.
        env (Optional[Dict[str, str]]): A dictionary of environment variables to be used for
            this job config.
    """

    def __init__(
        self,
        name: str,
        execution_cmd_args: List[str],
        trigger: Trigger,
        env: Optional[Dict[str, str]] = None,
        on_logging_event=None,
        max_executions: int = None,
        max_lines: int = None,
    ) -> None:
        """Class that configures a job execution and triggers them if necessary

        Attributes:
            name (str): The name of the job.
            execution_cmd_args (List[str]): The list of command arguments to be executed.
            trigger (Trigger): The trigger associated with the job.
            env (Optional[Dict[str, str]]): A dictionary of environment variables to be used for
                this job config.
        """
        self.name = name
        self.execution_cmd_args = execution_cmd_args
        self.trigger = trigger
        self.env = env
        self.on_logging_event = on_logging_event
        self.max_executions = max_executions
        self.max_lines = max_lines

        self.next_trigger_datetime = trigger.calculate_next_trigger()
        self.executions = []
        self.current_execution = None

    def trigger_if_necessary(self, current_datetime: datetime):
        """Handles the triggering logic of the job. Sets a new trigger time if necessary.

        This method checks if the job is currently running or if the current datetime is
        past the next_trigger_datetime. If the job is not running and it's time to trigger
        the job, this method starts a new JobExecution instance.

        Args:
            current_datetime (datetime): The current datetime provided from outside.
        """
        if self.current_execution and self.current_execution.is_alive():
            return

        if self.current_execution and not self.current_execution.is_alive():
            self.executions.append(self.current_execution)
            while len(self.executions) > self.max_executions:
                self.executions.pop(0)
            self.current_execution = None
            self.next_trigger_datetime = self.trigger.calculate_next_trigger()
            return

        if current_datetime > self.next_trigger_datetime and not self.current_execution:
            self.current_execution = JobExecution(
                self.name,
                self.execution_cmd_args,
                self.env,
                self.on_logging_event,
                self.max_lines,
            )
            self.current_execution.start()
            return
