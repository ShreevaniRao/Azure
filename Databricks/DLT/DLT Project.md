## Pipeline Construction Steps

This project follows the progression shown in the below provided steps, to build the DLT pipeline, along with insights gained at each stage.

### Introduction to Delta Live Tables (DLT)

This DLT pipeline as a declarative framework in Databricks designed to simplify ETL pipelines by handling orchestration, cluster management, data quality, and error handling. It requires the **Premium plan** on Databricks.

**Steps:**

*   **Set up the Environment:**
    *   Created a new folder for DLT pipelines within the workspace.
    *   Used a setup notebook to **create a new schema** (e.g., `etl` under the `dlt-catalog` catalog) for the DLT run.
    *   **Deep cloned sample data** (e.g., `orders` and `customer` from `samples.tpch`) into raw tables (e.g., `etl.bronze.orders_raw`, `etl.bronze.customer_raw`) to use as source data.
    *   **Insight:** Setting up a dedicated schema and cloning data provides a clean, repeatable starting point for the pipeline development. Using `deep clone` creates independent copies of the source data.

    *(Insert Screenshot: Creating Schema and Cloning Data)*

*   **Understand DLT Dataset Types:**
    *   Learned about the three main types of datasets in DLT: **Streaming Tables**, **Materialized Views**, and **Views** [2].
    *   **Streaming Tables** are used for streaming sources and processing incremental data, allowing data to be appended [2].
    *   **Materialized Views** are generally used for transformations, aggregations, or computations [2].
    *   **Views** are typically used for intermediate transformations and are **not stored** at the target schema [2, 3].
    *   Understood that DLT pipelines are powered by **Delta Lake**, inheriting its capabilities [2].
    *   **Insight:** Choosing the right dataset type is crucial for defining how data is processed and stored. Streaming tables are key for efficiency with ever-growing data.

*   **Write the Initial DLT Code:**
    *   Noted that DLT code can be written in **Python or SQL** and requires a special **job compute** type, not the standard all-purpose compute [2, 4].
    *   Imported the necessary **`dlt` Python module** [4].
    *   **Created a Streaming Table** (`orders_bronze`) for the `orders_raw` source using the `@dlt.table` decorator and `spark.readStream.table()` to read the Delta table as a streaming source [4, 5]. Added optional table properties like `quality` and a comment [4].
    *   **Created a Materialized View** (`customer_bronze`) for the `customer_raw` source using the `@dlt.table` decorator and `spark.read.table()` to read the Delta table as a batch source [5, 6]. Used the `name` parameter to explicitly set the table name [5].
    *   **Insight:** The `@dlt.table` and `@dlt.view` decorators, along with the `dlt` module, are the core building blocks for defining datasets and transformations in DLT. The key difference between streaming tables and materialized views often lies in how their source is read (`readStream` vs `read`) [6].

    *(Insert Screenshot: Creating orders_bronze Streaming Table)*
    *(Insert Screenshot: Creating customer_bronze Materialized View)*

*   **Define Intermediate and Final Transformations:**
    *   **Created a View** (`join_view`) to join the `orders_bronze` streaming table and `customer_bronze` materialized view [6, 7]. Used the `@dlt.view` decorator and read the datasets using the **`live` keyword** (`live.customer_bronze`, `live.orders_bronze`) to reference datasets within the same pipeline [6].
    *   **Created a Silver Materialized View** (`joined_silver`) by reading the `join_view` and adding a new column (`insert_date`) with the current timestamp [7]. Changed the `quality` property to `silver` [7].
    *   **Created a Gold Materialized View** (`orders_aggregated_gold`) by reading the `joined_silver` table, performing aggregations (e.g., `count(order_key)`) grouped by `market_segment`, and adding an `insert_date` column [7, 8]. Set the `quality` property to `gold` [8].
    *   **Insight:** Views are useful for breaking down complex transformations into logical steps without persisting intermediate results. Reading datasets within the same pipeline using `live` is essential for chaining transformations. Aggregations typically produce materialized views.

    *(Insert Screenshot: Creating join_view)*
    *(Insert Screenshot: Creating joined_silver Materialized View)*
    *(Insert Screenshot: Creating orders_aggregated_gold Materialized View)*

