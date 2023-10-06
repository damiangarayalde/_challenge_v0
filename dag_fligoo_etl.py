import os

from functools import wraps
from datetime import datetime, timedelta
import requests
import pandas as pd

from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

from dotenv import dotenv_values
from sqlalchemy import create_engine, inspect


# # Define the default_args for the DAG
# default_args = {
#     'owner': 'damian',
#     'start_date': datetime(2023, 10, 5),
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }

# # Define the DAG
# dag = DAG(
#     'flight_data_etl_v0',
#     default_args=default_args,
#     start_date=datetime(2023, 10, 5),
#     schedule_interval=timedelta(minutes=10),
#     catchup=False,  # Disable catchup to avoid running missed intervals
# )

args = {"owner": "Airflow", "start_date": days_ago(1)}

dag = DAG(dag_id="dag_fligoo_etl_v2",
          default_args=args, schedule_interval=None)


def logger(func):
    from datetime import datetime, timezone

    @wraps(func)
    def wrapper(*args, **kwargs):
        called_at = datetime.now(timezone.utc)
        print(f">>> Running {func.__name__!r} function. Logged at {called_at}")
        to_execute = func(*args, **kwargs)
        print(
            f">>> Function: {func.__name__!r} executed. Logged at {called_at}")
        return to_execute

    return wrapper


DATASET_URL = "http://api.aviationstack.com/v1/flights"


CONFIG = dotenv_values(".env")
if not CONFIG:
    CONFIG = os.environ


@logger
def connect_db():
    print("Connecting to DB")
    connection_uri = "postgresql+psycopg2://{}:{}@{}:{}".format(
        CONFIG["POSTGRES_USER"],
        CONFIG["POSTGRES_PASSWORD"],
        CONFIG["POSTGRES_HOST"],
        CONFIG["POSTGRES_PORT"],
    )

    engine = create_engine(connection_uri, pool_pre_ping=True)
    engine.connect()
    return engine


@logger
def extract(dataset_url):
    print(f"Reading dataset from {dataset_url}")

    params = {
        # CONFIG["API_ACCESS_KEY"],
        'access_key': 'b9bae4850fdd4c65e655eac05ce4c4d1',
        'limit': 100
        # ,
        #  'flight_status': 'active'
    }

    api_result = requests.get(dataset_url, params)
    api_response = api_result.json()

    df = pd.json_normalize(api_response['data'])

    return df


@logger
def transform(df):
    print("Transforming data")

    df = df[['flight_date', 'flight_status', 'departure.airport', 'departure.timezone',
             'arrival.airport', 'arrival.timezone', 'arrival.terminal', 'airline.name', 'flight.number']]

    df.columns = ['flight_date', 'flight_status', 'departure_airport', 'departure_timezone',
                  'arrival_airport', 'arrival_timezone', 'arrival_terminal', 'airline_name', 'flight_number']

    df['departure_timezone'] = df['departure_timezone'].str.replace('/', ' - ')
    df['arrival_timezone'] = df['arrival_timezone'].str.replace('/', ' - ')

    return df


@logger
def check_table_exists(table_name, engine):
    if table_name in inspect(engine).get_table_names():
        print(f"{table_name!r} exists in the DB!")
    else:
        print(f"{table_name} does not exist in the DB!")


@logger
def load_to_db(df, table_name, engine):
    print(f"Loading dataframe to DB on table: {table_name}")
    df.to_sql(table_name, engine, if_exists="replace")


@logger
def tables_exists():
    db_engine = connect_db()
    print("Checking if tables exists")
    check_table_exists("testdata", db_engine)
    db_engine.dispose()


@logger
def etl():
    db_engine = connect_db()

    raw_df = extract(DATASET_URL)
    raw_table_name = "testdata"

    raw_df = transform(raw_df)

    load_to_db(raw_df, raw_table_name, db_engine)

    db_engine.dispose()


with dag:
    run_etl_task = PythonOperator(task_id="run_etl_task", python_callable=etl)
    run_tables_exists_task = PythonOperator(
        task_id="run_tables_exists_task", python_callable=tables_exists)

    run_etl_task >> run_tables_exists_task
