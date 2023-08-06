import unittest
from datetime import datetime, timedelta
from urturn.trigger import PeriodicTrigger, TimeTrigger, ImmediateTrigger


class TestPeriodicTrigger(unittest.TestCase):

    def test_calculate_next_trigger(self):
        time_delta = timedelta(seconds=2)
        trigger = PeriodicTrigger(time_delta)
        now = datetime.utcnow()
        next_trigger = trigger.calculate_next_trigger()

        expected_next_trigger = now + time_delta
        self.assertAlmostEqual(next_trigger.timestamp(),
                               expected_next_trigger.timestamp(), delta=1)


class TestTimeTrigger(unittest.TestCase):

    def test_calculate_next_trigger(self):
        trigger_time = (datetime.utcnow() + timedelta(seconds=2)).time()
        trigger = TimeTrigger(trigger_time)
        now = datetime.utcnow()
        next_trigger = trigger.calculate_next_trigger()

        expected_next_trigger = datetime.combine(now.date(), trigger_time)
        if now.time() > trigger_time:
            expected_next_trigger += timedelta(days=1)

        self.assertAlmostEqual(next_trigger.timestamp(),
                               expected_next_trigger.timestamp(), delta=1)


class TestImmediateTrigger(unittest.TestCase):
    def test_calculate_next_trigger(self):
        trigger = ImmediateTrigger()
        now = datetime.utcnow()
        next_trigger = trigger.calculate_next_trigger()

        self.assertAlmostEqual(next_trigger.timestamp(),
                               now.timestamp(), delta=1)
