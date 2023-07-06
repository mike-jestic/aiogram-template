from apscheduler.schedulers.asyncio import AsyncIOScheduler

from . import jobs

class ScheduleService(AsyncIOScheduler):
    def __init__(self, *, pending_jobs_interval: int = 60) -> None:
        super().__init__()
        self.pending_jobs_interval = pending_jobs_interval

    async def setup(self):
        self.add_job(jobs.some_jobe, 'interval', seconds=60)

        self.start()

    async def dispose(self):
        self.shutdown()
