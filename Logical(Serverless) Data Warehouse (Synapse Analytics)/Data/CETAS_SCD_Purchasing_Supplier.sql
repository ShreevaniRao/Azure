DECLARE @MaxKey TINYINT
SELECT @MaxKey = MAX(SupplierKey) FROM STG.vwDimSupplier

IF OBJECT_ID('STG.DimSupplier') IS NOT NULL 
    DROP EXTERNAL TABLE STG.DimSupplier;

CREATE EXTERNAL TABLE STG.DimSupplier
WITH 
(
  LOCATION = 'transformed/dimensions/dimsupplier/02',
  DATA_SOURCE = ExternalDataSourceDataLake,
  FILE_FORMAT = SynapseParquetFormat
) 
AS
SELECT CAST(ROW_NUMBER() OVER(ORDER BY S.SupplierID) AS TINYINT) + @MaxKey AS SupplierKey,
S.SupplierID,
S.SupplierName,
SC.SupplierCategoryName,
CAST(S.ValidFrom AS DATE) AS ValidFromDate
FROM LDW.vwIncrementalSuppliers S
LEFT JOIN LDW.vwSupplierCategories SC ON SC.SupplierCategoryID = S.SupplierCategoryID
WHERE S.FilePathDate = '2021-06-22'
ORDER BY S.SupplierID;