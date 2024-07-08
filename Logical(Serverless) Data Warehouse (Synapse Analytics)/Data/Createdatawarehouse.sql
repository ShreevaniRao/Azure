--Create Database and Data Sources

CREATE DATABASE sqllogicaldw;

CREATE EXTERNAL DATA SOURCE ExternalDataSourceDataLake
	WITH (
		LOCATION   = 'https://staccserverlesswarehouse.dfs.core.windows.net/datalakehouse' 
	    );
		
CREATE EXTERNAL FILE FORMAT SynapseParquetFormat
WITH ( 
        FORMAT_TYPE = PARQUET
     );

CREATE SCHEMA LDW authorization dbo;

CREATE MASTER KEY ENCRYPTION BY PASSWORD = '9S%%U9rXfmLes5swcc9Y';

CREATE DATABASE SCOPED CREDENTIAL SynapseUserIdentity 
WITH IDENTITY = 'User Identity';

ALTER DATABASE sqllogicaldw COLLATE Latin1_General_100_BIN2_UTF8;