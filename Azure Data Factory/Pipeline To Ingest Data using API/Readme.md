
# Azure Data Factory Pipeline Overview: pl_getapidata

## Summary  
This pipeline provides a robust workflow for:
- Automating data retrieval from APIs  
- Storing data securely in ADLS Gen2  
- Loading cleaned and processed data into an Azure SQL Database
- Adding parameters enhances adaptability, supports multi-purpose workflows, and demonstrates advanced skills in designing maintainable pipelines—a valuable skill set for data engineering roles.

This pipeline performs the following tasks:  
1. **Retrieve CSV files from an API and store them in Azure Data Lake Storage Gen2 (ADLS Gen2)**  
2. **Load the CSV files from ADLS Gen2 into an Azure SQL Database**  

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20To%20Ingest%20Data%20using%20API/GetApiDataToAzureSqlDBPipelineRun.jpg" width="950" height="450"> 

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

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20To%20Extract%20data%20from%20API/GetApiData-Source.jpg" width="950" height="450">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20To%20Extract%20data%20from%20API/GetApiData-Sink.jpg" width="950" height="450">

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

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20To%20Extract%20data%20from%20API/GetApiData-AzureSqlDB-Source.jpg" width="950" height="450">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20To%20Extract%20data%20from%20API/GetApiData-AzureSqlDB-Sink.jpg" width="950" height="450">
---

## Parameters in the Pipeline
#### Pipeline Parameters
Pipeline parameters are used to make the pipeline reusable and dynamic by enabling external input. While not explicitly visible in the provided JSON, pipeline parameters can often be passed to activities like datasets. For example:

- Purpose: To reuse the pipeline for different configurations by modifying inputs like file names, storage paths, or API endpoints without rewriting the pipeline.
- Example: If there’s a parameter named "fileName", you could dynamically copy different files using the same pipeline logic.
  
#### Dataset Parameters
- Dataset parameters provide the flexibility to define dynamic values for the datasets used in the pipeline. In this JSON:
##### Relative URL Parameter in ds_http_csv
- "parameters": {
    "relativeurl": "ShreevaniRao/Azure/refs/heads/main/Azure%20Data%20Factory/Fact_Sales_2.csv"
}
- Purpose: Dynamically specify the endpoint path of the API URL.
- Reason: Useful for scenarios where the API has endpoints with dynamic paths based on the dataset. For example:
The pipeline can access different files (Fact_Sales_1.csv, Fact_Sales_3.csv) by modifying only the relativeurl.
##### Filename Parameter in ds_adlsg2_sourceapi_files
"parameters": {
    "filename": "Fact_Sales_2.csv"
}
- Purpose: Dynamically specify the file to be processed from ADLS Gen2.
- Reason: Essential for batch processing scenarios where the file names may change between runs or depend on an upstream process.
##### Table Name Parameter in ds_azure_sqltable_sink
"parameters": {
    "tablename": "Fact_Sales_2"
}
- Purpose: Specify the SQL table dynamically where the data should be written.
- Reason: Allows the same pipeline logic to work for different tables (e.g., Fact_Sales_1, Fact_Orders) by adjusting the parameter value.
## Benefits of Using Parameters
- Pipeline Reusability:
By making datasets and sinks dynamic, you can avoid creating multiple pipelines for similar tasks and instead use one with parameterized inputs.

- Operational Flexibility:
Modify or extend pipeline behavior at runtime without redeploying.

- Reduced Maintenance Effort:
When business rules change, like endpoint URLs or table mappings, only parameter values need to be updated rather than altering the pipeline design.
