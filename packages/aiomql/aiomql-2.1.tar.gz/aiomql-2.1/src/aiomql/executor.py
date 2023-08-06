import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Sequence

from .strategy import Strategy
from .symbol import Symbol


class Executor:
    """Executor class for running multiple strategies on multiple symbols concurrently.

    Attributes:
        executor (ThreadPoolExecutor): The executor object.
        workers (list): List of strategies.

    """
    def __init__(self):
        self.executor = ThreadPoolExecutor
        self.workers: list[type(Strategy)] = []

    def add_workers(self, strategies: Sequence[type(Strategy)]):
        """Add multiple strategies at once

        Args:
            strategies (Sequence[Strategy]): A sequence of strategies.
        """
        self.workers.extend(strategies)

    def remove_workers(self, *symbols: Sequence[Symbol]):
        """Removes any worker running on a symbol not successfully initialized.
        
        Args:
            *symbols: Successfully initialized symbols.
        """
        self.workers = [worker for worker in self.workers if worker.symbol in symbols]

    def add_worker(self, strategy: type(Strategy)):
        """Add a strategy instance to the list of workers

        Args:
            strategy (Strategy): A strategy object
        """
        self.workers.append(strategy)

    @staticmethod
    def run(strategy: type(Strategy)):
        """Wraps the coroutine trade method of each strategy with 'asyncio.run'.

        Args:
            strategy (Strategy): A strategy object
        """
        asyncio.run(strategy.trade())

    async def execute(self, workers: int = 0):
        """Run the strategies with a threadpool executor.

        Args:
            workers: Number of workers to use in executor pool. Defaults to zero which uses all workers.

        Notes:
            No matter the number specified, the executor will always use a minimum of 5 workers.
        """
        workers = workers or len(self.workers)
        workers = max(workers, 5)
        loop = asyncio.get_running_loop()
        with self.executor(max_workers=workers) as executor:
            [loop.run_in_executor(executor, self.run, worker) for worker in self.workers]
