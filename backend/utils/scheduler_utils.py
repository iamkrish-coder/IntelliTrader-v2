import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import utc

from backend.utils.logging_utils import *


class Scheduler:

    def __init__(self, configuration, task_instance=None, runtime=None, mode='blocking'):
        self._scheduler = None
        self.configuration = configuration
        self.task_instance = task_instance
        self.task_runtime = runtime
        self.mode = mode

    def get_scheduled_runtime(self):
        """
        Retrieves the scheduled runtime from the configuration.

        Args:

        Returns:
            str: The parsed runtime string (e.g., '*/5 minute', '*/2 hour').

        Raises:
            ValueError: If 'runtime' key is missing or has an invalid format.
        """
        runtime = self.configuration.get('runtime')
        if not runtime:
            raise ValueError("Missing 'runtime' configuration for scheduling.")
        return runtime

    def start_scheduler(self, task_instance=None):
        """Reads runtime configuration, task object, schedules runtime and mode of scheduler."""
        if self.task_runtime is None or "minute" not in self.task_runtime or "hour" not in self.task_runtime:
            self.task_runtime = self.get_scheduled_runtime()

        if self.task_instance is None:
            self.task_instance = task_instance

        if self.mode == "blocking":
            self.schedule_task_blocking(self.task_instance, self.task_runtime)
        elif self.mode == "background":
            self.schedule_task_background(self.task_instance, self.task_runtime)
        elif self.mode == "asyncio":
            asyncio.create_task(self.run_async_function())
        else:
            log_error("Invalid scheduler mode. Expected 'blocking', 'background', or 'asyncio'.")

    async def run_async_function(self):
        if self.mode == "asyncio":
            await self.schedule_task_asyncio(self.task_instance, self.task_runtime)

    # ASYNCIO ##########################################################################
    # ASYNCIO ##########################################################################
    # ASYNCIO ##########################################################################

    async def schedule_task_asyncio(self, task_instance, task_runtime):
        """
        Schedules the task initialization using an AsyncIOScheduler (requires asyncio).

        Args:
            task_instance (object): The object containing the task initialization function.
            task_runtime (str): The parsed runtime string (e.g., '*/5 minute', '*/2 hour').

        Raises:
            ValueError: If the runtime format is invalid (expected 'minute' or 'hour').
        """
        self._scheduler = AsyncIOScheduler()
        try:
            await self.run_schedule_task_async(task_instance, task_runtime)
        except (KeyboardInterrupt, SystemExit):
            self._scheduler.shutdown()

    async def run_schedule_task_async(self, task_instance, task_runtime):
        """
        Async Function.

        Args:
            task_instance (object): The object containing the task initialization function.
            task_runtime (str): The parsed runtime string (e.g., '*/5 minute', '*/2 hour').

        Raises:
            ValueError: If the runtime format is invalid (expected 'minute' or 'hour').
        """
        if "minute" in task_runtime:
            minute = int(task_runtime.split("minute")[0])
            minute = int(1)
            self._scheduler.add_job(task_instance.initialize, trigger='cron', minute=f'*/{minute}', timezone=utc)
        elif "hour" in task_runtime:
            hrs = int(task_runtime.split("hour")[0])
            self._scheduler.add_job(task_instance.initialize, trigger='cron', hour=f'*/{hrs}', timezone=utc)
        else:
            raise ValueError("Invalid format for 'runtime'. Expected 'minute' or 'hour'.")

        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        self._scheduler.start()

    # BLOCKING ##########################################################################
    # BLOCKING ##########################################################################
    # BLOCKING ##########################################################################

    def schedule_task_blocking(self, task_instance, task_runtime):
        """
        Schedules the task initialization using a BlockingScheduler.

        Args:
            task_instance (object): The object containing the task initialization function.
            task_runtime (str): The parsed runtime string (e.g., '*/5 minute', '*/2 hour').

        Raises:
            ValueError: If the runtime format is invalid (expected 'minute' or 'hour').
        """
        self._scheduler = BlockingScheduler()
        try:
            if "minute" in task_runtime:
                minute = int(task_runtime.split("minute")[0])
                self._scheduler.add_job(task_instance.initialize, trigger='cron', minute=f'*/{minute}', timezone=utc)
            elif "hour" in task_runtime:
                hrs = int(task_runtime.split("hour")[0])
                self._scheduler.add_job(task_instance.initialize, trigger='cron', hour=f'*/{hrs}', timezone=utc)
            else:
                raise ValueError("Invalid format for 'runtime'. Expected 'minute' or 'hour'.")

            print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
            self._scheduler.start()

        except (KeyboardInterrupt, SystemExit):
            self._scheduler.shutdown()

    # BACKGROUND ##########################################################################
    # BACKGROUND ##########################################################################
    # BACKGROUND ##########################################################################

    def schedule_task_background(self, task_instance, task_runtime):
        """
        Schedules the task initialization using a BackgroundScheduler.

        Args:
            task_instance (object): The object containing the task initialization function.
            task_runtime (str): The parsed runtime string (e.g., '*/5 minute', '*/2 hour').

        Raises:
            ValueError: If the runtime format is invalid (expected 'minute' or 'hour').
        """
        self._scheduler = BackgroundScheduler()
        try:
            if "minute" in task_runtime:
                minute = int(task_runtime.split("minute")[0])
                self._scheduler.add_job(task_instance.initialize, trigger='cron', minute=f'*/{minute}', timezone=utc)
            elif "hour" in task_runtime:
                hrs = int(task_runtime.split("hour")[0])
                self._scheduler.add_job(task_instance.initialize, trigger='cron', hour=f'*/{hrs}', timezone=utc)
            else:
                raise ValueError("Invalid format for 'runtime'. Expected 'minute' or 'hour'.")

            print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
            self._scheduler.start()

        except (KeyboardInterrupt, SystemExit):
            self._scheduler.shutdown()
