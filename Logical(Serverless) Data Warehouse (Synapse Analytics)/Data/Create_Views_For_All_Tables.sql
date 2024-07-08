DROP VIEW IF EXISTS LDW.vwSalesOrders
GO
CREATE VIEW LDW.vwSalesOrders
AS
SELECT *,
CAST(SalesOrderfct.filepath(1) AS DATE) AS FilePathDate
FROM 
OPENROWSET 
(
    BULK 'sourcedatapartitionsalesorder/OrderDatePartition=*/*.csv',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE,
    FIELDTERMINATOR ='|'
) AS SalesOrderfct
GO


DROP VIEW IF EXISTS LDW.vwSalesOrdersLines
GO
    CREATE VIEW LDW.vwSalesOrdersLines
    AS 
    SELECT *,
    CAST(SalesOrderLinesfct.filepath(1) AS DATE) AS FilePathDate
    FROM 
    OPENROWSET 
    (
        BULK 'sourcedatapartitionsalesorderline/OrderDate=*/*.csv',
        DATA_SOURCE = 'ExternalDataSourceDataLake',
        FORMAT = 'CSV',
        PARSER_VERSION = '2.0',
        HEADER_ROW = TRUE,
        FIELDTERMINATOR ='|'
    ) AS SalesOrderLinesfct
GO


DROP VIEW IF EXISTS LDW.vwCustomers
GO
CREATE VIEW LDW.vwCustomers
AS
SELECT * FROM 
OPENROWSET 
(
    BULK 'Sales_Customers/*.csv',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE,
    FIELDTERMINATOR ='|'
) AS CustomerDim
GO


DROP VIEW IF EXISTS LDW.vwStateProvinces
GO
CREATE VIEW LDW.vwStateProvinces
AS
SELECT * FROM 
OPENROWSET 
(
    BULK 'Application_StateProvinces/*.csv',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE,
    FIELDTERMINATOR ='|'
)
WITH
(
    StateProvinceID TINYINT,
    StateProvinceCode CHAR(2),
    StateProvinceName VARCHAR(30),
    CountryID TINYINT,
    SalesTerritory VARCHAR(14),
    LatestRecordedPopulation INT
) AS StateProvDim
GO

DROP VIEW IF EXISTS LDW.vwCities
GO
CREATE VIEW LDW.vwCities
AS
SELECT CityID,
        CityName,
        StateProvinceID,
        LatestRecordedPopulation
FROM 
OPENROWSET 
(
    BULK 'Application_Cities/*.csv',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE,
    FIELDTERMINATOR ='|'
) AS fct
GO

DROP VIEW IF EXISTS LDW.vwStateProvinces
GO

CREATE VIEW LDW.vwStateProvinces
AS
SELECT * FROM 
OPENROWSET 
(
    BULK 'Application_StateProvinces/*.csv',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE,
    FIELDTERMINATOR ='|'
)
WITH
(
    StateProvinceID TINYINT,
    StateProvinceCode CHAR(2),
    StateProvinceName VARCHAR(30),
    CountryID TINYINT,
    SalesTerritory VARCHAR(14),
    LatestRecordedPopulation INT
) AS fct
GO

DROP VIEW IF EXISTS LDW.vwCountries
GO
CREATE VIEW LDW.vwCountries
AS
SELECT * FROM 
OPENROWSET 
(
    BULK 'Application_Countries/*.csv',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    FIRSTROW = 2,
    FIELDTERMINATOR ='|'
)
WITH
(
    CountryID TINYINT 1,
    Country VARCHAR(50) 2,
    IsoCode3 CHAR(3) 4,
    CountryType VARCHAR(50) 6,
    LatestRecordedPopulation INT 7,
    Continent VARCHAR(50) 8,
    Region VARCHAR(50) 9,
    Subregion VARCHAR(50) 10
) AS fct
GO

DROP VIEW IF EXISTS LDW.vwBuyingGroups
GO

CREATE VIEW LDW.vwBuyingGroups
AS
SELECT * FROM 
OPENROWSET 
(
    BULK 'Sales_BuyingGroups/*.csv',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE,
    FIELDTERMINATOR ='|'
) AS fct
GO

DROP VIEW IF EXISTS LDW.vwDeliveryMethods
GO

CREATE VIEW LDW.vwDeliveryMethods
AS
SELECT * FROM 
OPENROWSET 
(
    BULK 'Application_DeliveryMethods/*.csv',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE,
    FIELDTERMINATOR ='|'
) AS fct
GO

DROP VIEW IF EXISTS LDW.vwCustomerCategories
GO
CREATE VIEW LDW.vwCustomerCategories
AS
SELECT * FROM 
OPENROWSET 
(
    BULK 'Sales_CustomerCategories/*.csv',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE,
    FIELDTERMINATOR ='|'
) AS fct
GO

DROP VIEW IF EXISTS LDW.vwPeople
GO

CREATE VIEW LDW.vwPeople
AS
SELECT * FROM 
OPENROWSET 
(
    BULK 'Application_People/*.csv',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE,
    FIELDTERMINATOR ='|'
) AS fct
GO

DROP VIEW IF EXISTS LDW.vwSuppliers
GO
CREATE VIEW LDW.vwSuppliers
AS
SELECT * FROM 
OPENROWSET 
(
    BULK 'Purchasing_Suppliers/*.csv',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE,
    FIELDTERMINATOR ='|'
) AS fct
GO

DROP VIEW IF EXISTS LDW.vwSupplierCategories
GO
CREATE VIEW LDW.vwSupplierCategories
AS
SELECT * FROM 
OPENROWSET 
(
    BULK 'Purchasing_SupplierCategories/*.csv',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE,
    FIELDTERMINATOR ='|'
) AS fct
GO

DROP VIEW IF EXISTS LDW.vwStockItems
GO
CREATE VIEW LDW.vwStockItems
AS
SELECT * FROM 
OPENROWSET 
(
    BULK 'Warehouse_StockItems/*.csv',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE,
    FIELDTERMINATOR ='|'
) AS fct
GO

DROP VIEW IF EXISTS LDW.vwColors
GO
CREATE VIEW LDW.vwColors
AS
SELECT * FROM 
OPENROWSET 
(
    BULK 'Warehouse_Colors/*.csv',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE,
    FIELDTERMINATOR ='|'
) AS fct
GO

DROP VIEW IF EXISTS LDW.vwPackageTypes
GO
CREATE VIEW LDW.vwPackageTypes
AS
SELECT * FROM 
OPENROWSET 
(
    BULK 'Warehouse_PackageTypes/*.csv',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE,
    FIELDTERMINATOR ='|'
) AS fct
GO