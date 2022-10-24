import json
import os
from datetime import date
from datetime import datetime
from typing import Optional

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from adapter.bigquery_adapter import BigQueryAdapter
from adapter.redis_adapter import RedisAdapter
from config.runtime_config import RuntimeConfig

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = RuntimeConfig.credentials_file

router = APIRouter()


@router.get("/crimes")
async def list_crimes(crime_type: Optional[str] = None, crime_date: Optional[date] = None):
    """Get data from redis and return records in json format"""
    redis_adapter = RedisAdapter()
    if crime_type and crime_date:
        return redis_adapter.get_by_crime_type_and_date(crime_type=crime_type, crime_date=crime_date)
    elif crime_type:
        return redis_adapter.get_records_by_crime_type(crime_type=crime_type)
    elif crime_date:
        return redis_adapter.get_records_by_crime_date(crime_date=crime_date)
    else:
        redis_repository = RedisAdapter()
        return redis_repository.get_all_records()


@router.get("/data")
async def fetch_crimes(num_rows: Optional[int] = None):
    """Get data bigquery and insert the data into sorted list in redis"""
    bigquery_adapter = BigQueryAdapter(RuntimeConfig.bigquery_project, RuntimeConfig.bigquery_dataset)
    crime_details_list = bigquery_adapter.get_records(table_name=RuntimeConfig.bigquery_table,
                                                      num_rows=num_rows)
    crimes_details_json = jsonable_encoder(crime_details_list)

    # insert json data to redis by using sorted lists
    # the key is primary_type and the score is date formatted in timestamp format
    # the goal is to retrieve data by crime_type and date fast

    for crimes_detail_json in crimes_details_json:
        redis_adapter = RedisAdapter()
        redis_adapter.insert_sorted_list(key=crimes_detail_json['primary_type'],
                                         value=json.dumps(crimes_detail_json),
                                         score=datetime.fromisoformat(crimes_detail_json['date']).timestamp())
    return crime_details_list
