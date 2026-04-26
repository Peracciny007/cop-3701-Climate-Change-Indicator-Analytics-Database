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

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_csv(file_path, csv_cols, db_cols, table, date_cols=None):
    print(f"Loading {table}...")

    df = pd.read_csv(file_path)
    df = df.where(pd.notnull(df), None)

    if date_cols:
        for c in date_cols:
            if c in df.columns:
                df[c] = pd.to_datetime(df[c]).dt.date

    rows = list(df[csv_cols].itertuples(index=False, name=None))

    placeholders = ",".join([f":{i+1}" for i in range(len(db_cols))])

    sql = f"""
        INSERT INTO {table} ({','.join(db_cols)})
        VALUES ({placeholders})
    """

    try:
        with oracledb.connect(user=DB_USER, password=DB_PASS, dsn=local_dsn) as conn:
            cur = conn.cursor()
            cur.executemany(sql, rows)
            conn.commit()

        print(f"{table}: {len(rows)} rows loaded")

    except Exception as e:
        print(f"{table} ERROR: {e}")

    print("Done.\n")


with oracledb.connect(user=DB_USER, password=DB_PASS, dsn=local_dsn) as conn:
    cur = conn.cursor()
    cur.execute("DELETE FROM DataRevision")
    cur.execute("DELETE FROM ClimateMeasurement")
    cur.execute("DELETE FROM CountryProfile")
    cur.execute("DELETE FROM Indicator")
    cur.execute("DELETE FROM Country")
    conn.commit()

print("Old data cleared.\n")


load_csv(
    os.path.join(DATA_DIR, "Country.csv"),
    ["ISO3", "Country", "ISO2"],
    ["ISO3", "COUNTRYNAME", "ISO2"],
    "COUNTRY"
)

load_csv(
    os.path.join(DATA_DIR, "Indicator.csv"),
    ["CTSCode", "IndicatorName", "Unit", "Source", "CTSFullDescriptor"],
    ["CTSCode", "IndicatorName", "Unit", "Source", "CTSFullDescriptor"],
    "INDICATOR"
)

load_csv(
    os.path.join(DATA_DIR, "ClimateMeasurement.csv"),
    ["ISO3", "CTSCode", "Year", "Measurements"],
    ["ISO3", "CTSCode", "Year", "Measurements"],
    "CLIMATEMEASUREMENT"
)

load_csv(
    os.path.join(DATA_DIR, "CountryProfile.csv"),
    ["ISO3", "Region", "IncomeLevel", "ClimateZone"],
    ["ISO3", "Region", "IncomeLevel", "ClimateZone"],
    "COUNTRYPROFILE"
)

load_csv(
    os.path.join(DATA_DIR, "DataRevision.csv"),
    ["RevisionNumber", "ISO3", "CTSCode", "Year", "RevisionDate", "Notes"],
    ["RevisionNumber", "ISO3", "CTSCode", "Year", "RevisionDate", "Notes"],
    "DATAREVISION",
    date_cols=["RevisionDate"]
)

print("All data loaded successfully.")
