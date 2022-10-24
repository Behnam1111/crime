# Chicago Crime

Chicago Crime is a project based on Python FastAPI that fetch data from bigquery and by using a dashboard
made with streamlit you can see crimes in chicago and filter them by crime type a

## Installation


use docker-compose to run the application.


```bash
docker-compose up
```

## Usage
fetch data and insert it to redis by using
## GET

`fetch data and insert it to redis` [http://127.0.0.1:8000/data](#get-http://127.0.0.1:8000/data)

or

`fetch data limit number of rows and insert it to redis` [http://127.0.0.1:8000/data?num_rows=<num>](#get-http://127.0.0.1:8000/data?num_rows=<num>)

then you can go to the dashboard path and see the data on
[http://127.0.0.1:8501/](#get-http://127.0.0.1:8501/)



# API endpoints

These endpoints allow you to handle Stripe subscriptions for Publish and Analyze.
## GET

`Swagger` [http://127.0.0.1:8000/docs](#get-http://127.0.0.1:8000/docs)

```