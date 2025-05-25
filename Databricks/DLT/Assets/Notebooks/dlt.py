# Databricks notebook source
import dlt

# COMMAND ----------

# read from configuration settings the order status to create dynamic tables for each order status type
order_status = spark.conf.get("orderStatus", "NA")

# COMMAND ----------

# Data quality rules as dictionary for Orders & Customer data (warn (default), drop or fail) - Rule name & its value
order_rules ={
    "Valid Order Status" : "o_orderstatus in ('F', 'O')",
    "Valid Order Price" : "o_totalprice > 0"
}

customer_rules ={
    "Valid Market Segment": "c_mktsegment is not null"
}

# COMMAND ----------

# Create streaming table for Orders

@dlt.table(
  comment="This table contains all the data from the bronze layer for Orders.",
  table_properties={
    "quality": "bronze"
  }
)
@dlt.expect_all_or_drop(order_rules) #drop
def orders_bronze():
  return spark.readStream.table("`dlt-catalog`.etl.orders_raw")

# COMMAND ----------

# Read Orders data from the landing files folder using autoloader
@dlt.table(
  comment="Incremental Order data from Autoloader",
  table_properties={
    "quality": "bronze"
  },
  name = "orders_autoloader_bronze"
)

def load_autoloader():
  df = spark.readStream.format("cloudFiles") \
    .option("cloudFiles.schemaHints", "o_orderkey long, o_custkey long, o_orderstatus string, o_totalprice decimal(18,2), o_orderdate date, o_orderpriority string, o_clerk string, o_shippriority integer, o_comment string")\
    .option("cloudFiles.format", "csv") \
    .option("cloudFiles.schemaEvolutionMode", "none") \
    .load("/Volumes/dlt-catalog/etl/autoloader/files/")
  return df

# COMMAND ----------

# Combine the data from both tables using append_flow and write to a new table to be able to append streaming source and not just union the 2 datasets.

dlt.create_streaming_table("orders_union_bronze")

@dlt.append_flow(target = "orders_union_bronze")
def order_append():
    df = spark.readStream.table("LIVE.orders_bronze")
    return df

@dlt.append_flow(target = "orders_union_bronze")
def order_append_incremental():
    df = spark.readStream.table("LIVE.orders_autoloader_bronze")
    return df



# COMMAND ----------

# Create materialized view for Customer

@dlt.table(
  comment="This table contains all the data from the bronze layer for Customer.",
  table_properties={
    "quality": "bronze"
  }
)
def customer_bronze():
  return spark.read.table("`dlt-catalog`.etl.customer_raw")

# COMMAND ----------

# Create streaming view for Customer, which will be the source for the SCD 1 & SCD 2 table. To be able to use Apply_Changes the source has to be a streaming. Commented the above code to use this streaming for the SCD tables

@dlt.view(
   comment="This table contains all the data from the bronze layer for Customer."
 )

def customer_bronze_view():
  return spark.readStream.table("`dlt-catalog`.etl.customer_raw")

# COMMAND ----------

# SCD 1 table - for tracking , deletes, truncates and upserts
from pyspark.sql.functions import expr

dlt.create_streaming_table("customer_scd1_bronze")
dlt.apply_changes(
  target = "customer_scd1_bronze",
  source = "customer_bronze_view",    
  keys = ["c_custkey"],
  stored_as_scd_type = 1,
  sequence_by = "_dlt_timestamp",
  apply_as_deletes = expr("_dlt_change_type = 'D'"),
  apply_as_truncates = expr("_dlt_change_type = 'T'"),
)


# COMMAND ----------

# SCD 2 table - for tracking history of changes
dlt.create_streaming_table("customer_scd2_bronze")
dlt.apply_changes(
  target = "customer_scd2_bronze",
  source = "customer_bronze_view",    
  keys = ["c_custkey"],
  stored_as_scd_type = 2,
  sequence_by = "_dlt_timestamp",
  except_column_list = ["_dlt_change_type", "_dlt_timestamp"]
)

# COMMAND ----------

# create a view to join Orders and Customer (testing before SCD)
@dlt.view(
  comment="This view contains all the data from the bronze layer for Orders and Customer."
)
def order_customer_view():
  df_customer = spark.read.table("LIVE.customer_bronze")
  df_orders = spark.read.table("LIVE.orders_bronze")
  
  return df_orders.join(df_customer, how="left_outer", on=df_orders["o_custkey"] == df_customer["c_custkey"])

# COMMAND ----------

# Create a view to join Orders and Customer, Comment the above code to use the SCD tables.

@dlt.view(
  comment="This view contains all the data from the bronze layer for Orders and Customer."
)
@dlt.expect_all_or_drop(order_rules) #drop
@dlt.expect_all(customer_rules) #warn
def order_customer_view():
  df_customer = spark.read.table("LIVE.customer_scd2_bronze").where ("__END_AT IS NULL")
  df_orders = spark.read.table("LIVE.orders_union_bronze") #use the new live table instead of the old one
  return df_orders.join(df_customer, how="left_outer", on=df_orders["o_custkey"] == df_customer["c_custkey"])

# COMMAND ----------

# Create another materialized view for silver layer version of the order_customer_view
from pyspark.sql.functions import current_timestamp

@dlt.table(
  comment="This silver layer mat view will be used from the above view with additional column.",
  table_properties={"quality": "silver"},
  name = "customerOrders_silver"
)
def order_customer_silver_view():
  return spark.read.table("LIVE.order_customer_view").withColumn("__insert_date", current_timestamp())

# COMMAND ----------

# Create materialized view for gold layer that will have aggregations - order counts based on customer mkt segment
from pyspark.sql.functions import current_timestamp,count,sum

@dlt.table(
  comment="This gold layer mat view will be used for aggregations.",
  table_properties={
    "quality": "gold"
  }
)
def orders_aggregated_gold():
  df = spark.read.table("LIVE.customerOrders_silver")
  df_agg = df.groupBy("c_mktsegment").agg(count("o_orderkey").alias("orders_count_by_mkg_seg"), sum("o_totalprice").alias("sum_totalprice")).withColumn("__insert_date", current_timestamp())
  return df_agg

# COMMAND ----------

# create dynamic tables for each order status type using the configuration settings
for _status in order_status.split(","):
    @dlt.table(
    comment="This gold layer mat view will be used for aggregations.",
    table_properties={
        "quality": "gold"
    },
    name = f"orders_agg_{_status}_gold"
    )
    def func():
        df = spark.read.table("LIVE.customerOrders_silver")
        df_agg = df.where(f"o_orderstatus = '{_status}'").groupBy("c_mktsegment").agg(count("o_orderkey").alias("orders_count_by_mkg_seg"), sum("o_totalprice").alias("sum_totalprice")).withColumn("__insert_date", current_timestamp())
        return df_agg 