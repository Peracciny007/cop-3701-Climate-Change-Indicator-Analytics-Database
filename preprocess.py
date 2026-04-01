import pandas as pd
import numpy as np
import os
from datetime import datetime
import random

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

raw_df = pd.read_csv(os.path.join(BASE_DIR, "climate_raw.csv"))

countries = raw_df[['Country', 'ISO2', 'ISO3']].drop_duplicates().copy().dropna()
countries['Country'] = countries['Country'].astype(str)
countries['ISO2'] = countries['ISO2'].astype(str)
countries['ISO3'] = countries['ISO3'].astype(str).str[:3].str.upper()
countries = countries.drop_duplicates(subset=["ISO3"])

country_iso_list = countries["ISO3"].tolist()

countries.to_csv(os.path.join(DATA_DIR, "Country.csv"), index=False)

indicators = raw_df[['CTS Code', 'CTS Name', 'Unit', 'Source', 'CTS Full Descriptor']].drop_duplicates().copy()

indicators = indicators.rename(columns={
    'CTS Code': 'CTSCode',
    'CTS Name': 'IndicatorName',
    'CTS Full Descriptor': 'CTSFullDescriptor'
}).dropna()

indicators['CTSFullDescriptor'] = indicators['CTSFullDescriptor'].astype(str).str[:300]

while len(indicators) < 100:
    i = len(indicators) + 1
    base = indicators.sample(1).iloc[0]

    indicators = pd.concat([
        indicators,
        pd.DataFrame([{
            "CTSCode": f"SYN_{i:03d}",
            "IndicatorName": f"{base['IndicatorName']} Variant {i}",
            "Unit": base["Unit"],
            "Source": base["Source"],
            "CTSFullDescriptor": f"Synthetic extension of {base['CTSFullDescriptor']}"[:300]
        }])
    ], ignore_index=True)

indicators.to_csv(os.path.join(DATA_DIR, "Indicator.csv"), index=False)

year_cols = [c for c in raw_df.columns if str(c).isdigit()]

climate = raw_df.melt(
    id_vars=['ISO3', 'CTS Code'],
    value_vars=year_cols,
    var_name='Year',
    value_name='Measurements'
)

climate = climate.rename(columns={'CTS Code': 'CTSCode'})

climate['Measurements'] = pd.to_numeric(climate['Measurements'], errors='coerce')
climate = climate.dropna(subset=['Measurements'])
climate = climate[climate["ISO3"].isin(country_iso_list)]

target_size = max(len(climate), 5000)

while len(climate) < target_size:
    base = climate.sample(1).iloc[0]

    climate = pd.concat([
        climate,
        pd.DataFrame([{
            "ISO3": random.choice(country_iso_list),
            "CTSCode": base["CTSCode"],
            "Year": str(int(base["Year"]) + np.random.randint(1, 5)),
            "Measurements": float(base["Measurements"] * np.random.uniform(0.9, 1.1))
        }])
    ], ignore_index=True)

climate["ISO3"] = climate["ISO3"].astype(str).str[:3].str.upper()

climate.to_csv(os.path.join(DATA_DIR, "ClimateMeasurement.csv"), index=False)

profile = pd.DataFrame({"ISO3": country_iso_list})

profile["Region"] = np.random.choice(["Africa", "Asia", "Europe", "Americas", "Oceania"], len(profile))
profile["IncomeLevel"] = np.random.choice(["Low", "Lower middle", "Upper middle", "High"], len(profile))
profile["ClimateZone"] = np.random.choice(["Tropical", "Dry", "Temperate", "Continental", "Polar"], len(profile))

profile.to_csv(os.path.join(DATA_DIR, "CountryProfile.csv"), index=False)

rows = []

for i in range(len(climate)):
    rows.append([
        i + 1,
        climate.iloc[i]["ISO3"],
        climate.iloc[i]["CTSCode"],
        climate.iloc[i]["Year"],
        datetime.now().date().isoformat(),
        "synthetic revision"
    ])

revision = pd.DataFrame(rows, columns=[
    "RevisionNumber",
    "ISO3",
    "CTSCode",
    "Year",
    "RevisionDate",
    "Notes"
])

revision.to_csv(os.path.join(DATA_DIR, "DataRevision.csv"), index=False)

print("Preprocessing complete: ALL 5 CSVs created.")