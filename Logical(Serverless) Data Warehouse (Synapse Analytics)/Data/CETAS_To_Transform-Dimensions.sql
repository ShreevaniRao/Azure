CREATE SCHEMA STG AUTHORIZATION dbo;

--Customer
CREATE EXTERNAL TABLE STG.DimCustomer
WITH 
(
  LOCATION = 'transformed/dimensions/dimcustomer/01',
  DATA_SOURCE = ExternalDataSourceDataLake,
  FILE_FORMAT = SynapseParquetFormat
) 
AS
SELECT CAST(ROW_NUMBER() OVER(ORDER BY C.CustomerID) AS INT) AS CustomerKey,
        CAST(C.CustomerID AS INT) AS CustomerID,
        C.CustomerName,
        CC.CustomerCategoryName,
        BG.BuyingGroupName,
        DM.DeliveryMethodName,
        DC.CityName AS DeliveryCityName,
        DSP.StateProvinceName AS DeliveryStateProvinceName,
        DSP.SalesTerritory AS DeliverySalesTerritory,
        DCO.Country AS DeliveryCountry,
        DCO.Continent AS DeliveryContinent,
        DCO.Region AS DeliveryRegion,
        DCO.Subregion AS DeliverySubregion,
        CAST('2021-01-01' AS DATE) AS ValidFromDate
FROM LDW.vwCustomers C
LEFT JOIN LDW.vwCustomerCategories CC On CC.CustomerCategoryID = C.CustomerCategoryID
LEFT JOIN LDW.vwCities DC ON DC.CityID = C.DeliveryCityID
LEFT JOIN LDW.vwStateProvinces DSP ON DSP.StateProvinceID = DC.StateProvinceID
LEFT JOIN LDW.vwCountries DCO ON DCO.CountryID = DSP.CountryID
LEFT JOIN LDW.vwBuyingGroups BG ON BG.BuyingGroupID = C.BuyingGroupID
LEFT JOIN LDW.vwDeliveryMethods DM ON DM.DeliveryMethodID = C.DeliveryMethodID
ORDER BY C.CustomerID

--StockItem
CREATE EXTERNAL TABLE STG.DimStockItem
WITH 
(
  LOCATION = 'transformed/dimensions/dimstockitem/01',
  DATA_SOURCE = ExternalDataSourceDataLake,
  FILE_FORMAT = SynapseParquetFormat
) 
AS
SELECT CAST(ROW_NUMBER() OVER(ORDER BY SI.StockItemID) AS SMALLINT) AS StockItemKey,
CAST(SI.StockItemID AS SMALLINT) AS StockItemID,
SI.StockItemName,
SI.LeadTimeDays,
C.ColorName,
OP.PackageTypeName AS OuterPackageTypeName,
CAST('2021-01-01' AS DATE) AS ValidFromDate
FROM LDW.vwStockItems SI
LEFT JOIN LDW.vwColors C ON C.ColorID = SI.ColorID
LEFT JOIN LDW.vwPackageTypes OP ON OP.PackageTypeID = SI.OuterPackageID
ORDER BY SI.StockItemID

--Supplier
CREATE EXTERNAL TABLE STG.DimSupplier
WITH 
(
  LOCATION = 'transformed/dimensions/dimsupplier/01',
  DATA_SOURCE = ExternalDataSourceDataLake,
  FILE_FORMAT = SynapseParquetFormat
) 
AS
SELECT CAST(ROW_NUMBER() OVER(ORDER BY S.SupplierID) AS TINYINT) AS SupplierKey,
CAST(S.SupplierID AS TINYINT) AS SupplierID,
S.SupplierName,
SC.SupplierCategoryName,
CAST('2021-01-01' AS DATE) AS ValidFromDate
FROM LDW.vwSuppliers S
LEFT JOIN LDW.vwSupplierCategories SC ON SC.SupplierCategoryID = S.SupplierCategoryID
ORDER BY S.SupplierID;

--Date
CREATE EXTERNAL TABLE STG.DimDate
WITH 
(
  LOCATION = 'transformed/dimensions/dimdate',
  DATA_SOURCE = ExternalDataSourceDataLake,
  FILE_FORMAT = SynapseParquetFormat
) 
AS
SELECT CAST(DateKey AS INT) AS DateKey,
        CAST(Date AS DATE) AS Date,
        CAST(Day AS TINYINT) AS Day,
        CAST(WeekDay AS TINYINT) AS WeekDay,
        WeekDayName,
        CAST(Month AS TINYINT) AS Month,
        MonthName,
        CAST(Quarter AS TINYINT) AS Quarter,
        CAST(Year AS SMALLINT) AS Year
FROM
OPENROWSET 
(
    BULK 'SourceDataDim/DateDim/*.csv',
    DATA_SOURCE = 'ExternalDataSourceDataLake',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE,
    FIELDTERMINATOR ='|'
) AS fctDate