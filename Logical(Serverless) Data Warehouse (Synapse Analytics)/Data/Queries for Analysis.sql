SELECT COUNT(SO.OrderID) AS TotalOrderCount
FROM LDW.vwSalesOrders SO
WHERE SO.OrderDate = '2021-01-16'


SELECT YEAR(SO.OrderDate) AS OrderDateYear,
        COUNT(SO.OrderDate) AS TotalOrderCount
FROM LDW.vwSalesOrders SO
GROUP BY YEAR(SO.OrderDate);

SELECT ISNULL(C.ColorName,'No Colour') AS ColourName,
    SUM(SOL.Quantity) AS TotalOrderLineQuantity,
    SUM(SOL.UnitPrice) AS TotalOrderLineUnitPrice
FROM LDW.vwSalesOrdersLines SOL
INNER JOIN LDW.vwStockItems SI ON SI.StockItemID = SOL.StockItemID
LEFT JOIN LDW.vwColors C ON C.ColorID = SI.ColorID
GROUP BY ISNULL(C.ColorName,'No Colour');

SELECT 
    YEAR(SO.OrderDate) AS OrderDateYear,
    SC.SupplierCategoryName,
    SUM(SOL.Quantity) AS TotalOrderLineQuantity,
    SUM(SOL.UnitPrice) AS TotalOrderLineUnitPrice
FROM LDW.vwSalesOrdersLines SOL
INNER JOIN LDW.vwSalesOrders SO ON SO.OrderID = SOL.OrderID
INNER JOIN LDW.vwStockItems SI ON SI.StockItemID = SOL.StockItemID
INNER JOIN LDW.vwSuppliers S ON SI.SupplierID = S.SupplierID
INNER JOIN LDW.vwSupplierCategories SC ON SC.SupplierCategoryID = S.SupplierCategoryID
GROUP BY YEAR(SO.OrderDate),
        SC.SupplierCategoryName;



SELECT YEAR(SO.OrderDate) AS OrderDateYear,
        COUNT(SO.OrderDate) AS TotalOrderCount
FROM LDW.vwSalesOrders SO
WHERE SO.FilePathDate = '2021-01-16'
GROUP BY YEAR(SO.OrderDate)

CREATE VIEW LDW.vwDimStockItems
AS
SELECT  SI.StockItemID,
        SI.StockItemName,
        SI.LeadTimeDays,
        SI.TaxRate,
        SI.UnitPrice,
        SI.SearchDetails,
        PTUnit.PackageTypeName AS PackageTypeNameUnit,
        PTOut.PackageTypeName AS PackageTypeNameOuter,
        C.ColorName,
        S.SupplierName,
        S.PaymentDays,
        SC.SupplierCategoryName
FROM LDW.vwStockItems SI
LEFT JOIN LDW.vwPackageTypes PTUnit ON PTUnit.PackageTypeID = SI.UnitPackageID
LEFT JOIN LDW.vwPackageTypes PTOut ON PTOut.PackageTypeID = SI.OuterPackageID
LEFT JOIN LDW.vwColors C ON C.ColorID = SI.ColorID
LEFT JOIN LDW.vwSuppliers S ON S.SupplierID = SI.SupplierID
LEFT JOIN LDW.vwSupplierCategories SC ON SC.SupplierCategoryID = S.SupplierCategoryID


CREATE VIEW LDW.vwDimCustomers
AS
SELECT  C.CustomerID,
        C.CustomerName,
        C.AccountOpenedDate,
        C.CreditLimit,
        C.PaymentDays,
        CT.CityName AS CityNameDelivery,
        SP.StateProvinceCode AS StateProvinceCodeDelivery,
        SP.StateProvinceName AS StateProvinceNameDelivery,
        SP.SalesTerritory AS SalesTerritoryDelivery,
        CR.Country AS CountryDelivery,
        CR.Continent AS ContinentDelivery,
        CR.Region AS RegionDelivery,
        CR.Subregion AS SubregionDelivery,
        P.FullName AS PrimaryContactPersonName,
        CC.CustomerCategoryName,
        BG.BuyingGroupName,
        DM.DeliveryMethodName
FROM LDW.vwCustomers C
LEFT JOIN LDW.vwCities CT ON CT.CityID = C.DeliveryCityID
LEFT JOIN LDW.vwStateProvinces SP ON SP.StateProvinceID = CT.StateProvinceID
LEFT JOIN LDW.vwCountries CR ON CR.CountryID = SP.CountryID
LEFT JOIN LDW.vwPeople P ON P.PersonID = C.PrimaryContactPersonID
LEFT JOIN LDW.vwCustomerCategories CC ON CC.CustomerCategoryID = C.CustomerCategoryID
LEFT JOIN LDW.vwBuyingGroups BG ON BG.BuyingGroupID = C.BuyingGroupID
LEFT JOIN LDW.vwDeliveryMethods DM ON DM.DeliveryMethodID = C.DeliveryMethodID


SELECT DC.CustomerCategoryName,
        DS.PackageTypeNameUnit,
        SUM(SOL.Quantity) AS TotalOrderLineQuantity,
        SUM(SOL.UnitPrice) AS TotalOrderLineUnitPrice
FROM LDW.vwSalesOrdersLines SOL
INNER JOIN LDW.vwSalesOrders SO ON SO.OrderID = SOL.OrderID
INNER JOIN LDW.vwDimCustomers DC ON DC.CustomerID = SO.CustomerID
INNER JOIN LDW.vwDimStockItems DS ON DS.StockItemID = SOL.StockItemID
GROUP BY DC.CustomerCategoryName,
        DS.PackageTypeNameUnit

