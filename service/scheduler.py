import sched
import time
from datetime import datetime, timedelta


class Scheduler:

    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.from_date = datetime.now()

    def renew(self, myfunction):
        self.scheduler.enter(self.schedule_next_minute(), 1, myfunction)
        self.scheduler.run()

    def schedule_next_minute(self):
        now = datetime.now()
        repeat = 1
        next_minute = (now + timedelta(minutes=repeat)).replace(second=0, microsecond=0)
        delay = (next_minute - now).total_seconds() + 5  # wait repeat+5 seconds to turn
        print(f"\n\nupdating in {int(delay)} secs ....")
        return delay
