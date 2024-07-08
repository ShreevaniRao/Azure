DROP VIEW IF EXISTS STG.vwDimSupplierSCD
GO

CREATE VIEW STG.vwDimSupplierSCD
AS
SELECT SupplierKey,
        SupplierID,
        SupplierName,
        SupplierCategoryName,
        ValidFromDate,
        ISNULL(DATEADD(DAY,-1,LEAD(ValidFromDate,1) OVER (PARTITION BY SupplierID ORDER BY SupplierKey)),'2099-01-01') AS ValidToDate,
        CASE ROW_NUMBER() OVER(PARTITION BY SupplierID ORDER BY SupplierKey DESC) WHEN 1 THEN 'Y' ELSE 'N' END AS ActiveMember
FROM STG.vwDimSupplier