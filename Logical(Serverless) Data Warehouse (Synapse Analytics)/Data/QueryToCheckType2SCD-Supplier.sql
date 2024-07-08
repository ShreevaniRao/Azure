SELECT TOP (100) [SupplierKey]
,[SupplierID]
,[SupplierName]
,[SupplierCategoryName]
,[ValidFromDate]
,[ValidToDate]
,[ActiveMember]
 FROM [STG].[vwDimSupplierSCD]
 WHERE SupplierID IN (1,5,14)
ORDER BY SupplierID,SupplierKey