*   **Create and Configure the DLT Pipeline:**
    *   Created a new DLT pipeline via the Databricks UI (New -> DLT pipelines or ETL pipelines) [8].
    *   Configured pipeline settings: **Name**, **Product Edition** (starting with Core) [8, 9], **Pipeline Mode** (Triggered or Continuous - started with Triggered) [9], selected the notebook path [9], specified **Unity Catalog** settings (Catalog and Schema) [9], and configured compute (number of workers, driver type) [9].
    *   **Insight:** The product edition dictates available features (Core: basic ETL; Pro: CDC; Advanced: Data Quality) [8, 9]. Triggered mode is suitable for scheduled batch runs, while Continuous is for low-latency streaming [9]. Integrating with Unity Catalog ensures data governance [9].

    *(Insert Screenshot: DLT Pipeline Creation UI)*
    *(Insert Screenshot: Pipeline Settings - Product Edition, Mode, Catalog, Schema)*

*   **Run and Debug the Pipeline:**
    *   Started the pipeline run using the UI [10].
    *   Observed pipeline status (Initializing, Setting up tables, Running, Completed/Failed) [10].
    *   Used the **Development mode** for easy debugging, as the cluster remains running even if the pipeline fails [10]. Production mode terminates the cluster on success or failure to save costs [10].
    *   Identified and fixed errors by examining the **Event Log** (e.g., unimported functions like `count`, incorrect column names) [10, 11].
    *   Reran the pipeline after correcting code [11].
    *   **Insight:** Development mode is invaluable during the initial build and debugging phase. The Event Log provides detailed information about pipeline execution and failures, making troubleshooting efficient [10, 11].

    *(Insert Screenshot: Pipeline Run Status UI)*
    *(Insert Screenshot: Event Log showing Error)*
    *(Insert Screenshot: Correcting Code based on Error)*
    *(Insert Screenshot: Successful Pipeline Run and DAG Visualization)*

*   **Verify Pipeline Output:**
    *   Examined the Databricks Catalog to see the created datasets [3]. Confirmed that Streaming Tables and Materialized Views were created, while Views were not persisted [3].
    *   Queried the final gold table (`orders_aggregated_gold`) to verify the aggregated data [3].
    *   Terminated the DLT cluster after successful development runs to manage costs [3].
    *   **Insight:** DLT automatically manages the creation and storage of specified tables and materialized views based on the defined code. Views are temporary constructs used only during the pipeline run [3].

    *(Insert Screenshot: Datasets in Catalog after Run)*
    *(Insert Screenshot: Querying the Final Gold Table)*

###   2: DLT Internals & Incremental Load

This   dives deeper into DLT's internal workings, focusing on how it handles incremental data and dataset management, and introduces features for modifying/renaming tables and data lineage.

**Steps:**

*   **Understand Dataset Management:**
    *   Learned that DLT manages all datasets (Streaming Tables, Materialized Views, Views) created within a pipeline and ties them to a specific **Pipeline ID** [12, 13].
    *   Deleting a DLT pipeline **deletes all associated datasets** [12].
    *   **Insight:** This integrated management simplifies data lifecycle handling for pipeline-generated data, ensuring consistency between the pipeline definition and its output.

*   **Process Incremental Data:**
    *   Inserted new records into the source `orders_raw` table (the source for the `orders_bronze` streaming table) [14].
    *   Reran the DLT pipeline (in Triggered mode) [14].
    *   Observed that the `orders_bronze` streaming table **only read the newly inserted incremental records** (e.g., 10k records) during the run, demonstrating efficient incremental processing [14].
    *   Confirmed the final aggregated gold table reflected the new data, with increased counts [14].
    *   **Insight:** Streaming tables in DLT are designed for incremental processing. When their source is updated, they only process the new changes on subsequent runs, which is crucial for performance and cost-effectiveness with large datasets [14].

    *(Insert Screenshot: Inserting Incremental Data into Source)*
    *(Insert Screenshot: Pipeline Run showing Incremental Read on Streaming Table)*
    *(Insert Screenshot: Final Gold Table reflecting Increased Counts)*

