import sched
import time
from datetime import datetime, timedelta

from service.loggs import Loggs


class Scheduler:

    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def renew(self, my_function, server_dttime):
        self.scheduler.enter(self.schedule_next_minute(server_dttime), 1, my_function)
        self.scheduler.run()

    def schedule_next_minute(self, server_dttime):
        # initialize logs service
        loggs = Loggs().logger

        timer_min = 1  # 1 minute to waiting
        lazy_secs = 3  # plus seconds to waiting
        # Use Server time, not local time to update scheduler
        next_minute = (server_dttime + timedelta(minutes=timer_min)).replace(second=0, microsecond=0)
        # Wait lazy_secs seconds to receive data from server
        delay = (next_minute - server_dttime).total_seconds() + lazy_secs  # wait timer_min+lazy_secs seconds to turn
        # Ok If time adjusted with server_time now waiting for 5 minutes
        if delay >= 59:
            delay = ((5 - server_dttime.minute % 5) * 60) + lazy_secs - server_dttime.second
        loggs.info(
            f"\n\nServer time {server_dttime.strftime('%H:%M:%S')}, "
            f"Local time {datetime.now().strftime('%H:%M:%S')}, "
            f"Updating in {int(delay)} secs ....\n\n\n"
        )
        return delay
