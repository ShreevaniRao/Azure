## Pipeline Construction Steps

This project follows the progression shown in the below provided steps, to build the DLT pipeline with these quick link features & insights learnt along each stage.

## Quick Links
   #### Notebooks - [Setup ](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/Notebooks/dlt%20setup.py) & [DLT Pipeline Notebook](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/Notebooks/dlt.py)
 
1. [Intro to Delta Live Tables (DLT)](#introduction-to-delta-live-tables-dlt)
2. [DLT Internals & Incremental Load](#2-dlt-internals--incremental-load)
3. [DLT Append Flow & Autoloader](#3-dlt-append-flow--autoloader)
4. [Change Data Capture (CDC) - SCD2 & SCD1](#4-change-data-capture-cdc---scd2--scd1)
5. [DLT Data Quality & Expectations](#5-dlt-data-quality--expectations)
6. [Outro](#6-outro)
   
### Introduction to Delta Live Tables (DLT)

This DLT pipeline as a declarative framework in Databricks designed to simplify ETL pipelines by handling orchestration, cluster management, data quality, and error handling. It requires the **Premium plan** of Databricks.

**Steps:**

*   **Set up the Environment:**
    *   Used a [setup](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/Notebooks/dlt%20setup.py) notebook to **create a new catalog & schema** -> `etl` under the `dlt-catalog` catalog for the DLT run.
    *   **Deep cloned sample data** (e.g., `orders` and `customer` from `samples.tpch`) into raw tables (e.g., `etl.bronze.orders_raw`, `etl.bronze.customer_raw`) to use as source data.
    *   **Insight:** Setting up a dedicated schema and cloning data provides a clean, repeatable starting point for the pipeline development. Using `deep clone` creates independent copies of the source data.
      </br>
          <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/DLTInitialSetup%26Queries.jpg" width="900" height="450">

*   [**Understand DLT Dataset Types:(When to use what)**](https://docs.databricks.com/aws/en/dlt/transform)
    *   Learned about the three main types of datasets in DLT: **Streaming Tables**, **Materialized Views**, and **Views** .
    *   **Streaming Tables** are used for streaming sources and processing incremental data, allowing data to be appended.
    *   **Materialized Views** are generally used for transformations, aggregations, or computations.
    *   **Views** are typically used for intermediate transformations and are **not stored** at the target schema.
    *   Understood that DLT pipelines are powered by **Delta Lake**, inheriting its **ACID** capabilities.
    *   **Insight:** Choosing the right dataset type is crucial for defining how data is processed and stored. Streaming tables are key for efficiency with ever-growing data.

*   **[DLT](https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/Notebooks/dlt.py) Code to create the DLT Datasets:**

    *   DLT code can be written in **Python or SQL** and requires a special **job compute** type, not the standard all-purpose compute.
    *   Imported the necessary **`dlt` Python module**.
    *   **Created a Streaming Table** (`orders_bronze`) for the `orders_raw` source using the `@dlt.table` decorator and `spark.readStream.table()` to read the Delta table as a streaming source. Added optional table properties like `quality` and a comment.
    *   **Created a Materialized View** (`customer_bronze`) for the `customer_raw` source using the `@dlt.table` decorator and `spark.read.table()` to read the Delta table as a batch source. Used the `name` parameter to explicitly set the table name.
    *   **Insight:** The `@dlt.table` and `@dlt.view` decorators, along with the `dlt` module, are the core building blocks for defining datasets and transformations in DLT. The key difference between streaming tables and materialized views often lies in how their source is read (`readStream` vs `read`).
      </br>
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/CreateInitialStreamingTable%26MatView.jpg" width="700" height="450">

*   **Define Intermediate and Final Transformations:**
    *   **Created a View** (`order_customer_view`) to join the `orders_bronze` streaming table and `customer_bronze` materialized view. Used the `@dlt.view` decorator and read the datasets using the **`LIVE` keyword** (`LIVE.customer_bronze`, `LIVE.orders_bronze`) to reference datasets within the same pipeline.
    *   **Created a Silver Materialized View** (`order_customer_view`) by reading the `customer_bronze_view` and adding a new column (`insert_date`) with the current timestamp. Changed the `quality` property to `silver`.
    *   **Created a Gold Materialized View** (`orders_aggregated_gold`) by reading the `joined_silver` table, performing aggregations (e.g., `count(order_key)`) grouped by `market_segment`, and adding an `insert_date` column. Set the `quality` property to `gold.
    *   **Insight:** Views are useful for breaking down complex transformations into logical steps without persisting intermediate results. Reading datasets within the same pipeline using `LIVE` is essential for chaining transformations. Aggregations typically produce materialized views.
      </br>
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/CreateViewAndSilver%26GoldAssets.jpg" width="700" height="450">

*   **Create and Configure the DLT Pipeline:**
    *   Created a new DLT pipeline via the Databricks UI (New -> DLT pipelines or ETL pipelines).
    *   Configured pipeline settings: **Name**, **Product Edition** (starting with Core), **Pipeline Mode** (Triggered or Continuous - started with Triggered) , selected the notebook path, specified **Unity Catalog** settings (Catalog and Schema), and configured compute (number of workers, driver type).
    *   **Insight:** The product edition dictates available features (Core: basic ETL; Pro: CDC; Advanced: Data Quality). Triggered mode is suitable for scheduled batch runs, while Continuous is for low-latency streaming. Choose the pipeline mode based on the latency and cost requirements for your pipeline. Triggered pipelines update once and then shut down the cluster until the next manual or scheduled update. Continuous pipelines keep an always running cluster that ingests new data as it arrives. This property can be changed as your requirements evolve. Integrating with Unity Catalog ensures data governance
      </br>
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/InitialCorePipelineSettings.jpg" width="700" height="450">

*   **Run and Debug the Pipeline:**
    *   Started the pipeline run using the UI.
    *   Observed pipeline status (Initializing, Setting up tables, Running, Completed/Failed).
    *   Used the [**Development mode**](https://learn.microsoft.com/en-us/azure/databricks/dlt/updates#development-and-production-modes) for easy debugging, as the cluster remains running even if the pipeline fails. Production mode terminates the cluster on success or failure to save costs.
    *   Identified and fixed errors by examining the **Event Log** (e.g., unimported functions like `count`, incorrect column names).
    *   Reran the pipeline after correcting code.
    *   **Insight:** Development mode is invaluable during the initial build and debugging phase. The Event Log provides detailed information about pipeline execution and failures, making troubleshooting efficient.
      </br>
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/DebugPipelineRunWithErrors.jpg" width="700" height="450">
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/CorrectedPipelineErrorWithGoodGraph.jpg" width="700" height="450">


*   **Verify Pipeline Output:**
    *   Examined the Databricks Catalog to see the created datasets. Confirmed that Streaming Tables and Materialized Views were created, while Views were not persisted.
    *   Queried the final gold table (`orders_aggregated_gold`) to verify the aggregated data.
    *   Terminated the DLT cluster after successful development runs to manage costs.
    *   **Insight:** DLT automatically manages the creation and storage of specified tables and materialized views based on the defined code. Views are temporary constructs used only during the pipeline run.

       <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/QueryTheGold%26VerifyOtherDataAssets.jpg" width="900" height="750">


###   2: DLT Internals & Incremental Load

This dives deeper into DLT's internal workings, focusing on how it handles incremental data and dataset management, and introduces features for modifying/renaming tables and data lineage.

**Steps:**

*   **Understand Dataset Management:**
    *   Learned that DLT manages all datasets (Streaming Tables, Materialized Views, Views) created within a pipeline and ties them to a specific **Pipeline ID**.
    *   Deleting a DLT pipeline **deletes all associated datasets**.
    *   **Insight:** This integrated management simplifies data lifecycle handling for pipeline-generated data, ensuring consistency between the pipeline definition and its output.

*   **Process Incremental Data:**
    *   Inserted new records into the source `orders_raw` table (the source for the `orders_bronze` streaming table).
    *   Reran the DLT pipeline (in Triggered mode).
    *   Observed that the `orders_bronze` streaming table **only read the newly inserted incremental records** (e.g., 10k records) during the run, demonstrating efficient incremental processing.
    *   Confirmed the final aggregated gold table reflected the new data, with increased counts.
    *   **Insight:** Streaming tables in DLT are designed for incremental processing. When their source is updated, they only process the new changes on subsequent runs, which is crucial for performance and cost-effectiveness with large datasets.
       </br>
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/IncrementalDataLoadedGraph.jpg" width="750" height="550">
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/GoldViewInitialRecordsCounts.jpg" width="350" height="150">
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/GoldViewAfterIncrementRecordsCounts.jpg" width="350" height="150">


*   **Schema Evolution - Modify and Add Columns:**
    *   Modified the DLT code to **add a new aggregated column** (`sum_of_total_price`) and **rename an existing column** (`count_orders`) in the `orders_aggregated_gold` materialized view.
    *   Validated the code changes within the notebook while connected to the DLT pipeline in development mode. (Corrected errors like unimported functions or incorrect column names during validation).
    *   Reran the DLT pipeline.
    *   Verified that the final gold table now contained the renamed and newly added columns.
    *   **Insight:** DLT's declarative nature simplifies schema changes. You just update the desired schema/transformation in the code, and DLT handles the underlying table updates and schema evolution automatically.
      </br>
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/GraphForAddingNewColumn%26RenameColInGoldLayer.jpg" width="750" height="550">

*   **Rename Tables:**
    *   Modified the DLT code to **rename a materialized view** (`order_customer_silver_view` to `customerOrders_silver`) by changing the `name` parameter in the `@dlt.table` decorator.
    *   Updated the downstream table (`orders_aggregated_gold`) to read from the new table name (`live.order_silver`).
    *   Reran the DLT pipeline.
    *   Verified in the Databricks Catalog that the old table was removed, and a new table with the updated name was created.
    *   **Insight:** Just like schema changes, renaming tables is handled automatically by DLT when the code is updated. DLT takes care of removing the old dataset and creating the new one, managing the transition seamlessly from the user's perspective.
      </br>
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/EaseOfChangeinSilverTableName.jpg" width="750" height="550">

*   **Explore DLT Internals:**
    *   Understood that DLT datasets (Streaming Tables, Materialized Views) are **abstractions** on top of internal tables managed by DLT.
    *   Located the **internal catalog** (`Databricks internal`) and schema (`dlt_materialization_schema`) where the underlying data tables are stored, tied to the Pipeline ID. This internal schema is typically hidden from developers.
    *   Examined the details of a streaming table (e.g., `orders_bronze`) and found the **table ID** which points to the exact storage location.
    *   Explored the storage location in the Azure portal and identified a **`_dlt_metadata` folder** containing **checkpoint data** for the streaming table.
    *   **Insight:** DLT uses an internal catalog to manage the physical storage of its datasets. Streaming tables leverage checkpointing, stored alongside the data, to efficiently track and process only the incremental changes.
      </br>
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/DLTPipelineInternals.jpg" width="750" height="550">

*   **Visualize Data Lineage:**
    *   Explored **data lineage** powered by **Unity Catalog** for the DLT pipeline output tables.
    *   Viewed the lineage graph, showing the flow of data from the raw source tables (`customer_raw`, `orders_raw`) through intermediate steps (`customer_bronze`, `order_silver`) to the final aggregated table (`orders_aggregated_gold`).
    *   Demonstrated tracing **column-level lineage** (e.g., tracing `count_orders` back to `order_key`).
    *   Noted that lineage is a Unity Catalog feature and is available for standard tables as well, not just DLT outputs.
    *   **Insight:** Data lineage provides crucial visibility into the data flow, helping understand dependencies, troubleshoot issues, and manage data governance. Unity Catalog makes this feature broadly available across the data platform.

      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/UnityCatalogLineage.jpg" width="750" height="550">

###   3: DLT Append Flow & Autoloader

This section shows how to integrate external file ingestion using Autoloader into a DLT pipeline and how to dynamically create tables based on pipeline parameters.

**Steps:**

*   **Set up for Autoloader:**
    *   Used the setup notebook to **create a managed volume** (e.g., `autoloader`) under the DLT schema.
    *   Created folders within the volume for landing files (`files`) and for Autoloader's schema inference location (`autoloader_schemas`).
    *   **Insight:** Using managed volumes within Unity Catalog provides a governed location for landing external files for ingestion, integrating file-based sources into the governed Lakehouse environment.
      </br>
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/IncrementalLoadingUisngAutoloader.jpg" width="650" height="350">

*   **Read Data using Autoloader in DLT:**
    *   Added new code to the DLT notebook to **read data from files** using Autoloader.
    *   Defined a **Streaming Table** (`orders_autoloader_bronze`) using `@dlt.table` and `spark.readStream.format("cloudFiles")`.
    *   Configured Autoloader options: `cloudFiles.schemaHints` (specifying expected schema), `cloudFiles.schemaLocation` (location for schema inference files), `cloudFiles.format` (e.g., CSV) and `cloudFiles.schemaEvolutionMode` (`none` to prevent schema changes).
    *   Specified the **load path** pointing to the file landing location.
    *   Understood that DLT automatically manages Autoloader's **checkpoint location** at the streaming table's location, so it doesn't need to be explicitly configured.
    *   **Insight:** DLT seamlessly integrates with Autoloader for efficient, scalable ingestion of files from cloud storage. Autoloader's schema inference and evolution handling (when enabled) simplify file loading.
      </br>
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/AutoloaderForIngestingIncrementaLoad.jpg" width="950" height="350">

*   **Implement [Append Flow](https://docs.databricks.com/aws/en/dlt/flow-examples#example-use-append-flow-processing-instead-of-union) for Unioning:**
    *   Understood the need to **union data from multiple streaming sources** (Delta table and Autoloader) while maintaining incremental processing. A standard `union()` would reprocess all data every time.
    *   Used the **Append Flow** feature (`@dlt.append_flow`) to incrementally append data from multiple streaming sources into a single target streaming table.
    *   Created a **blank Streaming Table** (`orders_union_bronze`) using `dlt.create_streaming_table()` to serve as the target for the append flow.
    *   Defined separate functions using `@dlt.append_flow` to read incrementally from the Delta source (`live.orders_bronze`) and the Autoloader source (`live.orders_autoloader_bronze`) and append the data to the `orders_union_bronze` table.
    *   Modified the downstream join view to now read from the `orders_union_bronze` table (`live.orders_union_bronze`).
    *   **Insight:** Append Flow is a powerful DLT feature for combining data from multiple streaming sources incrementally into a single dataset, preserving the efficiency of streaming pipelines.
      </br>
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/AutoloaderForIngestingIncrementaLoad.jpg" width="950" height="450">

*   **Test Incremental File Ingestion:**
    *   Uploaded a test file to the Autoloader landing location.
    *   Ran the DLT pipeline.
    *   Observed that the Autoloader streaming table and the Union table initially processed data from both sources (full load for the new Union table).
    *   Uploaded another file to the landing location.
    *   Reran the DLT pipeline.
    *   Observed that the Autoloader streaming table only read the new records from the second file, and the Union streaming table only processed the incremental records coming from the Autoloader source, confirming incremental processing end-to-end.
    *   **Insight:** The combination of Autoloader and Append Flow within DLT provides a robust pattern for ingesting and combining incremental data from files and other streaming sources.
      </br>
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/IncrementalAutoloaderFile-1RunGraph(4newrecords).jpg" width="950" height="450">
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/IncrementalAutoloaderFileRunGraph.jpg" width="950" height="450">
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/AutoloaderTableWithIncrementalDataQuery.jpg" width="950" height="350">

*   **Pass Parameters into DLT Pipelines:**
    *   To dynamically create multiple gold tables based on the values of the OrderStatus column
    *   Accessed the pipeline **Settings** in the UI.
    *   Added a **Configuration** parameter (e.g., `custom.order_status`) with a value (e.g., `O,F`).
    *   **Insight:** Pipeline configurations provide a clean way to pass external parameters or settings into the DLT code, enabling dynamic behavior without hardcoding values.
    </br>
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/ConfigurationSettingsInPipelineForOrderStatus.jpg" width="950" height="550">

*   **Create Dynamic Tables based on Parameters:**
    *   Read the configuration parameter within the DLT code using `spark.conf.get()`.
    *   Split the parameter value (comma-separated list of order statuses).
    *   Used a **Python loop** to iterate through the values.
    *   Within the loop, used the `@dlt.table` decorator and **Python f-strings** to **dynamically create multiple gold tables** based on each status value (e.g., `orders_agg_o_gold`, `orders_agg_f_gold`).
    *   Added a `where` filter condition to each dynamically created table to select data matching the current status in the loop.
    *   Validated the code.
    *   Reran the DLT pipeline.
    *   Observed the dynamically created tables appearing in the pipeline graph and in the catalog.
    *   **Insight:** DLT allows you to build dynamic pipelines where the datasets created can be determined programmatically based on input parameters. This is incredibly powerful for building reusable data pipelines for different segments or configurations.
      </br>
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/ReadConfigFromPipelineSettings.jpg" width="550" height="105">
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/DynamicTablesUsingConfigurationSettingForOrderStatus.jpg" width="950" height="550">

###   4: [Change Data Capture (CDC) - SCD2 & SCD1](https://docs.databricks.com/aws/en/dlt/what-is-change-data-capture)

The Change Data Capture (CDC) capabilities in DLT using the [**`Apply_Changes`**](https://docs.databricks.com/aws/en/dlt/cdc) API to build Slowly Changing Dimension (SCD) Type 1 and Type 2 tables.

**Steps:**

*   **Understand Change Data Capture (CDC) and SCD:**
    *   Learned that CDC tracks changes (inserts, updates, deletes) in source data.
    *   Introduced **Slowly Changing Dimensions (SCD)**, specifically Type 1 (overwriting history) and Type 2 (maintaining history) for dimension tables.
    *   Understood that SCD Type 2 tables maintain a history of changes, typically using start and end dates/timestamps.
    *   Highlighted the difficulty of backloading out-of-order data into traditional SCD Type 2 implementations and how DLT simplifies this.

*   **Prepare Source Data for CDC:**
    *   Used the setup notebook to **add two new columns** to the source `customer_raw` table: `SourceAction` (indicating the action: Insert 'I', Delete 'D', Truncate 'T') and `SourceInsertDate` (timestamp of the action).
    *   Updated existing records in the source table with default values (e.g., `SourceAction='I'`, `SourceInsertDate = current_timestamp - 3 days`).
    *   **Insight:** Adding action and timestamp columns to the source is a common pattern for facilitating CDC, providing the necessary metadata for the target system (DLT) to process changes correctly.
   </br>
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/CDCSetupfortheRawCustomerTable.jpg" width="950" height="550">
   <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/RawCustomerDataWithNewColumnsForCDC.jpg" width="900" height="450">


*   **Modify DLT Code for SCD using `apply_changes`:**
    *   Modified the reading of the `customer_raw` source to be a **streaming view** (`customer_bronze_view`) using `@dlt.view` and `readStream`. This streaming view serves as the input for the SCD processing.
    *   **Created an SCD Type 1 table** (`customer_scd1_bronze`) using `dlt.create_streaming_table()`.
    *   Implemented the SCD Type 1 logic using the **`@dlt.apply_changes`** decorator. Specified the `target` (the SCD1 table), `source` (the streaming view using `live`), `keys` (`c_custkey`). `stored_as_scd_type=1` is the default. Included optional clauses for `apply_as_deletes` (when `SourceAction='D'`) and `apply_as_truncates` (when `SourceAction='T'`), using the `exp` function for expressions. Specified `sequence_by=SourceInsertDate` to order changes.
    *   **Created an SCD Type 2 table** (`customer_scd2_bronze`) using `dlt.create_streaming_table()`.
    *   Implemented the SCD Type 2 logic using `@dlt.apply_changes`. Specified the `target`, `source`, `keys`, and `stored_as_scd_type=2`. Used `except_column_list` to prevent `SourceAction` and `SourceInsertDate` from being included in the final SCD2 table columns. The `sequence_by` column (`SourceInsertDate`) is used by DLT to manage the `start_at` and `end_at` columns that track history.
    *   **Insight:** The `apply_changes` API is the cornerstone for CDC in DLT. It provides a declarative way to define how changes from a source stream should be applied to a target table to maintain SCD types, handling complex logic internally.
 
               | Requirement                   | Why It’s Needed                       |
               | ----------------------------- | ------------------------------------- |
               | Target is streaming           | `apply_changes` writes incrementally  |
               | Source is streaming/triggered | Needed for continuous ingestion       |
               | `sequence_by` is provided     | To resolve latest version of a key    |
               | `keys` are defined            | To match records (like primary key)   |
               | (Optional) `_dlt_change_type` | To handle deletes/truncates if needed |
        
     <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/DLTSCD1Apply_Changes.jpg" width="750" height="450">
     
     <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/SCD1%26SCD2TablesForCDC.jpg" width="900" height="400">
     <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/DLTSCD2Apply_Changes.jpg" width="900" height="350">
   

*   **Update Downstream Pipeline:**
    *   Modified the join view to read from the newly created `customer_scd2_bronze` table (`live.customer_scd2_bronze`) instead of the original `customer_bronze`.
    *   Added a **filter condition** (`end_at is null`) when reading the SCD Type 2 table for joining, to ensure only the currently active records are included in downstream processing.
    *   **Insight:** When using SCD Type 2 tables in downstream pipelines, it's typically necessary to filter for the active record to avoid duplicating data or incorrect aggregations.
      </br>
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/UpdateDownstreamViewToUseSCD2Table.jpg" width="900" height="300">

*   **Configure Pipeline for CDC:**
    *   Updated the pipeline's **Product Edition** in Settings to **Pro** (or Advanced, which includes Pro features), as CDC capabilities are available in the Pro edition and higher.
    *   **Insight:** Specific DLT features like CDC are tier-dependent. Selecting the appropriate product edition is necessary to enable these features.

*   **Test Initial Load and Incremental CDC:**
    *   Ran the DLT pipeline for the initial load. Observed the SCD Type 1 and Type 2 tables created and populated. Examined the SCD2 table columns (`start_at`, `end_at`) and confirmed `end_at` was null for initial records.
    *   Inserted a new record with a change for an existing customer key into the source `customer_raw` table, setting `SourceAction='I'` and current timestamp.
    *   Reran the pipeline (or used the "Refresh Table" feature on the SCD tables for quicker testing).
    *   Observed that the SCD Type 1 table was updated with the latest record for the modified key.
    *   Observed that the SCD Type 2 table inserted the new record with `start_at` as the current timestamp and `end_at` as null, while updating the previous record for the same key by populating its `end_at` with the new record's `start_at`. This demonstrated automatic history tracking.
      </br>
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/InsertTestCommentsCDCDataForCustomer.jpg" width="1000" height="250">
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/1RecordUpsertedForCDCChangeinSCD1.jpg" width="900" height="450">
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/QueriesForCDCForSCDTables.jpg" width="900" height="650">

*   **Test Backloading with SCD Type 2:**
    *   Inserted a record with a change for an existing customer key into the source `customer_raw` table, setting `SourceAction='I'` but providing a **timestamp from the past** (out of order).
    *   Reran the pipeline, specifically refreshing only the SCD tables.
    *   Confirmed that the SCD Type 1 table was **unaffected** (as it only keeps the latest record).
    *   Observed that the SCD Type 2 table correctly inserted the historical record in the middle of the existing history, automatically adjusting the `end_at` and `start_at` timestamps of the surrounding records to maintain accurate history.
    *   **Insight:** This demonstrates one of DLT's significant advantages: it handles out-of-order data ingestion for SCD Type 2 tables gracefully using the `sequence_by` column, a task that is notoriously complex in traditional ETL.

    </br>
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/InsertRecordForBackloadingForSCD2.jpg" width="900" height="250">
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/SelectRefreshSCDTablesforBackLoadingData.jpg" width="900" height="650">
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/QueriesAfterBackLoadingDataFOrSCDTables.jpg" width="900" height="650">
    
*   **Test Delete and Truncate Actions:**
    *   Inserted a record for an existing customer key into the source `customer_raw` table, setting `SourceAction='D'`.
    *   Reran the pipeline, refreshing only the SCD tables.
    *   Observed that the record for that key was **deleted** from the SCD Type 1 table (as `apply_as_deletes` was configured).
    *   Observed that the SCD Type 2 table was **unaffected** (as `apply_as_deletes` was *not* configured for SCD2 to maintain history).
    *   Inserted a record (key doesn't matter) into the source `customer_raw` table, setting `SourceAction='T'`.
    *   Reran the pipeline, refreshing only the SCD tables.
    *   Observed that the SCD Type 1 table was entirely **truncated** (as `apply_as_truncates` was configured).
    *   Observed that the SCD Type 2 table was **unaffected** (as `apply_as_truncates` was *not* configured for SCD2).
    *   **Insight:** The `apply_changes` API allows granular control over how delete and truncate actions in the source affect the target SCD tables, enabling different behaviors depending on whether you need to delete records (SCD1) or preserve history (SCD2).

      </br>
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/InsertRecordToDeleteCustomerForSCD1.jpg" width="900" height="250">
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/GraphDeleteDataForSCDTables.jpg" width="900" height="350">
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/QueriesAfterDeletingDataFOrSCDTables.jpg" width="900" height="550">
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/InsertNewRowFOrTruncatingDatainSCDTablesjpg.jpg" width="900" height="350">
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/GraphTruncateDataForSCDTables.jpg" width="900" height="500">

###   5: DLT Data Quality & Expectations

The focus on managing data quality within DLT pipelines using [**Expectations**](https://docs.databricks.com/aws/en/dlt/expectations), defining rules and actions for handling invalid data.

**Steps:**

*   **Understand Data Quality with Expectations:**
    *   Learned that DLT uses **Expectations** to define and enforce data quality rules.
    *   Expectations are optional clauses applied to DLT datasets (Tables or Views).
    *   Introduced the three types of actions when an expectation fails: **Warning** (default, logs failures but processes data), **Drop** (discards failing records), and **Fail** (stops the pipeline).

*   **Define Data Quality Rules:**
    *   Defined data quality rules using **Python dictionaries**, mapping a unique rule name to a Boolean expression (e.g., column is not null, column value is within a list, column value is greater than zero).
    *   Created dictionaries for rules related to orders (`order_rules`) and customers (`customer_rules`).
    *   **Insight:** Defining rules separately in a dictionary makes the code cleaner and rules reusable across multiple expectations.

*   **Apply Expectations to DLT Datasets:**
    *   Applied expectations to the DLT code using the `@dlt.expect` (for a single rule) or `@dlt.expect_all` (for multiple rules from a dictionary) decorator above the function defining the dataset.
    *   Applied rules to both a Streaming Table (`orders_bronze`) and a Streaming View (`customer_bronze_view`).
    *   **Insight:** Expectations can be applied at different stages of the pipeline (raw ingestion, intermediate transformations), allowing flexibility in enforcing data quality where needed.

*   **Configure Pipeline for Data Quality:**
    *   Updated the pipeline's **Product Edition** in Settings to **Advanced**, as data quality features like Expectations are available in the Advanced edition.
    *   **Insight:** Enabling the Advanced product edition unlocks the full suite of DLT data quality features.
    </br>
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/SetupExpectDataQulaityRules%26ApplyToOrders%26CustomerData.jpg" width="900" height="650">
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/ChangePipelineSettingToAdvancedFOrExpectTesting.jpg" width="900" height="650">
*   **Test Warning Mode:**
    *   Inserted records into the source tables that violated the defined data quality rules (e.g., invalid order status, negative order price, null market segment).
    *   Ensured the expectation action was set to **Warning** (default behavior when no action keyword is specified).
    *   Ran the DLT pipeline. Handled potential failures during initialization due to incorrect rule expressions by checking the Event Log.
    *   After the pipeline completed, checked the **Data Quality tab** for the datasets with expectations applied. Observed metrics showing the number of records that failed each rule.
    *   Confirmed the **Action** displayed as "allow" and verified that the violating records were **not dropped** but were processed downstream.
    *   **Insight:** Warning mode is useful for monitoring data quality issues without interrupting the pipeline. It provides visibility into rule violations via the UI metrics.
    </br>
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/InsertExpectDataQulaityRules%26ApplyToOrders%26CustomerData.jpg" width="900" height="650">
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/QualityCheckGrapghForOrder_rawTable.jpg" width="950" height="450">
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/GraphForCustomerRawQualityCheck.jpg"  width="950" height="450">

*   **Test Fail Mode:**
    *   Modified the expectation decorator to specify the **`or fail`** action keyword (e.g., `@dlt.expect_all(...) or fail`).
    *   Inserted records violating the rules again.
    *   Ran the DLT pipeline.
    *   Observed that the pipeline **failed** at the step where the expectation was defined and violated.
    *   Examined the Event Log, which explicitly stated the failure was due to an expectation check and often showed the violating record.
    *   **Insight:** Fail mode is critical for enforcing strict data quality requirements. If incoming data doesn't meet defined standards, the pipeline stops, preventing bad data from propagating downstream.
      </br>
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/ExpectQualityForOrders-Fail.jpg" width="950" height="350">
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/QualityCheckGrapghForOrder_rawTable-Fail.jpg" width="900" height="750">
   
*   **Test Drop Mode:**
    *   Modified the expectation decorator to specify the **`or drop`** action keyword (e.g., `@dlt.expect_all(...) or drop`).
    *   Inserted records violating the rules again.
    *   Ran the DLT pipeline.
    *   Observed that the pipeline **completed successfully**.
    *   Checked the Data Quality tab, observed the **Action** displayed as "drop" and confirmed the number of records dropped.
    *   Verified that the violating records were **not included** in the downstream tables.
    *   **Insight:** Drop mode allows the pipeline to continue running while automatically discarding records that fail data quality checks. This is useful when some data loss is acceptable to maintain the quality of the overall dataset.
      </br>
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/ExpectQualityForOrder-Drop.jpg" width="950" height="350">
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/GraphForOrderRawQualityCheck-Drop.jpg" width="900" height="450">
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/QueryCheckFOrOrderRawTable-Drop.jpg" width="900" height="350">
   
*   **Apply Multiple Expectations:**
    *   Demonstrated applying **multiple `@dlt.expect_all` decorators** with different sets of rules and different actions (e.g., one set with `or warning`, another with `or drop`) to a single dataset (e.g., the join view).
    *   Inserted data violating rules from both sets.
    *   Ran the pipeline.
    *   Observed in the Data Quality tab how DLT tracks failures and actions for each distinct set of expectations applied to the dataset.
    *   **Insight:** You can apply multiple layers of data quality checks with varying severity (warning, drop, fail) to the same dataset within DLT.
      </br>
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/QualityCheckForViewWithMultipleRules.jpg" width="950" height="350">
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/GraphForViewQualityCheck-Drop%26Warn.jpg" width=950" height="350">
      <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/QueryForViewQualityCheck.jpg" width="750" height="350">

*   **Monitor DLT Pipelines using SQL:**
    *   Learned that DLT provides a system function `event_log('<pipeline_id>')` to query the pipeline's event log directly using SQL.
    *   Executed SQL queries against the `event_log` function to retrieve raw log data.
    *   Used provided example queries to create SQL views (e.g., `event_log_raw`, `latest_updates`) based on the event log for easier querying.
    *   Queried the event log views to specifically retrieve data quality metrics (passing/failing records, expectation type) across the pipeline.
    *   Noted that these SQL queries can be used to build dashboards for monitoring pipeline health and data quality over time.
    *   **Insight:** The `event_log` provides a powerful interface for observing and monitoring DLT pipeline execution and data quality results programmatically, enabling integration with monitoring tools or creating custom dashboards.
      </br>
       <img src="https://github.com/ShreevaniRao/Azure/blob/main/Databricks/DLT/Assets/DBDatQualityPipelineMonitoringQuery.jpg" width="900" height="750">

###  6. Outro 
Though construction of a Delta Live Tables (DLT) pipeline in Databricks, demonstrates rich and powerful capabilities such as incremental data processing via Autoloader and the append flow, Change Data Capture (SCD type 1 & 2) using the apply_changes API, data quality enforcement with expectations, and dynamic table generation, but also has few limitations as mentioned in the documentation [**link**](https://learn.microsoft.com/en-us/azure/databricks/dlt/limitations).
