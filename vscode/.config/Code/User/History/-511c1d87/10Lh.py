import os
from sqlalchemy.engine import URL

DB_INIT_DATABASE = "personal_info" # os.getenv("DB_INIT_DATABASE")
DB_TYPE = "postgresql" # os.getenv("DB_TYPE")
DB_HOST = "127.0.0.1" # os.getenv("DB_HOST")
DB_PORT = "5432"  # os.getenv("DB_PORT")
DB_USER = "postgres"
DB_PASSWORD = "mysecretpassword" # os.getenv("DB_PASSWORD")

DB_URL = URL(drivername=DB_TYPE,username=DB_USER,password=DB_PASSWORD,host=DB_HOST,port=DB_PORT,database=DB_INIT_DATABASE)