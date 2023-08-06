"""Classes for triggering jobs on a schedule
"""

from datetime import time, datetime, timedelta


class Trigger:
    """Abstract Trigger Class
    """

    def calculate_next_trigger(self) -> datetime:
        """Calculates the next time the trigger fill fire

        Returns:
            datetime: _description_
        """
        raise NotImplementedError


class PeriodicTrigger(Trigger):
    """PeriodicTrigger class that triggers a job at fixed intervals.

    Attributes:
        time_delta (timedelta): The interval between triggers.
    """

    def __init__(self, time_delta: timedelta) -> None:
        """Initialize a PeriodicTrigger instance with the given time delta.

        Args:
            time_delta (timedelta): The interval between triggers.
        """
        super().__init__()
        self.time_delta = time_delta

    def calculate_next_trigger(self):
        """Calculate the next trigger time based on the current time and the time_delta attribute.

        Returns:
            datetime: The next trigger time as a datetime object.
        """
        return datetime.utcnow() + self.time_delta


class TimeTrigger(Trigger):
    """TimeTrigger class that triggers a job at a specific time every day.

    Attributes:
        trigger_time (time): The time of day when the job should be triggered.
    """

    def __init__(self, trigger_time: time) -> None:
        """Initialize a TimeTrigger instance with the given trigger time.

        Args:
            trigger_time (time): The time of day when the job should be triggered.
        """
        super().__init__()
        self.trigger_time = trigger_time

    def calculate_next_trigger(self):
        """Calculate the next trigger time based on the current date and the trigger_time attribute.

        Returns:
            datetime: The next trigger time as a datetime object.
        """
        now = datetime.utcnow()
        trigger_datetime = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=self.trigger_time.hour,
            minute=self.trigger_time.minute,
            second=self.trigger_time.second,
            microsecond=self.trigger_time.microsecond
        )

        if now < trigger_datetime:
            return trigger_datetime
        else:
            return trigger_datetime + timedelta(days=1)


class ImmediateTrigger(Trigger):
    """ImmediateTrigger class that fires the trigger immediately.

    The ImmediateTrigger is a trigger that calculates its next trigger time as the current time,
    causing the associated job to be executed as soon as possible.
    """

    def calculate_next_trigger(self) -> datetime:
        """Calculates the next time the trigger will fire by returning the current time.

        Returns:
            datetime: The current UTC time.
        """
        return datetime.utcnow()
