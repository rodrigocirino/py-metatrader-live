import sched
import time
from datetime import datetime


class scheduler:

    def __init__(self, interval):
        self.interval = interval
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.from_date = datetime.now()

    def create_scheduler(self, myfunction):
        self.scheduler.enter(self.interval, 1, myfunction)
        self.scheduler.run()
