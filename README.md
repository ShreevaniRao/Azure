# **Azure Projects Repository**
#### This collection showcases end-to-end data engineering solutions and advanced analytics implementations. Below, you’ll find highlights of my work with Azure services.
---

## **Featured Projects**

### 1. [**Azure End-to-End Data Engineering Project**](https://github.com/ShreevaniRao/Azure/tree/main/End%20to%20End%20Data%20Engineering%20Project)

An end-to-end solution leveraging the **Medallion Architecture** to ingest, process, and analyze data using **Azure Data Factory (ADF)** and **Azure Databricks**.

**Key Features**:

- Staged data transformations across **Bronze, Silver, and Gold** layers.
- Automated pipelines for data ingestion, transformation, and load.
- Integration with **Power BI** for seamless analytics.

---

### 2. [**Azure Serverless Logical Data Warehouse**](https://github.com/ShreevaniRao/Azure/tree/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics))

A demonstration of serverless analytics with **Azure Synapse Analytics**, showcasing advanced SQL features and seamless integration with Power BI for insights.

**Key Features**:

- Implemented **CETAS (Create External Tables As Select)** and Incremental Load Design.
- Utilized **Change Data Capture (CDC)** for real-time updates.
- Demonstrated **SQL performance monitoring** and query optimization.

---

## 3. [**Azure Data Factory Pipelines**](https://github.com/ShreevaniRao/Azure/tree/main/Azure%20Data%20Factory)

Multiple pipelines developed to demonstrate below functions

1. **Data Ingestion Pipeline**: Automated ingestion of structured and unstructured data into Azure Data Lake.
2. **Transformations Pipeline**: ETL workflows built for scalable data processing.
3. **Orchestration Pipeline**: Dependencies managed using pipeline chaining, conditional execution, and alerts for monitoring.

---
## 4. [**Azure Databricks**](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Readme.md)

 [**ETL**](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/ETL/Readme.md)
- Scalable enterprise data platform built with **Azure Databricks** and **Azure Data Factory**
- Automated, end-to-end ETL for car sales data, incrementally loading from **GitHub API** and **Azure SQL Database** into **ADLS Gen2** using parameterized ADF pipelines
- Data processed through the **Medallion architecture** (Bronze, Silver, Gold layers) orchestrated by **Databricks Workflows**
- Implements **Change Data Capture (CDC)** for fact tables and **Slowly Changing Dimensions (SCD Type 1)** for dimension tables
- Enforces data governance and security with **Unity Catalog**
- Delivers a **star schema** modeled in **Delta tables** for efficient analytics and BI use

[**DLT**](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/README.md)

Project with steps for a data processing pipeline using Delta Live Tables (DLT) showcasing -
- **Incremental Loading**:
Streaming Tables automatically process only new data on each pipeline run.

- **Schema Evolution**:
Adding/modifying columns or renaming tables is handled automatically by DLT.

- **Autoloader Integration**:
Integrated **Autoloader** (spark.readStream.format("cloudFiles")) to ingest files from a landing volume.
Configured with options for schema hinting, schema location, file format, and path glob filter.
DLT managed checkpoint location for Autoloader automatically.

- **Append Flow**:
Used @dlt.**append_flow** to combine streaming data from multiple sources into a union Streaming Table.

- **Passing Parameters** (Dynamic Tables):
Pipeline configurations can be accessed within the DLT notebook using spark.conf.get.
Example: dynamically creating separate Gold Materialized Views filtered by order status.

- **Change Data Capture (CDC) with apply_changes**:
Used **@dlt.apply_changes** for SCD Type 1 and 2.
Tracked historical changes and handled deletes/truncates.
Updated downstream logic to read from SCD Type 2 table and filter for active records.

- **Data Quality with Expectations**:
Defined rules using **@dlt.expect and @dlt.expect_all**.
Actions: Warning (default), Drop, Fail.
Data quality metrics shown in UI and event logs.
