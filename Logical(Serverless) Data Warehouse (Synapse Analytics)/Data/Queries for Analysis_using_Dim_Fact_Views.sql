--Sales by Date Grouping
SELECT DD.[Year] AS SalesYear,
    DD.[Month] AS SalesMonth,
SUM(FS.SalesOrderQuantity) as SalesOrderQuantity,
COUNT(DISTINCT FS.OrderID) AS TotalSalesOrdersCount
FROM STG.vwFactSales FS
INNER JOIN STG.vwDimDate DD ON DD.DateKey = FS.OrderDateKey
GROUP BY DD.[Year],
         DD.[Month]
ORDER BY DD.[Year],
         DD.[Month];

--Sales by Customer Grouping
SELECT DC.DeliverySalesTerritory,
SUM(FS.SalesOrderQuantity) As SalesOrderQuantity,
COUNT(DISTINCT OrderID) AS TotalSalesOrdersCount
FROM STG.vwFactSales FS
INNER JOIN STG.vwDimCustomer DC ON DC.CustomerKey = FS.CustomerKey
GROUP BY DC.DeliverySalesTerritory
ORDER BY SUM(FS.SalesOrderQuantity) DESC;

--Group Sales by Supplier
SELECT DS.SupplierName,
SUM(FS.SalesOrderQuantity) AS SalesOrderQuantity
FROM STG.vwFactSales FS
INNER JOIN STG.vwDimSupplier DS ON DS.SupplierKey = FS.SupplierKey
GROUP BY DS.SupplierName
ORDER BY SUM(FS.SalesOrderQuantity) DESC;