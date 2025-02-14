# 🚀 Databricks ETL Project: Enterprise Data Platform

## 📋 Project Overview

This project implements a robust and scalable enterprise data platform, showcasing advanced data engineering principles using Azure Databricks and Azure Data Factory. It automates the end-to-end ETL process, incrementally loading car sales data from an Azure SQL Database into an Azure Data Lake Storage Gen2 (ADLS Gen2) Bronze layer using a parameterized ADF pipeline. Leveraging Databricks Workflows, the pipeline orchestrates the progressive processing and transformation of data through the Medallion architecture (Bronze, Silver, and Gold layers). The solution incorporates Change Data Capture (CDC) for the Fact table, Slowly Changing Dimensions (SCD Type 1) handling for Dimension tables, and enforces comprehensive data governance using Unity Catalog. The project culminates in a well-designed star schema data model optimized for efficient and insightful analytical queries.

## 🎯 Project Objectives

### Primary Goals & Achievements
- **Implemented Medallion Architecture**: Designed and implemented a Bronze-Silver-Gold architecture for progressive data refinement, ensuring data quality and analytical readiness.
- **Automated Incremental Data Loading**: Developed an ADF pipeline that incrementally loads data from Azure SQL Database to ADLS Gen2 (Bronze layer) using parameterized datasets and Parquet format, optimizing for performance and cost efficiency.
- **Developed CDC and SCD (Type 1) Processing**: Created Databricks workflows to process data, incorporating CDC for fact tables and SCD (Type 1) handling for dimension tables, ensuring data accuracy and consistency.
- **Leveraged Unity Catalog for Data Governance**: Integrated Unity Catalog for centralized data governance, enabling data discovery, access control, and lineage tracking.
- **Designed a Star Schema Data Model**: Developed a star schema in the Gold layer using PySpark, creating dimension and fact tables optimized for analytical queries.
- **Automated ETL Pipeline with Databricks Workflows**: Orchestrated the entire ETL process using Databricks Workflows, including parallel task execution for optimized performance.

### Technical Architecture

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/PipelineArchitecture.jpg" width="900" height="450">

- **Architecture**: Medallion (Bronze, Silver, Gold Layers)
- **Governance Framework**: Unity Catalog
- **Design Pattern**: Star Schema
- **Processing Engine**: Apache Spark
- **Platform**: Azure Databricks & Data Factory
- **Consumption:** Power BI (or other BI tools) connects to the Gold layer for reporting.