*   **Modify and Add Columns:**
    *   Modified the DLT code to **add a new aggregated column** (`sum_of_total_price`) and **rename an existing column** (`count_orders`) in the `orders_aggregated_gold` materialized view [15].
    *   Validated the code changes within the notebook while connected to the DLT pipeline in development mode [15]. (Corrected errors like unimported functions or incorrect column names during validation) [15, 16].
    *   Reran the DLT pipeline [16].
    *   Verified that the final gold table now contained the renamed and newly added columns [16].
    *   **Insight:** DLT's declarative nature simplifies schema changes. You just update the desired schema/transformation in the code, and DLT handles the underlying table updates and schema evolution automatically [15, 16].

    *(Insert Screenshot: Modifying Code to Add/Rename Columns)*
    *(Insert Screenshot: Validating DLT Code in Notebook)*
    *(Insert Screenshot: Final Gold Table with New/Renamed Columns)*

*   **Rename Tables:**
    *   Modified the DLT code to **rename a materialized view** (`joined_silver` to `order_silver`) by changing the `name` parameter in the `@dlt.table` decorator [16].
    *   Updated the downstream table (`orders_aggregated_gold`) to read from the new table name (`live.order_silver`) [16].
    *   Reran the DLT pipeline [13, 16].
    *   Verified in the Databricks Catalog that the old table was removed, and a new table with the updated name was created [13].
    *   **Insight:** Just like schema changes, renaming tables is handled automatically by DLT when the code is updated. DLT takes care of removing the old dataset and creating the new one, managing the transition seamlessly from the user's perspective [13, 16].

    *(Insert Screenshot: Renaming Table in Code)*
    *(Insert Screenshot: Catalog showing Old Table Gone, New Table Created)*

*   **Explore DLT Internals:**
    *   Understood that DLT datasets (Streaming Tables, Materialized Views) are **abstractions** on top of internal tables managed by DLT [13].
    *   Located the **internal catalog** (`Databricks internal`) and schema (`dlt_materialization_schema`) where the underlying data tables are stored, tied to the Pipeline ID [13, 17]. This internal schema is typically hidden from developers [17].
    *   Examined the details of a streaming table (e.g., `orders_bronze`) and found the **table ID** which points to the exact storage location [17].
    *   Explored the storage location in the Azure portal and identified a **`_dlt_metadata` folder** containing **checkpoint data** for the streaming table [17].
    *   **Insight:** DLT uses an internal catalog to manage the physical storage of its datasets. Streaming tables leverage checkpointing, stored alongside the data, to efficiently track and process only the incremental changes [17].

    *(Insert Screenshot: Databricks internal Catalog)*
    *(Insert Screenshot: Streaming Table Details showing Table ID)*
    *(Insert Screenshot: Storage Location showing _dlt_metadata and checkpoint)*

*   **Visualize Data Lineage:**
    *   Explored **data lineage** powered by **Unity Catalog** for the DLT pipeline output tables [17].
    *   Viewed the lineage graph, showing the flow of data from the raw source tables (`customer_raw`, `orders_raw`) through intermediate steps (`customer_bronze`, `order_silver`) to the final aggregated table (`orders_aggregated_gold`) [17, 18].
    *   Demonstrated tracing **column-level lineage** (e.g., tracing `count_orders` back to `order_key`) [18].
    *   Noted that lineage is a Unity Catalog feature and is available for standard tables as well, not just DLT outputs [18].
    *   **Insight:** Data lineage provides crucial visibility into the data flow, helping understand dependencies, troubleshoot issues, and manage data governance. Unity Catalog makes this feature broadly available across the data platform [17, 18].

    *(Insert Screenshot: Data Lineage Graph)*
    *(Insert Screenshot: Column Lineage)*

###   3: DLT Append Flow & Autoloader

This   shows how to integrate external file ingestion using Autoloader into a DLT pipeline and how to dynamically create tables based on pipeline parameters.

**Steps:**

