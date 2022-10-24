import json
from datetime import date, datetime, timedelta

import redis

from config.runtime_config import RuntimeConfig
from util.singleton import Singleton


class RedisAdapter(metaclass=Singleton):
    def __init__(self):
        self.pool = redis.ConnectionPool(host=RuntimeConfig.redis_host, port=RuntimeConfig.redis_port)

    @property
    def conn(self):
        if not hasattr(self, '_conn'):
            self.getConnection()
        return self._conn

    def getConnection(self):
        self._conn = redis.Redis(connection_pool=self.pool)

    def insert_sorted_list(self, key, value, score):
        """Insert a value by key and a score into a redis sorted list
        :param key: the name of the sorted list
        :param value: the value you want to insert
        :param score: a score that will be used to retrieve record by zrangebyscore"""

        self.conn.zadd(key, {value: score})

    def get_all_records(self):
        """Get all records from redis"""

        # Because this method must fetch all the records in sorted lists the score min and max must be -inf and inf
        records_list = [self.conn.zrangebyscore(key, float('-inf'), float('inf'))
                        for key in self.conn.scan_iter("*")]
        return [json.loads(record) for records_for_sorted_list in records_list
                for record in records_for_sorted_list]

    def get_records_by_crime_type(self, crime_type: str):
        """ Get records from redis based on crime type which is the name of sorted lists"""
        records = self.conn.zrangebyscore(crime_type, float("-inf"), float("inf"))
        return self.redis_results_to_json(records)

    def get_records_by_crime_date(self, crime_date: date):
        """ Get records from redis based on date which is fetched by zrangebyscore"""
        crime_date = datetime.combine(crime_date, datetime.min.time())
        crime_date_tomorrow = crime_date + timedelta(days=1)
        records_list = [self.conn.zrangebyscore(key, crime_date.timestamp(), crime_date_tomorrow.timestamp())
                        for key in self.conn.scan_iter("*")]
        return [json.loads(record) for records_for_sorted_list in records_list
                for record in records_for_sorted_list]

    def get_by_crime_type_and_date(self, crime_type: str, crime_date: date):
        """ Get records from redis based on crime type which is the name of sorted lists and
        crime date which is the score.
        by using sorted lists we can retrieve it fast."""
        crime_date = datetime.combine(crime_date, datetime.min.time())
        crime_date_tomorrow = crime_date + timedelta(days=1)
        records = self.conn.zrangebyscore(crime_type, crime_date.timestamp(), crime_date_tomorrow.timestamp())
        return self.redis_results_to_json(records)

    @staticmethod
    def redis_results_to_json(rows):
        """helper method to convert redis results to json"""
        return [json.loads(row) for row in rows]
