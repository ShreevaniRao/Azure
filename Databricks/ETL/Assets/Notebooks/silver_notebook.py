# Databricks notebook source
# MAGIC %md
# MAGIC ### Data Reading

# COMMAND ----------

df = spark.read.format('parquet')\
        .option('inferSchema',True)\
        .load('abfss://bronze@stgcarsdatalake.dfs.core.windows.net/rawdata')

# COMMAND ----------

df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create new column - Model_Category

# COMMAND ----------

from pyspark.sql.functions import *

# COMMAND ----------

df = df.withColumn('Model_Category', split(col('Model_ID'), '-')[0])

# COMMAND ----------

df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create new column for aggregation data - RevenuePerUnitSold

# COMMAND ----------

df = df.withColumn('RevenuePerUnitSold', col('Revenue')/col('Units_Sold') )
df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Perform AD-HOC query
# MAGIC Check which branch has sold max units for each year (with Pie chart viz)

# COMMAND ----------

df.groupBy('Year','BranchName').agg(sum('Units_Sold').alias('Total_Units')).sort('Year','Total_Units',ascending=[1,0]).display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Write Data to Silver container

# COMMAND ----------

df.write.mode('overwrite').format('parquet').save('abfss://silver@stgcarsdatalake.dfs.core.windows.net/carsales')

# COMMAND ----------

# MAGIC %md
# MAGIC ### Querying data back from the silver container

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM parquet.`abfss://silver@stgcarsdatalake.dfs.core.windows.net/carsales`

# COMMAND ----------

