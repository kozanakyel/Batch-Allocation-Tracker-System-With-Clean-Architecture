import os
from dotenv import load_dotenv

load_dotenv()

PSQL_USER = os.getenv('PSQL_USER')
PSQL_PWD = os.getenv('PSQL_PWD')
PSQL_HOST = os.getenv('PSQL_HOST')
PSQL_PORT = os.getenv('PSQL_PORT')
PSQL_DB_NAME = os.getenv('PSQL_DB_NAME')

API_PORT = os.getenv('API_PORT')
API_HOST = os.getenv('API_HOST')

def get_postgres_uri():
    host = PSQL_HOST
    port = PSQL_PORT
    password = PSQL_PWD
    user, db_name = PSQL_USER, PSQL_DB_NAME
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = API_HOST
    port = API_PORT
    return f"http://{host}:{port}"