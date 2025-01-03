
# Pipeline Overview: pl_getapidata

This pipeline performs the following tasks:  
1. **Retrieve CSV files from an API and store them in Azure Data Lake Storage Gen2 (ADLS Gen2)**  
2. **Load the CSV files from ADLS Gen2 into an Azure SQL Database**  
<!img
---

## Steps

### **1. ac_copy_api_adlsg2**
**Description**: Retrieve CSV files via an HTTP request and store them in ADLS Gen2.

- **Source**:
  - Source Type: HTTP using a GET request
  - File Format: Delimited Text (e.g., CSV)  
  - Source Dataset: `ds_http_csv`  
- **Sink**:
  - Sink Type: ADLS Gen2  
  - File Format: Delimited Text (with `.txt` extension and quotes around all fields)  
  - Sink Dataset: `ds_adlsg2_sourceapi_files`  


---

### **2. ac_copy_adlsg2_sqldb**  
**Description**: Transfer the CSV files from ADLS Gen2 to an Azure SQL Database.

- **Source**:  
  - Source Type: ADLS Gen2 (recursive file access disabled)  
  - Source Dataset: `ds_adlsg2_sourceapi_files`  
  - Filename: `Fact_Sales_2.csv`  
- **Sink**:  
  - Sink Type: Azure SQL Database  
  - Sink Dataset: `ds_azure_sqltable_sink`  
  - Table Name: `Fact_Sales_2`  
  - Write Behavior: Insert rows  
  - Pre-Copy Script: `truncate table Fact_Sales_2`  

**Column Mappings**:
The pipeline maps fields from the CSV to SQL table columns with data conversion:
| **CSV Field**       | **SQL Column**       | **Type**     |
|----------------------|----------------------|--------------|
| `transaction_id`     | `transaction_id`     | nvarchar     |
| `transactional_date` | `transactional_date` | nvarchar     |
| `product_id`         | `product_id`         | nvarchar     |
| `customer_id`        | `customer_id`        | nvarchar     |
| `payment`            | `payment`            | nvarchar     |
| `credit_card`        | `credit_card`        | nvarchar     |
| `loyalty_card`       | `loyalty_card`       | nvarchar     |
| `cost`               | `cost`               | nvarchar     |
| `quantity`           | `quantity`           | nvarchar     |
| `price`              | `price`              | nvarchar     |  

**Dependencies**:  
This activity depends on the successful completion of `ac_copy_api_adlsg2`.  

---

## Summary  
This pipeline provides a robust workflow for:
- Automating data retrieval from APIs  
- Storing data securely in ADLS Gen2  
- Loading cleaned and processed data into an Azure SQL Database  
