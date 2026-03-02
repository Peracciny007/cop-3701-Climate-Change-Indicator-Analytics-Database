Here is the climate ER diagram 
<img width="906" height="646" alt="image" src="https://github.com/user-attachments/assets/15d3810e-4036-4a30-a70d-99acd7820db3" />
# Final Normalized Relational Schema (BCNF)
# Final Relational Schema (After Normalization)

Below is the final version of the relational schema after checking for BCNF.

---

## Country
ISO3 (Primary Key)  
CountryName  
ISO2  

---

## CountryProfile
ISO3 (Primary Key, also Foreign Key → Country.ISO3)  
Region  
IncomeLevel  
ClimateZone  

---

## Indicator
CTSCode (Primary Key)  
IndicatorName  
Unit  
Source  
CTSFullDescriptor  

---

## Year
YearID (Primary Key)  
YearValue  

---

## ClimateMeasurement
ISO3 (Foreign Key → Country.ISO3)  
CTSCode (Foreign Key → Indicator.CTSCode)  
YearID (Foreign Key → Year.YearID)  
Measurements  

Primary Key: (ISO3, CTSCode, YearID)

---

## DataRevision
RevisionNumber (Primary Key)  
ISO3  
CTSCode  
YearID  
RevisionDate  
Notes  

Foreign Key: (ISO3, CTSCode, YearID)  
References ClimateMeasurement(ISO3, CTSCode, YearID)

---

## Normalization Summary

Each table was checked for nontrivial functional dependencies.  
In every case, the determinant of each dependency is a primary key.  

Because of this, all relations satisfy Boyce-Codd Normal Form (BCNF).  
No additional decomposition was needed and no redundancy exists in the schema.
