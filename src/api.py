import os
import csv
import rich
import time
from .aircraft import Aircraft

class API:
    def __init__(self):
        self._success('started api')
        self.load_planes()

    def _success(self, text):
        rich.print(f'[green]{time.time()} INFO: {text}[/]')

    def _path(self, *path):
        return os.path.join(os.path.dirname(__file__), *path)

    def load_planes(self):
        with open(self._path('data', 'aircrafts.csv'), 'r') as f:
            self.aircrafts = [Aircraft(*r) for r in csv.reader(f)]
        
        rich.inspect(self.aircrafts)
        self._success('finished loading planes!')

    # def laod_airports(self):
    #     with open(os.path.join(os.path.dir))