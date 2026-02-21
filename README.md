# Climate-Change-Indicator-Analytics-Database

The goal of this project is to design an environmental database tracking long term climate indicators. This dataset will include decades of data and analysis of long term trends.
The data is sourced from Kaggle and it is from a public record of mean surface tempatures every year from 1961 to 2023. 
This dataset contains data from around 232 countries and it can be found here
https://climatedata.imf.org/datasets/4063314923d74187be9596f10d034914_0/explore
This project will use professional documentation to analyze this dataset and design relational schema. This project will apply sound database design principles, including conceptual modeling and SQL implementation to provide insight on important climate trends.
A key design challenge of this application is handling time-series data across multiple decades while maintaining normalization. Instead of storing yearly values as separate columns, the system models years as an entity and uses an associative entity to resolve many-to-many relationships between countries and indicators. Additionally, a weak entity is implemented to track measurement revisions while preserving referential integrity.
