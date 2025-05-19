# Databricks notebook source


# COMMAND ----------

# MAGIC %md
# MAGIC ### Create STAR Schema with Dim & Fact tables using data from Silver container data
# MAGIC - **Dim_Dealer table**

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# MAGIC %md
# MAGIC  **Create 'load' flag to switch between initial and incremental run**

# COMMAND ----------

dbutils.widgets.text('load_incremental','0')

# COMMAND ----------

load_incremental = dbutils.widgets.get('load_incremental')
print(load_incremental)

# COMMAND ----------

# MAGIC %md
# MAGIC **Spilt the data in the Silver container to create 4 new Dim tables first**

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Query the details for the First new Dim Table - Model
# MAGIC SELECT Dealer_id, Dealername FROM parquet.`abfss://silver@stgcarsdatalake.dfs.core.windows.net/carsales`

# COMMAND ----------

# Create a dataframe to hold the data queried
df_src = spark.sql('''
SELECT distinct Dealer_id, DealerName FROM parquet.`abfss://silver@stgcarsdatalake.dfs.core.windows.net/carsales`
''')
display(df_src)

# COMMAND ----------

# create the schema for the new table 'Dim_Dealer' with the new surrogate key with conditional stmt to copy data from silver container
if spark.catalog.tableExists('`cars-catalog`.gold.dim_dealer') and load_incremental == '1':
    df_sink = spark.sql('''
                        SELECT dim_dealer_key, dealer_id, dealername 
                        FROM `cars-catalog`.gold.dim_dealer
                       ''')
else: # this will create the new empty table with surrogate key
    df_sink = spark.sql('''
                        SELECT 1 as dim_dealer_key, dealer_id, dealername 
                          FROM parquet.`abfss://silver@stgcarsdatalake.dfs.core.windows.net/carsales` 
                          where 1 = 0
                        ''')
    
df_sink.display()

# COMMAND ----------

# Join the source and sink dataframes to copy the data with left join to be able to update the surrogate key
df_table = df_src.join(df_sink, df_src['Dealer_id'] == df_sink['Dealer_id'], 'left').select(df_src['Dealer_id'], df_src['DealerName'], df_sink['dim_dealer_key'])
df_table.display()

# COMMAND ----------

# separate the data to be able to update or insert the incremental data
df_table_with_existing_data = df_table.filter(df_table.dim_dealer_key.isNotNull())
df_table_with_existing_data.display()

# COMMAND ----------

# separate the data to be able to update or insert the incremental data
df_table_with_new_incremental_data = df_table.filter(df_table.dim_dealer_key.isNull()).select(df_table.Dealer_id, df_table.DealerName)
df_table_with_new_incremental_data.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Surrogate Key

# COMMAND ----------

# Use the Widget flag to determine if we are loading incremental data or not
if(load_incremental == '0'):
    max_value = 1
else:
    max_value_df = spark.sql("Select max(dim_dealer_key) from `cars-catalog`.gold.dim_dealer")
    max_value_result = max_value_df.collect()[0][0]
    max_value = (max_value_result if max_value_result is not None else 0) + 1  # returns the 1st row and 1st column value from the df



# COMMAND ----------

# Update the surrogate key in the dataframe
df_table_with_new_incremental_data = df_table_with_new_incremental_data.withColumn('dim_dealer_key', max_value + monotonically_increasing_id())

# COMMAND ----------

df_table_with_new_incremental_data.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Final Dataframe to join bothe dataframes

# COMMAND ----------

df_table_dim_dealer = df_table_with_existing_data.union(df_table_with_new_incremental_data)
df_table_dim_dealer.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### SCD TYPE 1 (UPSERT)

# COMMAND ----------

# MAGIC %md
# MAGIC

# COMMAND ----------

from delta.tables import DeltaTable

# COMMAND ----------

from delta.tables import DeltaTable#Incremental Run
if spark.catalog.tableExists('`cars-catalog`.gold.dim_dealer') and load_incremental == '1':
    delta_tbl = DeltaTable.forPath(spark, "abfss://gold@stgcarsdatalake.dfs.core.windows.net/dim_dealer")
    delta_tbl.alias('trg').merge(df_table_dim_dealer.alias('src'), 'trg.dim_dealer_key = src.dim_dealer_key')\
        .whenMatchedUpdateAll()\
        .whenNotMatchedInsertAll()\
        .execute()

# Initial Run
else:
    df_table_dim_dealer.write.format('delta')\
        .mode('overwrite')\
        .option("path","abfss://gold@stgcarsdatalake.dfs.core.windows.net/dim_dealer")\
        .saveAsTable('`cars-catalog`.gold.dim_dealer')

# COMMAND ----------

# MAGIC %sql
# MAGIC use catalog `cars-catalog`; select * from `gold`.`dim_dealer`;

# COMMAND ----------

# Rerun the upsert logic to verify the logic is working and keeping the same row count for now