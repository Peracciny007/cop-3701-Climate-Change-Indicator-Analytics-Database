import pandas as pd
import oracledb
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

local_dsn = "db.freesql.com" + ":" + "1521" + "/" + "23ai_34ui2"

cfg = dotenv_values(".env")

LIB_DIR = cfg["LIB_DIR"]
DB_USER = cfg["DB_USER"]
DB_PASS = cfg["DB_PASS"]

oracledb.init_oracle_client(lib_dir=LIB_DIR)

conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=local_dsn)

with open("create_db.sql", "r") as f:
    sql_script = f.read()


with conn.cursor() as cursor:
    for tab in sql_script.split(";"):
        t = tab.strip()
        if t:
            cursor.execute(t)

conn.close()
