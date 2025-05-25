# Databricks notebook source
# MAGIC %md
# MAGIC #### Setup schema, ingest data, Incremental Loading, Autoloader, Append Flow, CDC and Lineage queries for DLT pipeline

# COMMAND ----------

# MAGIC %sql
# MAGIC -- create new schema in the catalog
# MAGIC create schema if not exists `dlt-catalog`.etl

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Deep Clone the tables to work with
# MAGIC create table if not exists `dlt-catalog`.etl.orders_raw deep clone samples.tpch.orders;
# MAGIC create table if not exists `dlt-catalog`.etl.customers_raw deep clone samples.tpch.customer;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Query orders data from the sample database
# MAGIC select * from `dlt-catalog`.etl.orders_raw;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Query customer data from the sample database
# MAGIC select * from `dlt-catalog`.etl.customer_raw 

# COMMAND ----------

# MAGIC %md
# MAGIC ### Incremental loading in the streaming table 

# COMMAND ----------

# MAGIC %sql
# MAGIC --- insert data in orders table
# MAGIC insert into `dlt-catalog`.etl.orders_raw
# MAGIC select * from samples.tpch.orders
# MAGIC limit 10000

# COMMAND ----------

# MAGIC
# MAGIC %sql
# MAGIC -- Check the gold table for the aggregate changes - new column added and renamed the existing column
# MAGIC select * from `dlt-catalog`.etl.orders_aggregated_gold

# COMMAND ----------

# MAGIC %md
# MAGIC ## Increment data loading using Autoloader

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create Volume to have a landing place for autoloader files
# MAGIC Create Volume if not exists `dlt-catalog`.etl.autoloader

# COMMAND ----------

# make a folder for dropping files for incremental loading
dbutils.fs.mkdirs("/Volumes/dlt-catalog/etl/autoloader/files")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from `dlt-catalog`.etl.orders_union_bronze

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from `dlt-catalog`.etl.orders_autoloader_bronze

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from `dlt-catalog`.etl.orders_agg_f_gold

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from `dlt-catalog`.etl.orders_agg_o_gold

# COMMAND ----------

