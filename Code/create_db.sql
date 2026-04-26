CREATE TABLE Country (
    ISO3 CHAR(3) PRIMARY KEY,
    COUNTRYNAME VARCHAR2(150),
    ISO2 CHAR(2)
);

CREATE TABLE CountryProfile (
    ISO3 CHAR(3) PRIMARY KEY,
    Region VARCHAR2(100),
    IncomeLevel VARCHAR2(50),
    ClimateZone VARCHAR2(50),
    FOREIGN KEY (ISO3) REFERENCES Country(ISO3)
);

CREATE TABLE Indicator (
    CTSCode VARCHAR2(20) PRIMARY KEY,
    IndicatorName VARCHAR2(200),
    Unit VARCHAR2(50),
    Source VARCHAR2(300),
    CTSFullDescriptor VARCHAR2(300)
);

CREATE TABLE ClimateMeasurement (
    ISO3 CHAR(3),
    CTSCode VARCHAR2(20),
    Year NUMBER(4),
    Measurements NUMBER,
    PRIMARY KEY (ISO3, CTSCode, Year),
    FOREIGN KEY (ISO3) REFERENCES Country(ISO3),
    FOREIGN KEY (CTSCode) REFERENCES Indicator(CTSCode)
);

CREATE TABLE DataRevision (
    RevisionNumber NUMBER PRIMARY KEY,
    ISO3 CHAR(3),
    CTSCode VARCHAR2(20),
    Year NUMBER(4),
    RevisionDate DATE,
    Notes VARCHAR2(300),
    FOREIGN KEY (ISO3, CTSCode, Year)
        REFERENCES ClimateMeasurement(ISO3, CTSCode, Year)
);

