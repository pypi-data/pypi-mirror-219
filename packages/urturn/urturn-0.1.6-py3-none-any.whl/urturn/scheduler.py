"""Scheduler for execution jobs concurrently"""

from typing import List, Optional, Dict
import time
from datetime import datetime

from .trigger import Trigger
from .job import JobConfig, JobEvent


class Scheduler:
    """Scheduler class that runs jobs according to their configurations and triggers.

    Attributes:
        job_configs (List[JobConfig]): A list of job configurations to be executed.
        running (bool): A flag indicating whether the scheduler is running or not.
        env (Optional[Dict[str, str]]): A dictionary of environment variables to be used as the
            default for all job configs.
    """

    def __init__(self, env: Optional[Dict[str, str]] = None,
                 on_logging_event=None, on_error_event=None,
                 max_executions: int = 30, max_lines: int = 500) -> None:
        """Initialize a Scheduler instance with an empty list of job configurations and set the
        running attribute to False.

        Attributes:
            env (Optional[Dict[str, str]]): A dictionary of environment variables to be used as the
                default for all job configs.
        """
        self.job_configs: List[JobConfig] = []
        self.running: bool = False
        self.env: Optional[Dict[str, str]] = env
        self.on_logging_event = on_logging_event
        self.on_error_event = on_error_event
        self.max_executions = max_executions
        self.max_lines = max_lines

    def _on_logging_event_callback(self, event, job_name, **kwargs):
        if self.on_logging_event:
            self.on_logging_event(event, job_name, **kwargs)

        if event == JobEvent.ERROR and self.on_error_event:
            self.on_error_event(
                job_name, kwargs['return_core'], kwargs['error_message'])

    def add_job_config(
        self,
        name: str,
        execution_cmd_args: List[str],
        trigger: Trigger,
        env: Optional[Dict[str, str]] = None,
        max_executions: int = None,
        max_lines: int = None,
    ):
        """Add a job configuration to the scheduler.

        Args:
            name (str): The name of the job.
            execution_cmd_args (List[str]): The list of command arguments to be executed.
            trigger (Trigger): The trigger associated with the job.
        """
        env = env or self.env
        max_executions = max_executions or self.max_executions
        max_lines = max_lines or self.max_lines
        self.job_configs.append(JobConfig(
            name,
            execution_cmd_args,
            trigger,
            env,
            self._on_logging_event_callback,
            max_executions,
            max_lines,
        ))

    def start(self):
        """Start the scheduler, continuously checking and executing jobs according to their
        triggers.

        The scheduler runs in an infinite loop, checking each job's trigger and executing the job
        if necessary. The loop can be stopped by calling the `stop` method.
        """
        self.running = True
        while self.running:
            utc_now = datetime.utcnow()
            min_trigger = min(
                map(lambda x: x.next_trigger_datetime, self.job_configs))
            for job_conf in self.job_configs:
                print(job_conf.name)
                job_conf.trigger_if_necessary(utc_now)
            print(f'loop {min_trigger-utc_now}')
            time.sleep(1)

    def _kill_all_running_jobs(self):
        for job_conf in self.job_configs:
            if not job_conf.current_execution:
                continue

            job_conf.current_execution.process.kill()

    def stop(self):
        """Stop the scheduler's loop.

        Sets the running attribute to False, causing the scheduler's loop to terminate.
        """
        self._kill_all_running_jobs()
        self.running = False
