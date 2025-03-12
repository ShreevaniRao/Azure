# Databricks notebook source
# MAGIC %md
# MAGIC ### Create STAR Schema with Dim & Fact tables using data from Silver container data

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
# MAGIC SELECT distinct Model_id, Model_Category FROM parquet.`abfss://silver@stgcarsdatalake.dfs.core.windows.net/carsales`

# COMMAND ----------

# Create a dataframe to hold the data queried
df_src = spark.sql('''
SELECT distinct Model_id, Model_Category FROM parquet.`abfss://silver@stgcarsdatalake.dfs.core.windows.net/carsales`
''')
display(df_src)

# COMMAND ----------

# create the schema for the new table 'Dim_Model' with the new surrogate key with conditional stmt to copy data from silver container
if spark.catalog.tableExists('`cars-catalog`.gold.dim_model') and load_incremental == '1':
    df_sink = spark.sql('''
                        SELECT dim_model_key, model_id, model_category 
                        FROM `cars-catalog`.gold.dim_model 
                       ''')
else: # this will create the new empty table with surrogate key

    df_sink = spark.sql('''
                        SELECT 1 as dim_model_key, model_id, model_category 
                          FROM parquet.`abfss://silver@stgcarsdatalake.dfs.core.windows.net/carsales` 
                          where 1 = 0
                        ''')

# COMMAND ----------

# Join the source and sink dataframes to copy the data with left join to be able to update the surrogate key
df_table = df_src.join(df_sink, df_src.Model_id == df_sink.model_id, 'left').select(df_src.Model_id, df_src.Model_Category, df_sink.dim_model_key)
df_table.display()

# COMMAND ----------

# separate the data to be able to update or insert the incremental data
df_table_with_existing_data = df_table.filter(df_table.dim_model_key.isNotNull())
df_table_with_existing_data.display()

# COMMAND ----------

# separate the data to be able to update or insert the incremental data
df_table_with_new_incremental_data = df_table.filter(df_table.dim_model_key.isNull()).select(df_table.Model_id, df_table.Model_Category)
df_table_with_new_incremental_data.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Surrogate Key

# COMMAND ----------

# Use the Widget flag to determine if we are loading incremental data or not
if(load_incremental == '0'):
    max_value = 1
else:
    max_value_df = spark.sql("Select max(dim_model_key) from `cars-catalog`.gold.dim_model")
    max_value_result = max_value_df.collect()[0][0] # returns the 1st row and 1st column value from the df
    max_value = (max_value_result if max_value_result is not None else 0) + 1  



# COMMAND ----------

# Update the surrogate key in the dataframe
df_table_with_new_incremental_data = df_table_with_new_incremental_data.withColumn('dim_model_key', max_value + monotonically_increasing_id())

# COMMAND ----------

df_table_with_new_incremental_data.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Final Dataframe to join bothe dataframes

# COMMAND ----------

df_table_dim_model = df_table_with_existing_data.union(df_table_with_new_incremental_data)
df_table_dim_model.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### SCD TYPE 1 (UPSERT)

# COMMAND ----------

from delta.tables import DeltaTable

# COMMAND ----------

#Incremental Run
if spark.catalog.tableExists('`cars-catalog`.gold.dim_model') and load_incremental == '1':
    delta_tbl = DeltaTable.forPath(spark, "abfss://gold@stgcarsdatalake.dfs.core.windows.net/dim_model")
    delta_tbl.alias('trg').merge(df_table_dim_model.alias('src'), 'trg.dim_model_key = src.dim_model_key')\
        .whenMatchedUpdateAll()\
        .whenNotMatchedInsertAll()\
        .execute()

# Initial Run
else:
    df_table_dim_model.write.format('delta')\
        .mode('overwrite')\
        .option("path","abfss://gold@stgcarsdatalake.dfs.core.windows.net/dim_model")\
        .saveAsTable('`cars-catalog`.gold.dim_model')

# COMMAND ----------

# MAGIC %sql
# MAGIC use catalog `cars-catalog`; select * from `gold`.`dim_model`;

# COMMAND ----------

# Rerun the upsert logic to verify the logic is working and keeping the same row count for now