*   **Set up for Autoloader:**
    *   Used the setup notebook to **create a managed volume** (e.g., `landing`) under the DLT schema [19].
    *   Created folders within the volume for landing files (`files`) and for Autoloader's schema inference location (`autoloader_schemas`) [19].
    *   **Insight:** Using managed volumes within Unity Catalog provides a governed location for landing external files for ingestion, integrating file-based sources into the governed Lakehouse environment [19].

    *(Insert Screenshot: Creating Managed Volume and Folders)*
    *(Insert Screenshot: Managed Volume and Folders in Catalog)*

*   **Read Data using Autoloader in DLT:**
    *   Added new code to the DLT notebook to **read data from files** using Autoloader [20].
    *   Defined a **Streaming Table** (`orders_autoloader_bronze`) using `@dlt.table` and `spark.readStream.format("cloudFiles")` [20].
    *   Configured Autoloader options: `cloudFiles.schemaHints` (specifying expected schema), `cloudFiles.schemaLocation` (location for schema inference files), `cloudFiles.format` (e.g., CSV), `pathGlobFilter` (e.g., *.csv), and `cloudFiles.schemaEvolutionMode` (`none` to prevent schema changes) [20, 21].
    *   Specified the **load path** pointing to the file landing location [21].
    *   Understood that DLT automatically manages Autoloader's **checkpoint location** at the streaming table's location, so it doesn't need to be explicitly configured [21].
    *   **Insight:** DLT seamlessly integrates with Autoloader for efficient, scalable ingestion of files from cloud storage. Autoloader's schema inference and evolution handling (when enabled) simplify file loading.

    *(Insert Screenshot: DLT Code for Autoloader Streaming Table)*

*   **Implement Append Flow for Unioning:**
    *   Understood the need to **union data from multiple streaming sources** (Delta table and Autoloader) while maintaining incremental processing [22]. A standard `union()` would reprocess all data every time [22].
    *   Used the **Append Flow** feature (`@dlt.append_flow`) to incrementally append data from multiple streaming sources into a single target streaming table [22].
    *   Created a **blank Streaming Table** (`orders_union_bronze`) using `dlt.create_streaming_table()` to serve as the target for the append flow [22].
    *   Defined separate functions using `@dlt.append_flow` to read incrementally from the Delta source (`live.orders_bronze`) and the Autoloader source (`live.orders_autoloader_bronze`) and append the data to the `orders_union_bronze` table [22, 23].
    *   Modified the downstream join view to now read from the `orders_union_bronze` table (`live.orders_union_bronze`) [23].
    *   **Insight:** Append Flow is a powerful DLT feature for combining data from multiple streaming sources incrementally into a single dataset, preserving the efficiency of streaming pipelines [22].

    *(Insert Screenshot: Creating Target Streaming Table for Union)*
    *(Insert Screenshot: DLT Code for Append Flow from Delta Source)*
    *(Insert Screenshot: DLT Code for Append Flow from Autoloader Source)*
    *(Insert Screenshot: Modifying Join View to Read from Union Table)*

*   **Test Incremental File Ingestion:**
    *   Uploaded a test file to the Autoloader landing location [23].
    *   Ran the DLT pipeline [24].
    *   Observed that the Autoloader streaming table and the Union table initially processed data from both sources (full load for the new Union table) [24].
    *   Uploaded another file to the landing location [24].
    *   Reran the DLT pipeline [24, 25].
    *   Observed that the Autoloader streaming table only read the new records from the second file, and the Union streaming table only processed the incremental records coming from the Autoloader source, confirming incremental processing end-to-end [25].
    *   **Insight:** The combination of Autoloader and Append Flow within DLT provides a robust pattern for ingesting and combining incremental data from files and other streaming sources [25].

    *(Insert Screenshot: Uploading File to Landing Zone)*
    *(Insert Screenshot: Pipeline Run showing Incremental Read from Autoloader and Union)*

*   **Pass Parameters into DLT Pipelines:**
    *   Accessed the pipeline **Settings** in the UI [25].
    *   Added a **Configuration** parameter (e.g., `custom.order_status`) with a value (e.g., `O,F`) [25].
    *   **Insight:** Pipeline configurations provide a clean way to pass external parameters or settings into the DLT code, enabling dynamic behavior without hardcoding values [25].

    *(Insert Screenshot: Adding Configuration in Pipeline Settings)*

