import os
from pathlib import Path
from sys import _getframe
from typing import Iterator
import json
from logging import getLogger

logger = getLogger()


class Config:
    """A class for handling configuration settings for the aiomql package.

    Keyword Args:
        **kwargs: Configuration settings as keyword arguments.
        Variables set this way supersede those set in the config file.

    Attributes:
        file (str): Path to the config file
        record_trades (bool): Whether to record trades or not
        filename (str): Name of the config file
        records_dir (str): Path to the directory where trade records are saved
        win_percentage (float): Percentage of profit to be considered a win
        account_number (int): Broker account number
        password (str): Broker password
        server (str): Broker server
        path (str): Path to terminal file

    Notes:
        By default the config class looks for a file named aiomql.json.
        You can change this by passing the filename keyword argument to the constructor.
        You can also specify a different file by passing the file keyword argument to the constructor.
        By passing reload=True to the load_config method, you can reload search again for the config file.
    """
    login: int = 0
    password: str = ""
    server: str = ""
    path: str = ""
    timeout: int = 60000
    record_trades: bool = True
    filename: str = "aiomql.json"
    file = None
    win_percentage: float = 0.85
    _load = 1
    records_dir = Path.home() / 'Documents' / 'Aiomql' / 'Trade Records'
    records_dir.mkdir(parents=True, exist_ok=True)
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, **kwargs):
        self.file = kwargs.get('file', None)
        self.filename = kwargs.get('filename', None) or self.filename
        kwargs.pop('file', None)
        kwargs.pop('filename', None)
        self.load_config(reload=False)
        self.set_attributes(**kwargs)

    @staticmethod
    def walk_to_root(path: str) -> Iterator[str]:
        
        if not os.path.exists(path):
            raise IOError('Starting path not found')
        
        if os.path.isfile(path):
            path = os.path.dirname(path)
        
        last_dir = None
        current_dir = os.path.abspath(path)
        while last_dir != current_dir:
            yield current_dir
            parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
            last_dir, current_dir = current_dir, parent_dir
    
    def find_config(self):
        current_file = __file__
        frame = _getframe()
        while frame.f_code.co_filename == current_file:
            if frame.f_back is None:
                return None
            frame = frame.f_back
        frame_filename = frame.f_code.co_filename
        path = os.path.dirname(os.path.abspath(frame_filename))
        
        for dirname in self.walk_to_root(path):
            check_path = os.path.join(dirname, self.filename)
            if os.path.isfile(check_path):
                return check_path
        return None
    
    def load_config(self, file: str = None, reload: bool = True):
        if not reload and self._load == 0:
            return

        self._load = 0

        if (file := (file or self.find_config())) is None:
            logger.warning('No Config File Found')
            return
        fh = open(file, mode='r')
        data = json.load(fh)
        fh.close()
        [setattr(self, key, value) for key, value in data.items()]

    def account_info(self) -> dict['login', 'password', 'server']:
        """Returns Account login details as found in the config object if available

           Returns:
               dict: A dictionary of login details
        """
        return {'login': self.login, 'password': self.password, 'server': self.server}
    
    def set_attributes(self, **kwargs):
        """Add attributes to the config object

        Keyword Args:
            **kwargs: Attributes to be added to the config object
        """
        [setattr(self, i, j) for i, j in kwargs.items()]
