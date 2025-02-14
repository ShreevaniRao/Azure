## 🚀 Enterprise Data Platform: Scalable ETL with Azure Databricks & Unity Catalog

**Project Summary:**

This project demonstrates the development of a robust and scalable ETL solution using Azure Databricks and Azure Data Factory. It showcases modern data engineering principles by automating the incremental loading and transformation of car sales data from an Azure SQL Database to a data lake, implementing Change Data Capture (CDC), and enforcing data governance using Unity Catalog. The solution culminates in a star schema data model optimized for analytical insights.

**Key Achievements:**

*   **Implemented Medallion Architecture:** Designed and implemented a Bronze-Silver-Gold architecture for progressive data refinement, ensuring data quality and analytical readiness.
*   **Automated Incremental Data Loading:** Developed an ADF pipeline that incrementally loads data from Azure SQL Database to ADLS Gen2 (Bronze layer) using parameterized datasets and Parquet format, optimizing for performance and cost efficiency.
*   **Developed CDC and SCD (Type 1) Processing:** Created Databricks workflows to process data, incorporating CDC for fact tables and SCD (Type 1) handling for dimension tables, ensuring data accuracy and consistency.
*   **Leveraged Unity Catalog for Data Governance:** Integrated Unity Catalog for centralized data governance, enabling data discovery, access control, and lineage tracking.
*   **Designed a Star Schema Data Model:** Developed a star schema in the Gold layer using PySpark, creating dimension and fact tables optimized for analytical queries.
*   **Automated ETL Pipeline with Databricks Workflows:** Orchestrated the entire ETL process using Databricks Workflows, including parallel task execution for optimized performance.

**Technical Architecture:**

*   **Data Source:** Azure SQL Database (`source_cars_data`)
*   **Data Lake:** Azure Data Lake Storage Gen2 (ADLS Gen2)
*   **ETL Engine:** Azure Databricks (PySpark)
*   **Orchestration:** Azure Data Factory
*   **Data Governance:** Unity Catalog
*   **Data Modeling:** Star Schema
*   **Data Consumption:** Power BI (or other BI tools)

**Data Flow Stages:**

1.  **Bronze Layer (Raw Data Ingestion):**
    *   Objective: Capture raw data from the source system with minimal transformations.
    *   Implementation: ADF pipeline incrementally copies data from Azure SQL Database to ADLS Gen2 (Bronze layer) in Parquet format.
    *   Key Technologies: Azure Data Factory, Azure SQL Database, ADLS Gen2, Parquet format.
2.  **Silver Layer (Data Cleansing & Standardization):**
    *   Objective: Enforce data quality, validate schemas, and standardize data formats.
    *   Implementation: Databricks notebook (`silver_notebook.py`) reads Bronze layer data, performs transformations, and writes the transformed data to the Silver layer in Delta Lake format.
    *   Key Technologies: Azure Databricks, PySpark, Delta Lake, Unity Catalog.
    *   Configurations:
        *   Unity Catalog: Configured Unity Catalog to manage metadata and access control.
        *   Databricks Access Connector: Configured a Databricks Access Connector to enable secure access to ADLS Gen2.
        *   External Locations: Created external locations mapping to Bronze, Silver, and Gold storage containers.
        *   Spark Cluster: Configured a Unity Catalog-enabled Spark cluster.
3.  **Gold Layer (Business-Ready Analytics):**
    *   Objective: Aggregate data, implement dimensional modeling (star schema), and optimize for reporting and analysis.
    *   Implementation: Databricks notebooks (`gold_dim_*.py`, `gold_fact_sales.py`) read Silver layer data, create dimension and fact tables, and write the data to the Gold layer in Delta Lake format.
    *   Key Technologies: Azure Databricks, PySpark, Delta Lake, Unity Catalog, Star Schema.
    *   Highlights:
        *   Dynamically parameterizes pipeline runs for incremental loads.
        *   Implements SCD Type 1 handling for dimension tables.
        *   Uses surrogate keys for dimension tables.