*   **Create Dynamic Tables based on Parameters:**
    *   Read the configuration parameter within the DLT code using `spark.conf.get()` [25, 26].
    *   Split the parameter value (comma-separated list of order statuses) [26].
    *   Used a **Python loop** to iterate through the values [26].
    *   Within the loop, used the `@dlt.table` decorator and **Python f-strings** to **dynamically create multiple gold tables** based on each status value (e.g., `orders_agg_o_gold`, `orders_agg_f_gold`) [26].
    *   Added a `where` filter condition to each dynamically created table to select data matching the current status in the loop [26].
    *   Validated the code [26].
    *   Reran the DLT pipeline [27].
    *   Observed the dynamically created tables appearing in the pipeline graph and in the catalog [27].
    *   **Insight:** DLT allows you to build dynamic pipelines where the datasets created can be determined programmatically based on input parameters. This is incredibly powerful for building reusable data pipelines for different segments or configurations [26, 27].

    *(Insert Screenshot: Reading Configuration in DLT Code)*
    *(Insert Screenshot: DLT Code for Dynamic Table Creation Loop)*
    *(Insert Screenshot: Pipeline Graph showing Dynamically Created Tables)*
    *(Insert Screenshot: Catalog showing Dynamically Created Tables)*

###   4: DLT SCD2 & SCD1

This   introduces Change Data Capture (CDC) capabilities in DLT using the `apply_changes` API to build Slowly Changing Dimension (SCD) Type 1 and Type 2 tables.

**Steps:**

*   **Understand Change Data Capture (CDC) and SCD:**
    *   Learned that CDC tracks changes (inserts, updates, deletes) in source data [28].
    *   Introduced **Slowly Changing Dimensions (SCD)**, specifically Type 1 (overwriting history) and Type 2 (maintaining history) [28].
    *   Understood that SCD Type 2 tables maintain a history of changes, typically using start and end dates/timestamps [28, 29].
    *   Highlighted the difficulty of backloading out-of-order data into traditional SCD Type 2 implementations and how DLT simplifies this [28].

*   **Prepare Source Data for CDC:**
    *   Used the setup notebook to **add two new columns** to the source `customer_raw` table: `SourceAction` (indicating the action: Insert 'I', Delete 'D', Truncate 'T') and `SourceInsertDate` (timestamp of the action) [30].
    *   Updated existing records in the source table with default values (e.g., `SourceAction='I'`, `SourceInsertDate = current_timestamp - 3 days`) [30].
    *   **Insight:** Adding action and timestamp columns to the source is a common pattern for facilitating CDC, providing the necessary metadata for the target system (DLT) to process changes correctly [30].

    *(Insert Screenshot: Adding SourceAction/SourceInsertDate to Raw Table)*
    *(Insert Screenshot: Updating Raw Table with Default Values)*
    *(Insert Screenshot: Querying Raw Table showing New Columns)*

*   **Modify DLT Code for SCD using `apply_changes`:**
    *   Modified the reading of the `customer_raw` source to be a **streaming view** (`customer_bronze_view`) using `@dlt.view` and `readStream` [30, 31]. This streaming view serves as the input for the SCD processing [31].
    *   **Created an SCD Type 1 table** (`customer_scd1_bronze`) using `dlt.create_streaming_table()` [31].
    *   Implemented the SCD Type 1 logic using the **`@dlt.apply_changes`** decorator [31]. Specified the `target` (the SCD1 table), `source` (the streaming view using `live`), `keys` (`c_custkey`) [31]. `stored_as_scd_type=1` is the default [31]. Included optional clauses for `apply_as_deletes` (when `SourceAction='D'`) and `apply_as_truncates` (when `SourceAction='T'`), using the `exp` function for expressions [31, 32]. Specified `sequence_by=SourceInsertDate` to order changes [32].
    *   **Created an SCD Type 2 table** (`customer_scd2_bronze`) using `dlt.create_streaming_table()` [32].
    *   Implemented the SCD Type 2 logic using `@dlt.apply_changes` [32]. Specified the `target`, `source`, `keys`, and `stored_as_scd_type=2` [32]. Used `except_column_list` to prevent `SourceAction` and `SourceInsertDate` from being included in the final SCD2 table columns [32]. The `sequence_by` column (`SourceInsertDate`) is used by DLT to manage the `start_at` and `end_at` columns that track history [29].
    *   **Insight:** The `apply_changes` API is the cornerstone for CDC in DLT. It provides a declarative way to define how changes from a source stream should be applied to a target table to maintain SCD types, handling complex logic internally [31, 32].

    *(Insert Screenshot: Streaming View for Customer Source)*
    *(Insert Screenshot: DLT Code for SCD Type 1 Table using apply_changes)*
    *(Insert Screenshot: DLT Code for SCD Type 2 Table using apply_changes)*

