from loguru import logger
# from rich import inspect, print
import os
import csv
import time
import shutil
# import pandas as pd
from pyarrow import csv
import pyarrow.feather as feather
# import MySQLdb
import turbodbc

from config import Config
from .aircraft import Aircraft
from .airport import Airport
from .route import Route

class API:
    def __init__(self, config: Config):
        logger.debug('initializing API')
        self.config = config
        
        # if self.config.db_odbc_copy_ini:
        #     shutil.copy(
        #         os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'odbc.ini'),
        #         os.path.join(os.path.expanduser('~'), '.odbc.ini')
        #     )
        logger.critical(__name__)
        con = turbodbc.connect(dsn="testing")
        print(con)
        # with turbodbc.connect(dsn='testing') as self.con:
        #     self.cur = self.con.cursor()
        #     self.cur.execute("SHOW TABLES;")
        #     tables = [t[0] for t in self.cur.fetchall()]
        #     print(tables)
        #     self.create_database()

    def _path(self, *path) -> str:
        return os.path.join(os.path.dirname(__file__), *path)

    def __set_aircrafts(self):
        with open(self._path('data', 'aircrafts.csv'), 'r') as f:
            self.aircrafts = tuple(Aircraft(*r) for r in csv.reader(f))
        
        self.aircraft_shortname_hashtable = {}
        for i, a in enumerate(self.aircrafts):
            self.aircraft_shortname_hashtable[a.a_shortname] = i

    def __set_airports(self):
        with open(self._path('data', 'airports.csv'), 'r') as f:
            self.airports = tuple(Airport(*r) for r in csv.reader(f))
            logger.debug('finished loading airports')

        self.airport_icao_hashtable = {}
        self.airport_iata_hashtable = {}
        self.airport_id_hashtable = {}
        for i, a in enumerate(self.airports):
            self.airport_icao_hashtable[a.icao] = i
            self.airport_iata_hashtable[a.iata] = i
            self.airport_id_hashtable[a.id] = i

    def __set_routes(self):
        
        logger.debug('finished loading routes')

    def __get_sql_statement(self, filename: str) -> str:
        with open(self._path('sql', filename), 'r') as f:
            return f.read()

    def create_database(self):
        self.cur.execute("SHOW TABLES;")
        tables = [t[0] for t in self.cur.fetchall()]
        if 'routes' not in tables:
            self.cur.execute(self.__get_sql_statement('create_routes.sql'))
            self.con.commit()
            # tmp_routes_file = self._path('data', '_routes.csv')
            tbl = feather.read_table(self._path('data', 'routes'))
            print(tbl)
            logger.debug('finished decompressing')
            # self.cur.execute(f"LOAD DATA LOCAL INFILE '{tmp_routes_file}' INTO TABLE routes FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';")
            # os.remove(tmp_routes_file)
            self.con.commit()
            logger.debug('inserted routes table')
        logger.debug('all done')