# MAGIC %md
# MAGIC ## CDC Setup for raw Customer table

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Add new columns to track the change - Insert, Delete or Truncate
# MAGIC alter table `dlt-catalog`.etl.customer_raw add columns (
# MAGIC    _dlt_change_type string,
# MAGIC    _dlt_timestamp timestamp
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC -- update the existing data in the raw customer table for the new columns
# MAGIC update `dlt-catalog`.etl.customer_raw 
# MAGIC set _dlt_change_type = 'I', 
# MAGIC _dlt_timestamp = current_timestamp() - interval '3 day'

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Check the updated data in the raw customer table
# MAGIC select * from `dlt-catalog`.etl.customer_raw

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from `dlt-catalog`.etl.customer_scd1_bronze
# MAGIC --where c_custkey = 7

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from `dlt-catalog`.etl.customer_scd2_bronze
# MAGIC where c_custkey = 7

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Insert test comments for a customer key
# MAGIC INSERT INTO `dlt-catalog`.etl.customer_raw 
# MAGIC (c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment, _dlt_change_type, _dlt_timestamp)
# MAGIC VALUES 
# MAGIC (7, 'Customer#000000007', 'TcGe5gaZNgVePxU5kRrvXBfkasDTea', 18, '28-190-982-9759', 9561.95, 'AUTOMOBILE', 'New test comment for CDC test', 'I', current_timestamp());

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Backloading data for a customer key
# MAGIC INSERT INTO `dlt-catalog`.etl.customer_raw 
# MAGIC (c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment, _dlt_change_type, _dlt_timestamp)
# MAGIC VALUES 
# MAGIC (7, 'Customer#000000007', 'TcGe5gaZNgVePxU5kRrvXBfkasDTea', 18, '28-190-982-9759', 9561.95, 'AUTOMOBILE', 'BackLoading data for CDC', 'I', current_timestamp() - interval '1 days');

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Using 'D' to Delete data for a customer key for column _dlt_change_type value
# MAGIC INSERT INTO `dlt-catalog`.etl.customer_raw 
# MAGIC (c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment, _dlt_change_type, _dlt_timestamp)
# MAGIC VALUES 
# MAGIC (7, 'Customer#000000007', 'TcGe5gaZNgVePxU5kRrvXBfkasDTea', 18, '28-190-982-9759', 9561.95, 'AUTOMOBILE', 'Deleting data for CDC', 'D', current_timestamp());

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Using 'T' to Truncate data for a customer key for column _dlt_change_type value
# MAGIC INSERT INTO `dlt-catalog`.etl.customer_raw 
# MAGIC (c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment, _dlt_change_type, _dlt_timestamp)
# MAGIC VALUES 
# MAGIC (7, 'Customer#000000007', 'TcGe5gaZNgVePxU5kRrvXBfkasDTea', 18, '28-190-982-9759', 9561.95, 'AUTOMOBILE', 'Truncating data for CDC', 'T', current_timestamp());

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Qulaity & Expectations

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Insert data in the Orders raw table for testing data quality using expect
# MAGIC -- Setting o_orderstatus with invalid values (valid - O, F, P)
# MAGIC -- Setting o_totalprice with negative value
# MAGIC INSERT INTO `dlt-catalog`.etl.orders_raw 
# MAGIC VALUES
# MAGIC   (999999, 227285, 'NA', 1000.00, '2025-05-15', '1-URGENT', 'Clerk#000000001', 0, 'Test order for data quality for rec # 1'),
# MAGIC   (999999, 227285, 'O', -100, '2025-05-15', '1-URGENT', 'Clerk#000000001', 0, 'Test order for data quality for rec # 2'),
# MAGIC   (999999, 227285, null, 1000.00, '2025-05-15', '1-URGENT', 'Clerk#000000001', 0, 'Test order for data quality for rec # 3')

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Insert data in the Customer raw table for testing data quality using expect - setting c_mktsegment as null
# MAGIC INSERT INTO `dlt-catalog`.etl.customer_raw
# MAGIC VALUES (999999, 'Customer#000000008', 'Address#000000008', 19, '29-191-983-9760', 10500.00, null, 'Test customer for data quality', 'I', current_timestamp())

# COMMAND ----------

# MAGIC %sql
# MAGIC Select * from `dlt-catalog`.etl.orders_union_bronze
# MAGIC where o_orderkey = 999999

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) 
# MAGIC FROM `dlt-catalog`.etl.orders_union_bronze
# MAGIC WHERE o_orderstatus NOT IN ('F', 'O') OR o_orderstatus IS NULL;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Pipeline Monitoring 
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from event_log("1845b480-06f3-4f53-b5f0-9f889ec013e1")
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE VIEW event_log_raw
# MAGIC AS SELECT * FROM event_log("1845b480-06f3-4f53-b5f0-9f889ec013e1")

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW latest_update AS SELECT origin.update_id AS id FROM event_log_raw WHERE event_type = 'create_update' ORDER BY timestamp DESC LIMIT 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   row_expectations.dataset as dataset,
# MAGIC   row_expectations.name as expectation,
# MAGIC   SUM(row_expectations.passed_records) as passing_records,
# MAGIC   SUM(row_expectations.failed_records) as failing_records
# MAGIC FROM
# MAGIC   (
# MAGIC     SELECT
# MAGIC       explode(
# MAGIC         from_json(
# MAGIC           details :flow_progress :data_quality :expectations,
# MAGIC           "array<struct<name: string, dataset: string, passed_records: int, failed_records: int>>"
# MAGIC         )
# MAGIC       ) row_expectations
# MAGIC     FROM
# MAGIC       event_log_raw,
# MAGIC       latest_update
# MAGIC     WHERE
# MAGIC       event_type = 'flow_progress'
# MAGIC       AND origin.update_id = latest_update.id
# MAGIC   )
# MAGIC GROUP BY
# MAGIC   row_expectations.dataset,
# MAGIC   row_expectations.name