*   **Update Downstream Pipeline:**
    *   Modified the join view to read from the newly created `customer_scd2_bronze` table (`live.customer_scd2_bronze`) instead of the original `customer_bronze` [33].
    *   Added a **filter condition** (`end_at is null`) when reading the SCD Type 2 table for joining, to ensure only the currently active records are included in downstream processing [33].
    *   **Insight:** When using SCD Type 2 tables in downstream pipelines, it's typically necessary to filter for the active record to avoid duplicating data or incorrect aggregations [33].

    *(Insert Screenshot: Updating Join View to Read from SCD2)*
    *(Insert Screenshot: Adding Filter for Active Records)*

*   **Configure Pipeline for CDC:**
    *   Updated the pipeline's **Product Edition** in Settings to **Pro** (or Advanced, which includes Pro features), as CDC capabilities are available in the Pro edition and higher [33].
    *   **Insight:** Specific DLT features like CDC are tier-dependent. Selecting the appropriate product edition is necessary to enable these features [33].

    *(Insert Screenshot: Pipeline Settings - Product Edition set to Pro)*

*   **Test Initial Load and Incremental CDC:**
    *   Ran the DLT pipeline for the initial load [33]. Observed the SCD Type 1 and Type 2 tables created and populated [33]. Examined the SCD2 table columns (`start_at`, `end_at`) and confirmed `end_at` was null for initial records [29].
    *   Inserted a new record with a change for an existing customer key into the source `customer_raw` table, setting `SourceAction='I'` and current timestamp [29].
    *   Reran the pipeline (or used the "Refresh Table" feature on the SCD tables for quicker testing) [29, 34].
    *   Observed that the SCD Type 1 table was updated with the latest record for the modified key [34].
    *   Observed that the SCD Type 2 table inserted the new record with `start_at` as the current timestamp and `end_at` as null, while updating the previous record for the same key by populating its `end_at` with the new record's `start_at` [34]. This demonstrated automatic history tracking [34].

    *(Insert Screenshot: Querying SCD1 Table - Initial Load)*
    *(Insert Screenshot: Querying SCD2 Table - Initial Load)*
    *(Insert Screenshot: Inserting New/Changed Record into Raw Source)*
    *(Insert Screenshot: SCD1 Table after Incremental Update)*
    *(Insert Screenshot: SCD2 Table after Incremental Update showing History)*

*   **Test Backloading with SCD Type 2:**
    *   Inserted a record with a change for an existing customer key into the source `customer_raw` table, setting `SourceAction='I'` but providing a **timestamp from the past** (out of order) [34].
    *   Reran the pipeline, specifically refreshing only the SCD tables [34].
    *   Confirmed that the SCD Type 1 table was **unaffected** (as it only keeps the latest record) [35].
    *   Observed that the SCD Type 2 table correctly inserted the historical record in the middle of the existing history, automatically adjusting the `end_at` and `start_at` timestamps of the surrounding records to maintain accurate history [35].
    *   **Insight:** This demonstrates one of DLT's significant advantages: it handles out-of-order data ingestion for SCD Type 2 tables gracefully using the `sequence_by` column, a task that is notoriously complex in traditional ETL [35].

    *(Insert Screenshot: Inserting Historical (Backdated) Record into Raw Source)*
    *(Insert Screenshot: Refreshing Only SCD Tables in Pipeline UI)*
    *(Insert Screenshot: SCD2 Table showing Correctly Backloaded History)*

