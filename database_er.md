Here is the climate ER diagram 
<img width="906" height="646" alt="image" src="https://github.com/user-attachments/assets/15d3810e-4036-4a30-a70d-99acd7820db3" />
# Final Normalized Relational Schema (BCNF)

## Country
ISO3 (PK)
CountryName
ISO2

## CountryProfile
ISO3 (PK, FK → Country.ISO3)
Region
IncomeLevel
ClimateZone

## Indicator
CTSCode (PK)
IndicatorName
Unit
Source
CTSFullDescriptor

## Year
YearID (PK)
YearValue

## ClimateMeasurement
ISO3 (PK, FK → Country.ISO3)
CTSCode (PK, FK → Indicator.CTSCode)
YearID (PK, FK → Year.YearID)
Measurements

Primary Key: (ISO3, CTSCode, YearID)

## DataRevision
RevisionNumber (PK)
ISO3 (FK → ClimateMeasurement.ISO3)
CTSCode (FK → ClimateMeasurement.CTSCode)
YearID (FK → ClimateMeasurement.YearID)
RevisionDate
Notes

All relations were checked for BCNF.
For every nontrivial functional dependency X → Y, X is a candidate key.
No decomposition was required.
