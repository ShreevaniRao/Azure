DROP VIEW IF EXISTS STG.vwIncrementalSuppliers
GO

CREATE VIEW STG.vwIncrementalSuppliers
AS
SELECT fct.*,
fct.filepath(1) AS FilePathDate
FROM 
OPENROWSET 
(
    BULK 'ChangedData/*/Purchasing_Suppliers/*.csv',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE,
    FIELDTERMINATOR ='|'
) AS fct