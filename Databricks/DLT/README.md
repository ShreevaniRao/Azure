 # 🚀 [Delta Live Tables (DLT)](https://docs.databricks.com/aws/en/dlt) Pipeline Overview

This repository outlines the steps for a data processing pipeline using **[Delta Live Tables (DLT)](https://docs.databricks.com/aws/en/dlt)**, a [declarative framework](https://docs.databricks.com/gcp/en/data-engineering/procedural-vs-declarative) built by Databricks for reliable ETL processing.  
DLT simplifies pipeline development by handling orchestration automation, cluster management, data quality, and error handling automatically, enabling developers to focus on transformations.

### <u>[Go To -> DLT Pipeline Details](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/DLT%20Project.md)</u>
---

## Table of Contents

1. [Project Setup and Prerequisites](#project-setup-and-prerequisites)
2. [Understanding Delta Live Tables Data Sets](#understanding-delta-live-tables-data-sets)
3. [Creating the DLT Pipeline](#creating-the-dlt-pipeline)
4. [Building the Data Pipeline (Logical Flow)](#building-the-data-pipeline-logical-flow)
5. [Key DLT Features Explored](#key-dlt-features-explored)
6. [DLT Internals and Observability](#dlt-internals-and-observability)

---

## Project Setup and Prerequisites

 **Note:** Delta Live Tables require a Premium Databricks plan.
- **Schema Creation:**  
  Created a new schema called `etl` under the `dlt-catalog` catalog to house all DLT artifacts.

- **Sample Data:**  
  - Used Databricks sample data: `samples.tpch.orders` and `samples.tpch.customer`.
  - Deep clones created for tables as `orders_raw` and `customer_raw`.

- **Autoloader Preparation:**  
  - Created a managed volume `autoloader` in `dlt-catalog.etl`.
  - Uploaded csv files:

- **Setup Notebook:**  
  [dlt setup (source code)](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/Notebooks/dlt%20setup.py) - Used to execute initial schema, cloning, and volume creation steps.

- **Source Table Enhancements:**  
  - Added columns to `customer_raw`:
    - `Source_action` (indicates operations like insert, delete, truncate)
    - `Source_insert_date` (timestamp for tracking changes)
  - Populated new columns with default values for existing records.

---

## Understanding Delta Live Tables Data Sets

DLT pipelines operate using three primary types of datasets:

- **Streaming Tables:**  
  A [streaming table](https://docs.databricks.com/gcp/en/dlt/streaming-tables) in Databricks is a Delta table specifically designed to support streaming or incremental data processing. Unlike traditional tables that are typically loaded in batches, a streaming table is continuously updated as new data arrives from streaming sources, such as files landing in cloud storage or messages from a data stream.They are typically used for initial ingestion layers (e.g., Bronze).

- **Materialized Views:**  
  A [materialized view](https://docs.databricks.com/aws/en/dlt/materialized-views) is a special kind of database object that stores the results of a query as a physical table, enabling fast access to precomputed data and reducing the need to recalculate results each time the view is queried.Generally used for transformations, aggregations, and computations. They provide an up-to-date view of the data based on the defined query. Often used for Silver and Gold layers

- **Views:**  
  Temporary intermediate transformations that are not stored at the target schema. Useful for breaking down complex logic within the pipeline.

---

## Setting up the DLT Pipeline configuration

The DLT pipeline was created using the Databricks UI:

- Initiated a new DLT pipeline by selecting "ETL pipelines".
- Provided a pipeline name (e.g., `dlt_01`).
- Selected a Product Edition (Core, Pro, Advanced) depending on the DLT feature in use.
- Chose a Pipeline Mode (Triggered or Continuous).
- Specified the path to the [**DLT pipeline notebook(source code)**](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/Notebooks/dlt.py) containing transformation code.
- Defined the target schema (e.g., `dlt-catalog.etl`).
- Configured compute settings (number of workers, worker type).
- Added optional configurations for dynamic pipeline parameters.

---

## Building the Data Pipeline (Logical Flow)

The project followed a multi-layered [Medallion architecture](https://docs.databricks.com/gcp/en/lakehouse/medallion) (Bronze, Silver, Gold):

### Bronze Layer (Ingestion)
Data is ingested from raw sources (like Delta tables or files) into Streaming Tables or Materialized Views
- **Orders:**  
  Read from `orders_raw` as a Streaming Table using `@dlt.table` and `spark.readStream.table` into a orders_bronze Streaming Table.
- **Customer:**  
  Read from `customer_raw` as a batch source for a Materialized View using `@dlt.table` and `spark.read.table`.
- **Properties:**  
  Included optional table properties (like `quality`) and comments.

### Intermediate Layer (Joining)

- Created a View - order_customer_view to join the orders bronze Streaming Table and the customer bronze Materialized View using `@dlt.view`.
- Used the `LIVE.` keyword to reference pipeline datasets (e.g., `LIVE.orders_bronze`).
- Join logic defined with Spark DataFrame operations (e.g., left_outer join on customer key).

### Silver Layer (Transformations)

- Created a Materialized View `customerOrders_silver` from the intermediate join view using `@dlt.table`.
- Added an `insert_date` column using `current_timestamp`.

### Gold Layer (Aggregation)

- Created a final Materialized View (e.g., `orders_aggregated_gold`) from the `customerOrders_silver` table using `@dlt.table`.
- Performed aggregations based on `Market_segment` (e.g., counting `order_keys`, summing `total_price`).
- Added an `insert_date` column.

---

## Key DLT Features Explored

- **Incremental Loading:**  
  Streaming Tables automatically process only new data on each pipeline run.

- **Schema Evolution:**  
  Adding/modifying columns or renaming tables is handled automatically by DLT.

- **Autoloader Integration:**  
  Integrated Autoloader (`spark.readStream.format("cloudFiles")`) to ingest files from a landing volume.  
  Configured with options for schema hinting, schema location, file format, and path glob filter.  
  DLT managed checkpoint location for Autoloader automatically.

- **Append Flow:**  
  Used `@dlt.append_flow` to combine streaming data from multiple sources into a union Streaming Table (`orders_union_bronze`).

- **Passing Parameters (Dynamic Tables):**  
  Pipeline configurations can be accessed within the DLT notebook using `spark.conf.get`.  
  Example: dynamically creating separate Gold Materialized Views filtered by order status.

- **Change Data Capture (CDC) with `apply_changes`:**  
  - Used `@dlt.apply_changes` for SCD Type 1 and 2.
  - Tracked historical changes and handled deletes/truncates.
  - Updated downstream logic to read from SCD Type 2 table and filter for active records.

- **Data Quality with Expectations:**  
  - Defined rules using `@dlt.expect` and `@dlt.expect_all`.
  - Actions: Warning (default), Drop, Fail.
  - Data quality metrics shown in UI and event logs.

---

## DLT Internals and Observability

- **Managed Datasets:**  
  DLT datasets are managed by the pipeline and tied to a specific pipeline ID. Deleting the pipeline deletes the datasets.

- **Internal Storage:**  
  Streaming Tables and Materialized Views are abstractions over internal Delta tables stored in a hidden schema.

- **Checkpointing:**  
  Streaming Tables maintain incremental state using checkpoint locations within the DLT managed storage.

- **Data Lineage:**  
  Powered by Unity Catalog, DLT pipelines automatically capture and visualize data lineage down to the column level.

- **Monitoring:**  
  DLT pipelines can be monitored via the UI (pipeline graph, update details, event logs) or by querying the event log directly for dashboards.

---

## Summary

By using these DLT features, this project demonstrates how to build a robust, maintainable, and observable data pipeline capable of handling common data engineering patterns like incremental loading, CDC, and data quality enforcement declaratively.

**DLT enables declarative, production-grade data engineering with minimal operational overhead.**

---