*   **Test Delete and Truncate Actions:**
    *   Inserted a record for an existing customer key into the source `customer_raw` table, setting `SourceAction='D'` [35, 36].
    *   Reran the pipeline, refreshing only the SCD tables [36].
    *   Observed that the record for that key was **deleted** from the SCD Type 1 table (as `apply_as_deletes` was configured) [36].
    *   Observed that the SCD Type 2 table was **unaffected** (as `apply_as_deletes` was *not* configured for SCD2 to maintain history) [36].
    *   Inserted a record (key doesn't matter) into the source `customer_raw` table, setting `SourceAction='T'` [37].
    *   Reran the pipeline, refreshing only the SCD tables [37].
    *   Observed that the SCD Type 1 table was entirely **truncated** (as `apply_as_truncates` was configured) [37].
    *   Observed that the SCD Type 2 table was **unaffected** (as `apply_as_truncates` was *not* configured for SCD2) [37].
    *   **Insight:** The `apply_changes` API allows granular control over how delete and truncate actions in the source affect the target SCD tables, enabling different behaviors depending on whether you need to delete records (SCD1) or preserve history (SCD2) [36, 37].

    *(Insert Screenshot: Inserting Delete Action Record)*
    *(Insert Screenshot: SCD1 Table after Delete Action)*
    *(Insert Screenshot: Inserting Truncate Action Record)*
    *(Insert Screenshot: SCD1 Table after Truncate Action)*

###   5: DLT Data Quality & Expectations

This   focuses on managing data quality within DLT pipelines using **Expectations**, defining rules and actions for handling invalid data.

**Steps:**

*   **Understand Data Quality with Expectations:**
    *   Learned that DLT uses **Expectations** to define and enforce data quality rules [38].
    *   Expectations are optional clauses applied to DLT datasets (Tables or Views) [38, 39].
    *   Introduced the three types of actions when an expectation fails: **Warning** (default, logs failures but processes data), **Drop** (discards failing records), and **Fail** (stops the pipeline) [38].

*   **Define Data Quality Rules:**
    *   Defined data quality rules using **Python dictionaries**, mapping a unique rule name to a Boolean expression (e.g., column is not null, column value is within a list, column value is greater than zero) [38, 40].
    *   Created dictionaries for rules related to orders (`order_rules`) and customers (`customer_rules`) [38, 40].
    *   **Insight:** Defining rules separately in a dictionary makes the code cleaner and rules reusable across multiple expectations [38, 40].

    *(Insert Screenshot: Defining Data Quality Rules in Python Dictionary)*

*   **Apply Expectations to DLT Datasets:**
    *   Applied expectations to the DLT code using the `@dlt.expect` (for a single rule) or `@dlt.expect_all` (for multiple rules from a dictionary) decorator above the function defining the dataset [40, 41].
    *   Applied rules to both a Streaming Table (`orders_bronze`) and a Streaming View (`customer_bronze_view`) [39].
    *   **Insight:** Expectations can be applied at different stages of the pipeline (raw ingestion, intermediate transformations), allowing flexibility in enforcing data quality where needed [39].

    *(Insert Screenshot: Applying Expectations to a DLT Table)*
    *(Insert Screenshot: Applying Expectations to a DLT View)*

*   **Configure Pipeline for Data Quality:**
    *   Updated the pipeline's **Product Edition** in Settings to **Advanced**, as data quality features like Expectations are available in the Advanced edition [39].
    *   **Insight:** Enabling the Advanced product edition unlocks the full suite of DLT data quality features [39].

    *(Insert Screenshot: Pipeline Settings - Product Edition set to Advanced)*

*   **Test Warning Mode:**
    *   Inserted records into the source tables that violated the defined data quality rules (e.g., invalid order status, negative order price, null market segment) [41].
    *   Ensured the expectation action was set to **Warning** (default behavior when no action keyword is specified) [41].
    *   Ran the DLT pipeline [39]. Handled potential failures during initialization due to incorrect rule expressions by checking the Event Log [39].
    *   After the pipeline completed, checked the **Data Quality tab** for the datasets with expectations applied [42]. Observed metrics showing the number of records that failed each rule [42].
    *   Confirmed the **Action** displayed as "allow" and verified that the violating records were **not dropped** but were processed downstream [42].
    *   **Insight:** Warning mode is useful for monitoring data quality issues without interrupting the pipeline. It provides visibility into rule violations via the UI metrics [42].

    *(Insert Screenshot: Inserting Data Violating Rules)*
    *(Insert Screenshot: Data Quality Tab showing Failed Records in Warning Mode)*
    *(Insert Screenshot: Verifying Violating Records Passed Downstream)*

*   **Test Fail Mode:**
    *   Modified the expectation decorator to specify the **`or fail`** action keyword (e.g., `@dlt.expect_all(...) or fail`) [42].
    *   Inserted records violating the rules again [42].
    *   Ran the DLT pipeline [43].
    *   Observed that the pipeline **failed** at the step where the expectation was defined and violated [43].
    *   Examined the Event Log, which explicitly stated the failure was due to an expectation check and often showed the violating record [43].
    *   **Insight:** Fail mode is critical for enforcing strict data quality requirements. If incoming data doesn't meet defined standards, the pipeline stops, preventing bad data from propagating downstream [43].

    *(Insert Screenshot: DLT Code with 'or fail' Action)*
    *(Insert Screenshot: Pipeline Failed due to Expectation)*
    *(Insert Screenshot: Event Log showing Expectation Failure Detail)*

*   **Test Drop Mode:**
    *   Modified the expectation decorator to specify the **`or drop`** action keyword (e.g., `@dlt.expect_all(...) or drop`) [43].
    *   Inserted records violating the rules again [43].
    *   Ran the DLT pipeline [43].
    *   Observed that the pipeline **completed successfully** [43].
    *   Checked the Data Quality tab, observed the **Action** displayed as "drop" and confirmed the number of records dropped [43].
    *   Verified that the violating records were **not included** in the downstream tables [43].
    *   **Insight:** Drop mode allows the pipeline to continue running while automatically discarding records that fail data quality checks. This is useful when some data loss is acceptable to maintain the quality of the overall dataset [43].

    *(Insert Screenshot: DLT Code with 'or drop' Action)*
    *(Insert Screenshot: Pipeline Completed in Drop Mode)*
    *(Insert Screenshot: Data Quality Tab showing Dropped Records)*
    *(Insert Screenshot: Verifying Violating Records were Dropped Downstream)*

*   **Apply Multiple Expectations:**
    *   Demonstrated applying **multiple `@dlt.expect_all` decorators** with different sets of rules and different actions (e.g., one set with `or warning`, another with `or drop`) to a single dataset (e.g., the join view) [44].
    *   Inserted data violating rules from both sets [44].
    *   Ran the pipeline [45].
    *   Observed in the Data Quality tab how DLT tracks failures and actions for each distinct set of expectations applied to the dataset [45].
    *   **Insight:** You can apply multiple layers of data quality checks with varying severity (warning, drop, fail) to the same dataset within DLT [45].

    *(Insert Screenshot: Applying Multiple Expectations to a Single Dataset)*
    *(Insert Screenshot: Data Quality Tab showing Metrics for Multiple Expectations)*

*   **Monitor DLT Pipelines using SQL:**
    *   Learned that DLT provides a system function `event_log('<pipeline_id>')` to query the pipeline's event log directly using SQL [45, 46].
    *   Executed SQL queries against the `event_log` function to retrieve raw log data [46].
    *   Used provided example queries to create SQL views (e.g., `event_log_raw`, `latest_updates`) based on the event log for easier querying [46].
    *   Queried the event log views to specifically retrieve data quality metrics (passing/failing records, expectation type) across the pipeline [46].
    *   Noted that these SQL queries can be used to build dashboards for monitoring pipeline health and data quality over time [47].
    *   **Insight:** The `event_log` provides a powerful interface for observing and monitoring DLT pipeline execution and data quality results programmatically, enabling integration with monitoring tools or creating custom dashboards [45-47].

    *(Insert Screenshot: Querying Event Log using SQL function)*
    *(Insert Screenshot: Querying Data Quality Metrics from Event Log View)*

