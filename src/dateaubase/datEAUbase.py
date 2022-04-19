from urllib import parse

import sqlalchemy
import yaml
from sqlalchemy import create_engine

from tables import ValueTable


def connect_local(server: str, database: str) -> sqlalchemy.engine:
    engine = create_engine(f'mssql+pyodbc://{server}:1433/{database}?driver=ODBC+Driver+17+for+SQL+Server', connect_args={'connect_timeout': 2}, fast_executemany=True)
    print(f'Remote connection: {engine.url}')
    return engine


def connect_remote(server: str, database: str, login_file: str) -> sqlalchemy.engine:
    with open(login_file) as f:
        secrets = yaml.safe_load(f)
        username = secrets["dateaubase"]["username"].strip()
        password = parse.quote_plus(secrets["dateaubase"]["password"].strip())
    engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}:1433/{database}?driver=ODBC+Driver+17+for+SQL+Server', connect_args={'connect_timeout': 2}, fast_executemany=True)
    print(f'Remote connection: {engine.url}')
    engine.connect()
    return engine


def get_last_value_id(db_engine: sqlalchemy.engine) -> int:
    query = 'SELECT MAX(Value_ID) FROM dbo.value'
    result = db_engine.execute(query).fetchone()
    return result[0]


def get_last_value_id_for_variable(db_engine: sqlalchemy.engine, meta_ID: int) -> int:
    query = f'SELECT TOP 1 Value_ID FROM dbo.value WHERE Metadata_ID = {meta_ID} ORDER BY [Timestamp] DESC'

    if result := db_engine.execute(query).fetchone():
        return result[0]
    return 0


def get_last_timestamp_for_variable(db_engine: sqlalchemy.engine, meta_ID: int) -> int:
    query = f'SELECT TOP 1 Timestamp FROM dbo.value WHERE Metadata_ID = {meta_ID} ORDER BY [Timestamp] DESC'

    if result := db_engine.execute(query).fetchone():
        return result[0]
    return 0


def engine_runs(engine: sqlalchemy.engine) -> bool:
    try:
        _ = get_last_value_id(engine)
    except sqlalchemy.exc.DBAPIError:
        return False
    else:
        return True


def send_to_db(df: ValueTable, db_engine: sqlalchemy.engine) -> None:
    '''stores df in SQL table dbo.value'''
    df.to_sql('value', con=db_engine, if_exists='append', index=False)
