import os
from abc import ABCMeta, abstractmethod
from typing import List
from typing import Optional

from google.cloud import bigquery
from google.cloud.bigquery.table import RowIterator

from config.runtime_config import RuntimeConfig

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = RuntimeConfig.credentials_file


class BaseBigqueryAdapter(metaclass=ABCMeta):
    @abstractmethod
    def get(self, table_name: str, num_rows: Optional[int] = None) -> RowIterator:
        """List the rows of the table"""
        pass

    @abstractmethod
    def get_records(self, table_name: str, num_rows: Optional[int] = None) -> List:
        """ Get all records from bigquery using pagination and returns list of records."""
        pass


class BigQueryAdapter(BaseBigqueryAdapter):
    def __init__(self, project_name, dataset_name):
        self.project_name = project_name
        self.dataset_name = dataset_name
        self.client = bigquery.Client()

    def get(self, table_name: str, num_rows: Optional[int] = None) -> RowIterator:
        table_id = f'{self.project_name}.{self.dataset_name}.{table_name}'
        table = self.client.get_table(table_id)
        results = self.client.list_rows(table, page_size=1000, max_results=num_rows)
        return results

    def get_records(self, table_name: str, num_rows: Optional[int] = None) -> List:
        crime_details_rows = self.get(table_name=table_name,
                                      num_rows=num_rows)
        crime_details_list = [crime_details_row for page in crime_details_rows.pages
                              for crime_details_row in page]
        return crime_details_list

