import os

from connectors.database import DBConnection
from connectors.storage import StorageConnection

FILE_TO_PROC = 'taxi_bi.csv'
BUCKET = 'brytlyt'
KEY = 'MG/taxi_bi.csv'
DB_CONFIG = 'config/database.ini'
TABLE_CREATE = 'plpgsql/create_taxi_table.sql'

if __name__ == "__main__":

    if not os.path.isfile(FILE_TO_PROC):
        StorageConnection.download_file(BUCKET, KEY, FILE_TO_PROC)
    else:
        print(f"{FILE_TO_PROC} exists!")

    DBConnection.connect(DB_CONFIG)
    result = DBConnection.execute_query("SELECT version()", True)

    print(result)
    
    DBConnection.execute_query("DROP TABLE IF EXISTS taxi")
    with open(TABLE_CREATE, 'r') as file_:
        query = file_.read()
        DBConnection.execute_query(query)
    
    DBConnection.load_from_file(FILE_TO_PROC)
