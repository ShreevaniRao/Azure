--Initial Sales Fact Table load using views
CREATE EXTERNAL TABLE STG.FactSales
WITH 
(
  LOCATION = 'transformed/facts/factsales/initial',
  DATA_SOURCE = ExternalDataSourceDataLake,
  FILE_FORMAT = SynapseParquetFormat
) 
AS
SELECT  
  --Keys 
    DC.CustomerKey,
    CAST(FORMAT(SO.OrderDate,'yyyyMMdd') AS INT) as OrderDateKey,
    DSI.StockItemKey,
    DS.SupplierKey,
    --Dimensions
    CAST(SO.OrderID AS INT) AS OrderID,
    CAST(SOL.OrderLineID AS INT) AS OrderLineID,  
    --Measures
    CAST(SOL.Quantity AS INT) AS SalesOrderQuantity, 
    CAST(SOL.UnitPrice AS DECIMAL(18,2)) AS SalesOrderUnitPrice
FROM LDW.vwSalesOrdersLines SOL
INNER JOIN LDW.vwSalesOrders SO ON SOL.OrderID = SO.OrderID
LEFT JOIN STG.vwDimCustomer DC ON DC.CustomerID = SO.CustomerID
LEFT JOIN STG.vwDimStockItem DSI ON DSI.StockItemID = SOL.StockItemID
LEFT JOIN LDW.vwStockItems SI ON SI.StockItemID = DSI.StockItemID
LEFT JOIN STG.vwDimSupplier DS ON DS.SupplierID = SI.SupplierID;