### Data Flow Stages
1. **Bronze Layer**: Raw Data Ingestion
   - Capture source system data
   - Minimal transformations
   - Preserve data lineage
     ## ADF Pipeline: Incremental Data Load

      This Azure Data Factory pipeline performs an initial & incremental car sales data load from a Github repository to Azure SQL Database.
      Finally from the Azure table the car sales data is copied to the Bronze layer container of the Data lake.
      
      This pipeline needs an initial setup of creating 2 Azure Sql tables & a Stored Procedure -
     
      1. 'Source_Cars_Data' table is used to ingest data from a csv file in the Github, containing data of car sales. 
      2. 'Watermark' table to mark the last data ingested.
      3. 'UpdateWatermarkTable' - that updates & marks the last load date.
  
         <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/ADFPipeline.jpg" width="700" height="450">
      **Pipeline Activities:**
     
   *   **`CopyGitData`**:
       *   Copies a delimited text file from a Git repository to an Azure SQL table.
       *   Purpose: Loads initial configuration data (e.g., Branch IDs, Dealer IDs, Model IDs).
       *   **Source:**
           *   Delimited text file.
           *   Accessed via HTTP Linked Service (GET request).
           **Dataset Parameter:** Uses load_flag that accepts the csv file name to dynamically built the relative url for initial and incremental loads
       *   **Sink:** Azure SQL Database.
       *   **Type Conversion:** Imports Schema from the Git file for the Azure SQL table.
   *   **`LastLoad`**:
       *   Looks up the last loaded `date_id` from the `watermark` table in Azure SQL.
       *   Purpose: Determines the starting point for incremental data extraction.
       *   SQL Query: `select last_load from watermark`
       *   **Dataset Parameter:** Uses the `ds_AzureSqlTable` dataset, parameterized with `table_name = "watermark"`.
   *   **`CurrentLoad`**:
       *   Looks up the maximum `date_id` from the `source_cars_data` table in Azure SQL.
       *   Purpose: Determines the latest available date for data extraction.
       *   SQL Query: `select max(date_id) as max_date from source_cars_data`
       *   **Dataset Parameter:** Uses the `ds_AzureSqlTable` dataset, parameterized with `table_name = "source_cars_data"`.
   *   **`Copy data to Bronze Layer`**:
       *   Copies data from `source_cars_data` (Azure SQL) to a Parquet file in Bronze container of Azure Data Lake Storage.
       *   **Incremental Load:** Selects data based on the `date_id` column, filtering for records greater than `LastLoad` and less than or equal to `CurrentLoad`.
       *   SQL Query (Parameterized):
           ```
           SELECT * FROM source_cars_data
           WHERE date_id > '@{activity('LastLoad').output.firstRow.last_load}'
             AND date_id <= '@{activity('CurrentLoad').output.firstRow.max_date}'
           ```
       *   **Source Dataset Parameter:** Uses the `ds_AzureSqlTable` dataset, parameterized with `table_name = "source_cars_data"`.
       *   **Sink Dataset:** Uses the `ds_datalake` dataset (points to the Bronze layer in ADLS).
       *   **Data Type Mappings:** Converts source data types (varchar, bigint, int) to Parquet-compatible types (UTF8, INT_64, INT_32).  Specific examples:
           *   `varchar` to `UTF8`
           *   `bigint` to `INT_64`
           *   `int` to `INT_32`
   *   **`UpdateWatermarkTable`**:
       *   Updates the `watermark` table in Azure SQL with the latest `max_date` loaded.
       *   Purpose: Ensures that the next pipeline run picks up only new data.
       *   Stored Procedure: `[dbo].[UpdateWatermarkTable]`
       *   **Parameter:** `@lastload = @{activity('CurrentLoad').output.firstRow.max_date}` (Expression dynamically sets the `lastload` parameter with the maximum `date_id`).
       *   **Linked Service:** Uses the `ls_SqlDb` linked service to connect to the Azure SQL Database.
      
      **Data Flow:**
      1.  Git Repository (via HTTP API) --> Azure SQL (Initial Configuration - `CopyGitData`)
      2.  Azure SQL (Source) --> Azure Data Lake Storage (Bronze Layer - `Copy data to Bronze Layer`)

    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/CompleteIncrementalPipelineRun.jpg" width="700" height="450">

3. **Silver Layer**: Data Cleansing & Standardization
   - Data quality enforcement
   - Schema validation
   - Consistent data formatting
     
   In this step Azure Databricks resource is created and Unity Catalog, Databricks Access Connector, Storage Credentials, External Data Locations & Spark cluster are setup as below -

   **Unity Catalog Configuration:** - Follow this [Unity Catalog setup](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/get-started) link to create your own Catalog and assign Azure managed identity(DB Access connector) to access the Data lake storage containers.
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/CarsUnityCatalog.jpg" width="700" height="450">
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/UnityCatalogDetails.jpg" width="600" height="250">
   

   **Databricks Access Connector:** -  Follow this [Create Access Connector](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/azure-managed-identities) link to setup this Storage credentials to access data lake
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/UnityCatalogStorageCredential.jpg" width="550" height="220">

   **Create External Location:** - Setup external locations that map to the 3 data lake storage containers - Bronze, Silver & Gold (need to be created manually ahead) which will have databricks read and write delta tables to these locations
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/UnityCatalogExternalLocations.jpg" width="500" height="300">
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/ExternalLocationForUnityCatalog.jpg" width="500" height="300">
   
   **Spark Cluster:** - Created a Personal Compute cluster (verified Unity Catalog enabled)
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/DBSparkClusterCompute.jpg" width="575" height="270">
   
   Created a new folder repository - 'CarsProject' to organize the pyspark notebooks artefacts in the Workspace.

   **Catalog-Schema-Table:** - Created 'Cars-Catalog' Unity Catalog and used it to contain the 2 schemas - 'Silver' & ' Gold'. All the Delta Tables created will be using this data hierarchy to make use of a structured system. Refer to [db_notebook](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/Notebooks/db_notebook.py) for this setup.

   **[silver_notebook](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/Notebooks/silver_notebook.py):** - Pyspark notebook to read the Bronze layer data to transform the data for adding new columns by splitting the existing column data, creating new calculated columns and also aggregate the existing data to perform ad-hoc query using vizualizatons like pie chart.
   Finally writing the transformed data to the Silver container in parquet file format that can be leveraged for data analytics.

