import asyncio
import csv
from logging import getLogger

from .core.config import Config

logger = getLogger()


class Result:
    """A base class for handling trade results and strategy parameters for record keeping and reference purpose.
    The data property must be implemented in the subclass

    Attributes:
        config: The configuration object
        name: Any desired name for the result csv file
    """
    config = Config()

    def __init__(self, name: str):
        self.name = name

    @property
    def data(self) -> dict:
        """A dict representing data to be saved in the csv file.

        Returns (dict): A dict of data to be saved
        """
        return {}

    async def to_csv(self):
        """Record trade results and associated parameters as a csv file
        """
        try:
            file = self.config.records_dir / f"{self.name}.csv"
            exists = file.exists()
            with open(file, 'a', newline='') as fh:
                writer = csv.DictWriter(fh, fieldnames=sorted(list(self.data.keys())), extrasaction='ignore', restval=None)
                if not exists:
                    writer.writeheader()
                writer.writerow(self.data)
        except Exception as err:
            logger.error(f'Error: {err}. Unable to save trade results')

    async def save(self):
        """Save trade results and associated parameters as a csv file in a separate thread
        """
        loop = asyncio.get_running_loop()
        asyncio.run_coroutine_threadsafe(self.to_csv(), loop)
