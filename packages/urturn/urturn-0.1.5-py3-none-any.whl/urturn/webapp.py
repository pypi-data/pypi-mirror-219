"""Webapp for displaying the scheduler and job status.
"""
from threading import Thread
import os

from flask import Flask, render_template
from flask_socketio import SocketIO

from .scheduler import Scheduler


class SchedulerWebApp:
    """A web application that displays the current status of the scheduler and its job
        configurations.

    Attributes:
        scheduler (Scheduler): The scheduler instance.
        app (Flask): The Flask web application instance.
    """

    def __init__(self, scheduler: Scheduler):
        """Initialize a SchedulerWebApp instance.

        Args:
            scheduler (Scheduler): The scheduler instance.
        """
        self.scheduler = scheduler
        self.scheduler.on_logging_event = self.on_logging_event
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.urandom(24)
        self.socketio = SocketIO(self.app)
        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule("/job_config/<job_name>",
                              "job_config", self.job_config)

    def on_logging_event(self, event, job_name: str, **kwargs):
        """
        Handles the logging events emitted during the execution of jobs and sends these events to
        the client through the websocket.

        Args:
            event (JobEvent): An instance of JobEvent representing the type of the event.
            job_name (str): The name of the job that emitted the event.
            **kwargs: Additional event data.

        This function takes the event, job name, and any additional event data, packages it into a
        dictionary, and emits it to the client over the websocket connection. The event's value
        (a string representation of the event) is used as the event name for the emit function.
        """
        data = {
            "job_name": job_name,
        }
        data.update(kwargs)

        self.socketio.emit(event.value, data)

    def index(self):
        """Render the index page showing the overall status of the scheduler.

        Returns:
            str: The rendered HTML of the index page.
        """
        return render_template("index.html", scheduler=self.scheduler)

    def job_config(self, job_name):
        """Render the job configuration page for a specific job.

        Args:
            job_name (str): The name of the job configuration.

        Returns:
            str: The rendered HTML of the job configuration page, or an error message and 404 status
                if the job is not found.
        """
        job = next(
            (job_conf for job_conf in self.scheduler.job_configs if job_conf.name == job_name),
            None)
        if job is None:
            return "Job not found", 404

        return render_template("job_config.html", job=job)

    def run(self, host=None, port=8000, debug=False):
        """Start the web application with the specified debug mode.

        Args:
            debug (bool, optional): Run the web application in debug mode. Defaults to False.
        """

        # Start the scheduler in a separate thread
        scheduler_thread = Thread(target=self.scheduler.start)
        scheduler_thread.start()

        self.app.run(host=host, port=port, debug=debug, use_reloader=False)
