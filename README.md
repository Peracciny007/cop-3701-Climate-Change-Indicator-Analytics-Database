# Climate-Change-Indicator-Analytics-Database

The goal of this project is to design an environmental database tracking long term climate indicators. This dataset will include decades of data and analysis of long term trends.
The data is sourced from Kaggle and it is from a public record of mean surface tempatures every year from 1961 to 2023. 
This dataset contains data from around 232 countries and it can be found here
https://climatedata.imf.org/datasets/4063314923d74187be9596f10d034914_0/explore
This project will use professional documentation to analyze this dataset and design relational schema. This project will apply sound database design principles, including conceptual modeling and SQL implementation to provide insight on important climate trends.
A key design challenge of this application is handling time-series data across multiple decades while maintaining normalization. Instead of storing yearly values as separate columns, the system models years as an entity and uses an associative entity to resolve many-to-many relationships between countries and indicators. Additionally, a weak entity is implemented to track measurement revisions while preserving referential integrity.

# Usage
## How to use:
- Run preprocess.py
- Replace the LIB_DIR, DB_USER, and DB_PASS environment variables with your unique values in the .env file
- Execute create_db.sql or create_db.py file (if not already executed)
- Run dataload2.py (for ease of use)
- Run app.py for the main cli application, commands below may be referred to

## Commands
- ### list
Lists all ISO3's for the countries to be used in the commands
- ### help
Displays the help command
- ### 1
Lists the temperature anomaly given a country and year
- ### 2
Lists all recorded years for a given country
- ### 3
Compares two countries anomalies given a year
- ### 4
Lists the top 5 hottest countries in a year
- ### 5
Displays the highest temperature of a country throughout all recorded years
- ### exit
Exits the program
