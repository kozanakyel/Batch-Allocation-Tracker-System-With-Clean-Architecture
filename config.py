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
    host = os.getenv('PSQL_HOST')
    port = 54321 if host == "127.0.0.1" else 5432
    password = os.getenv("PSQL_PWD")
    user, db_name = "PSQL_USER", "PSQL_DB_NAME"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = os.getenv("API_HOST")
    port = os.getenv("API_PORT")
    return f"http://{host}:{port}"