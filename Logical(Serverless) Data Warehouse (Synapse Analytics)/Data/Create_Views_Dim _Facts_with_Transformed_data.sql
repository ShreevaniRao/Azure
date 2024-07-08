--DROP VIEW LDW.vwDimCustomers;
--DROP VIEW LDW.vwDimStockItems;

--Customer
DROP VIEW IF EXISTS STG.vwDimCustomer
GO
CREATE VIEW STG.vwDimCustomer
AS
SELECT * FROM 
OPENROWSET 
(
    BULK 'transformed/dimensions/dimcustomer/*/',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'Parquet'
) AS fctCustomer
GO

--StockItem
DROP VIEW IF EXISTS STG.vwDimStockItem
GO
CREATE VIEW STG.vwDimStockItem
AS
SELECT * FROM 
OPENROWSET 
(
    BULK 'transformed/dimensions/dimstockitem/*/',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'Parquet'
) AS fctStockItem
GO

--Supplier
DROP VIEW IF EXISTS STG.vwDimSupplier
GO
CREATE VIEW STG.vwDimSupplier
AS
SELECT * FROM 
OPENROWSET 
(
    BULK 'transformed/dimensions/dimsupplier/*/',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'Parquet'
) AS fctSupplier
GO

--Date
DROP VIEW IF EXISTS STG.vwDimDate
GO
CREATE VIEW STG.vwDimDate
AS
SELECT * FROM 
OPENROWSET 
(
    BULK 'transformed/dimensions/dimdate',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'Parquet'
) AS fctDate
GO

DROP VIEW IF EXISTS STG.vwFactSales
GO
CREATE VIEW STG.vwFactSales
AS
SELECT *,
CAST(fctSales.filepath(3) AS DATE) AS SalesOrderPathDate
 FROM 
OPENROWSET 
(
    BULK 'transformed/facts/factsales/*/*/*/',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'Parquet'
) AS fctSales
GO
