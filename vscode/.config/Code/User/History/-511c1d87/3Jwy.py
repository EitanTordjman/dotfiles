import os

DB_INIT_DATABASE = "personal_info" # os.getenv("DB_INIT_DATABASE")
DB_TYPE = "postgresql" # os.getenv("DB_TYPE")
DB_HOST = "127.0.0.1" # os.getenv("DB_HOST")
DB_PORT = "5432"  # os.getenv("DB_PORT")
DB_USER = "postgres"
DB_PASSWORD = "mysecretpassword" # os.getenv("DB_PASSWORD")
DB_URL = f"{DB_TYPE}://{DB_HOST}:{DB_PORT}"