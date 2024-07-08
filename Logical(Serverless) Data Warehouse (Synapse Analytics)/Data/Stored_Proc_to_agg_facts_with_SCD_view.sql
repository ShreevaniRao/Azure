CREATE PROCEDURE STG.FactSalesLoadCSD @ProcessDate DATE
WITH ENCRYPTION
AS

BEGIN

DECLARE @location varchar(100)

IF OBJECT_ID('STG.FactSales') IS NOT NULL 
  DROP EXTERNAL TABLE STG.FactSales

SET @location = CONCAT('transformed/facts/factsales/incremental/',FORMAT (@ProcessDate, 'yyyy/MM/dd') )

DECLARE @CreateExternalTableString NVARCHAR(2000)

SET @CreateExternalTableString = 
'CREATE EXTERNAL TABLE STG.FactSales
WITH 
(
  LOCATION = ''' + @location + ''',                                      
  DATA_SOURCE = ExternalDataSourceDataLake,
  FILE_FORMAT = SynapseParquetFormat
)
AS
SELECT  
--Surrogate Keys 
DC.CustomerKey,
CAST(FORMAT(SO.OrderDate,''yyyyMMdd'') AS INT) as OrderDateKey,
DSI.StockItemKey,
DS.SupplierKey,
--Dimensions
CAST(SO.OrderID AS INT) AS OrderID,
CAST(SOL.OrderLineID AS INT) AS OrderLineID,  
--Measures
CAST(SOL.Quantity AS INT) AS SalesOrderQuantity, 
CAST(SOL.UnitPrice AS DECIMAL(18,2)) AS SalesOrderUnitPrice
FROM LDW.vwSalesOrdersLines SOL
INNER JOIN STG.vwSalesOrders SO ON SOL.OrderID = SO.OrderID
LEFT JOIN STG.vwDimCustomer DC ON DC.CustomerID = SO.CustomerID
LEFT JOIN STG.vwDimStockItem DSI ON DSI.StockItemID = SOL.StockItemID
LEFT JOIN STG.vwStockItems SI ON SI.StockItemID = DSI.StockItemID
LEFT JOIN STG.vwDimSupplierSCD  DS ON DS.SupplierID = SI.SupplierID AND SO.OrderDate BETWEEN DS.ValidFromDate AND DS.ValidToDate
WHERE SOL.FilePathDate = ''' + CAST(@ProcessDate AS CHAR(10)) + '''  AND SO.FilePathDate = ''' + CAST(@ProcessDate AS CHAR(10)) + ''''

EXEC sp_executesql @CreateExternalTableString

END