**Azure Data Factory Pipeline Details:**

*   The ADF pipeline incrementally copies data from the `source_cars_data` table in Azure SQL Database to the Bronze layer in ADLS Gen2.
*   It utilizes a `watermark` table to track the last loaded `date_id`, enabling incremental data extraction.
*   Key activities include:
    *   `CopyGitData`: Copies configuration data from a Git repository to Azure SQL Database.
    *   `LastLoad`: Looks up the last loaded `date_id` from the `watermark` table.
    *   `CurrentLoad`: Looks up the maximum `date_id` from the `source_cars_data` table.
    *   `Copy data to Bronze Layer`: Copies data from `source_cars_data` to ADLS Gen2 (Bronze).
    *   `UpdateWatermarkTable`: Updates the `watermark` table with the latest `max_date` loaded.

**Databricks Workflow Details:**

*   The project leverages Databricks Workflows to automate the entire ETL process.
*   The workflow consists of multiple tasks, including:
    *   Executing the `silver_notebook.py` notebook to transform data in the Silver layer.
    *   Executing the `gold_dim_*.py` and `gold_fact_sales.py` notebooks to create dimension and fact tables in the Gold layer.
*   Tasks are parallelized to optimize pipeline performance.

**Challenges & Solutions:**

*   **Data Quality Issues:** Implemented data quality checks in the Silver layer to identify and resolve inconsistencies.
*   **Performance Optimization:** Optimized pipeline performance by using incremental loading, Delta Lake, and parallel task execution.
*   **Data Governance:** Addressed data governance requirements by implementing Unity Catalog for centralized data management.

**Conclusion:**

This project demonstrates the ability to build a scalable, governed, and production-ready data lake using Azure Databricks, Azure Data Factory, and Unity Catalog. It showcases skills in data modeling, ETL development, data governance, and cloud computing. This project serves as a valuable asset for organizations looking to modernize their data infrastructure and unlock the value of their data.

**Links:**

*   [Unity Catalog setup](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/get-started)
*   [Create Access Connector](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/azure-managed-identities)
*   [silver_notebook](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/Notebooks/silver_notebook.py)
*   [gold_dim_branch](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/Notebooks/gold_dim_branch.py)
*   [gold_dim_dealer](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/Notebooks/gold_dim_dealer.py)
*   [gold_dim_model](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/Notebooks/gold_dim_model.py)
*   [gold_dim_date](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/Notebooks/gold_dim_date.py)
*   [gold_fact_sales](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/Notebooks/gold_fact_sales.py)

**Images:**

*   [PipelineArchitecture](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/PipelineArchitecture.jpg)
*   [ADFPipeline](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/ADFPipeline.jpg)
*   [CompleteIncrementalPipelineRun](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/CompleteIncrementalPipelineRun.jpg)
*   [CarsUnityCatalog](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/CarsUnityCatalog.jpg)
*   [UnityCatalogStorageCredential](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/UnityCatalogStorageCredential.jpg)
*   [UnityCatalogExternalLocations](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/UnityCatalogExternalLocations.jpg)
*   [DBSparkClusterCompute](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/DBSparkClusterCompute.jpg)
*   [Catalog-Schema-Table](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/Catalog-Schema-Table.jpg)
*   [STARSchema](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/STARSchema.jpg)
*   [WorkflowJobs](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/WorkflowJobs.jpg)
*   [ParellelWorkFlowJobs](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/ParellelWorkFlowJobs.jpg)
*   [FailedIncrementlLoadWorkflow](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/FailedIncrementlLoadWorkflow.jpg)
*   [Troubleshoot&DebugScript](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/Troubleshoot&DebugScript.jpg)
*   [FailedRunOfWorkFlow](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/FailedRunOfWorkFlow.jpg)
*   [SuccessfulIncrementalLoadRun](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/SuccessfulIncrementalLoadRun.jpg)
*   [VerifyIncrementalLoadData](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/Assets/VerifyIncrementalLoadData.jpg)

