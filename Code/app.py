import oracledb
from oracledb import Cursor
from dotenv import load_dotenv, dotenv_values

load_dotenv()

local_dsn = "db.freesql.com" + ":" + "1521" + "/" + "23ai_34ui2"

cfg = dotenv_values(".env")

LIB_DIR = cfg["LIB_DIR"]
DB_USER = cfg["DB_USER"]
DB_PASS = cfg["DB_PASS"]

oracledb.init_oracle_client(lib_dir=LIB_DIR)

def main():
    conn = oracledb.connect(
        user=DB_USER,
        password=DB_PASS,
        dsn=local_dsn)
    cur = conn.cursor()

    while True:
        print("(1) Temperature anomaly for a country in a year")
        print("(2) All recorded years for a country")
        print("(3) Compare two countries in a year")
        print("(4) Top 5 hottest countries in a year")
        print("(5) Highest temperature of a country")
        print("(list) Lists all ISO3s to be used as country option")
        print("(help)")
        print("(exit)")

        choice = input()

        print("===============")
        match choice:
            case "1":
                avg_temps(cur)
            case "2":
                all_rec_years(cur)
            case "3":
                compare_countries(cur)
            case "4":
                top_countries(cur)
            case "5":
                country_highest_temp(cur)
            case "list":
                list_countries(cur)
            case "help":
                print("Most commands will ask for a country, after choosing the command with a given number (1-5) you can provide the country's ISO3")
                print("ISO3's can be listed with the list command")
            case "exit":
                print("Breaking")
                break
            case _:
                print("Invalid command")
        print("===============")

    conn.close()


def avg_temps(cur: Cursor):
    loc = input("Country location:").upper()
    year = input("Year:")

    cur.execute("""
    SELECT cm.Measurements
    FROM ClimateMeasurement cm
    JOIN Country c ON cm.ISO3 = c.ISO3
    JOIN Indicator i ON cm.CTSCode = i.CTSCode
    WHERE cm.ISO3 = :c_name
    AND cm.Year = :year
    """, {
        "c_name": loc,
        "year": year
    })

    anom = cur.fetchone()
    print(f"Temperature anomaly for {year} is {anom[0]}")

def all_rec_years(cur: Cursor):
    loc = input("Country location:").upper()

    cur.execute("""
        SELECT c.CountryName, cm.Year, cm.Measurements
        FROM ClimateMeasurement cm
        JOIN Country c ON cm.ISO3 = c.ISO3
        WHERE cm.ISO3 = :iso3
        ORDER BY cm.Year
    """, {
        "iso3": loc
    })

    for r in cur.fetchall():
        print(f"{r[0]}; Year: {r[1]}; Anomaly: {r[2]}")


def compare_countries(cur: Cursor):
    c1 = input("Country 1 location:").upper()
    c2 = input("Country 2 location:").upper()
    year = input("Year:")

    cur.execute("""
        SELECT c.CountryName, cm.Measurements
        FROM ClimateMeasurement cm
        JOIN Country c ON cm.ISO3 = c.ISO3
        WHERE cm.ISO3 IN (:c1, :c2)
        AND cm.Year = :year
    """, {
        "c1": c1,
        "c2": c2,
        "year": year
    })

    for r in cur.fetchall():
        print(f"{r[0]}: {r[1]}")


def top_countries(cur: Cursor):
    year = input("Year:")

    cur.execute("""
        SELECT c.CountryName, Measurements
        FROM ClimateMeasurement cm
        JOIN Country c on cm.ISO3 = c.ISO3
        WHERE cm.Year = :year
        ORDER BY Measurements DESC
    """, {
        "year": year
    })

    for i, r in enumerate(cur.fetchmany(5)):
        print(f"#{i + 1} {r[0]}: {r[1]}")


def country_highest_temp(cur: Cursor):
    loc = input("Country location:").upper()

    cur.execute("""
        SELECT cm.Year, cm.Measurements
        FROM ClimateMeasurement cm
        JOIN Country c ON cm.ISO3 = c.ISO3
        WHERE cm.ISO3 = :iso3
        ORDER BY cm.Measurements DESC
        FETCH FIRST 1 ROW ONLY
    """, {
        "iso3": loc
    })

    r = cur.fetchone()

    print(f"Year: {r[0]}; Anomaly: {r[1]}")

def list_countries(cur: Cursor):
    cur.execute("SELECT ISO3 FROM Country")

    for r in cur.fetchall():
        print(r[0])

if __name__ == "__main__":
    main()