4. **Gold Layer**: Business-Ready Analytics
   - Aggregated insights
   - Dimensional modeling
   - Optimized for reporting

      + In this stage multiple pyspark notebooks are used to create **STAR schema dimensional modeling** consuming the transformed Silver container data and splitting into 1 Fact & 4 Dimensional tables and saving them simultaneously into Unity Catalog data hierarchy **'Catalog-Schema-Table(Delta)'** and into Gold data lake container.
      + All these pyspark notebooks use **Databricks Widgets** to parameterize the pipeline run for incremental load with user input.
      + Every pyspark notebook dynamically checks for load type and accordingly creates a Delta table or **upserts** the existing Delta table (SCD Type 1).
      + The new Delta Dimensional tables created first are assigned a new **Surrogate key** and its unique serial value generated.
      + The new Fact table created uses 4 Dimension table's business keys & surrogate keys to join and filter the data to load.
      + Every notebook can be run multiple times to verify and validate the row count is accurate & valid.
      + Every notebook also writes and saves the Dimension and Fact tables in the Gold Data lake container in **Delta file format**.
        
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/Catalog-Schema-Table.jpg" width="575" height="270">
  
      
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/STARSchema.jpg" width="575" height="270">

      **[gold_dim_branch](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/Notebooks/gold_dim_branch.py):** - Creates cars-catalog.gold.dim_branch
      
      **[gold_dim_dealer](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/Notebooks/gold_dim_dealer.py):** - Creates cars-catalog.gold.dim_dealer
      
      **[gold_dim_model](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/Notebooks/gold_dim_model.py):** - Creates cars-catalog.gold.dim_model
      
      **[gold_dim_date](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/Notebooks/gold_dim_date.py):** - Creates cars-catalog.gold.dim_date
      
      **[gold_fact_sales](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/Notebooks/gold_fact_sales.py):**- Creates cars-catalog.gold.fact_carsales

5. **Complete ETL pipeline using Databricks Workflows**
   
      Created a Job to run multiple tasks to automate all the above pyspark notebooks. Further parallelized the tasks runs, to process the notebooks parallely to optimize the pipeline.
   
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/WorkflowJobs.jpg" width="775" height="370">
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/ParellelWorkFlowJobs.jpg" width="775" height="570">
   
7. **Debug, Troubleshoot & Validate the data**
   
      Multiple runs of the notebooks execution and job runs resulted in ability to learn to diagnose, debug and troubleshoot the issues.
   
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/FailedIncrementlLoadWorkflow.jpg" width="775" height="570">
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/Troubleshoot&DebugScript.jpg" width="775" height="570">
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/FailedRunOfWorkFlow.jpg" width="775" height="570">  
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/WorkflowRuns.jpg" width="775" height="570"> 
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/SuccessfulIncrementalLoadRun.jpg" width="775" height="570">
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/VerifyIncrementalLoadData.jpg" width="775" height="570">
   
8. **Alternate solution & approach**

   Alternately the Databricks notebooks can be executed in the ADF pipeline which will trigger the Databricks Workflow and can be monitored for the similar output.
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/AlternateSolution.jpg" width="1000" height="570">

9 **Unity Catalog - Data Governance with Unity Catalog: Managing Metadata, Access Control, and Lineage**

   Below details showcases the way Unity Catalog can be leveraged to
   Grant granular access to tables -
   
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/UnityCatalogGranularACL.jpg" width="1000" height="570">

   Track the lineage of any asset -
   
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/UnityCatalogLineage.jpg" width="900" height="470">

   Illustrates metadata enrichment and data discoverability -
    
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/UnityCatalogDataDiscovery.jpg" width="900" height="300">
    
   

