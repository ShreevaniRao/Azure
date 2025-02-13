# Databricks notebook source
# MAGIC %md
# MAGIC ### Create Fact Table

# COMMAND ----------

# MAGIC %md
# MAGIC **Read Silver data for the rest of the fact table columns**

# COMMAND ----------

#Check the columns from the silver container data
df_silver = spark.sql("SELECT * FROM PARQUET.`abfss://silver@stgcarsdatalake.dfs.core.windows.net/carsales`")
df_silver.display()

# COMMAND ----------

# Create dataframes from all the 4 Dim tables to be able to create the composite Primary key from them for the Fact Table
df_dealer = spark.sql("SELECT * FROM `cars-catalog`.gold.dim_dealer")
df_branch = spark.sql("SELECT * FROM `cars-catalog`.gold.dim_branch")
df_model = spark.sql("SELECT * FROM `cars-catalog`.gold.dim_model")
df_date = spark.sql("SELECT * FROM `cars-catalog`.gold.dim_date")


# COMMAND ----------

#Joining the dataframes
df_fact = df_silver.join(df_branch, df_silver.Branch_ID == df_branch.Branch_id, how='left')\
        .join(df_dealer, df_silver.Dealer_ID == df_dealer.Dealer_id, how='left')\
        .join(df_model, df_silver.Model_ID == df_model.Model_id, how='left')\
        .join(df_date, df_silver.Date_ID == df_date.Date_id, how='left')\
        .select( df_silver.Revenue, df_silver.Units_Sold, df_silver.RevenuePerUnitSold, df_branch.dim_branch_key, df_dealer.dim_dealer_key, df_model.dim_model_key, df_date.dim_date_key)

df_fact.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating the Fact Table with DELTA format
# MAGIC

# COMMAND ----------

from delta.tables import DeltaTable

# COMMAND ----------

if spark.catalog.tableExists("cars-catalog", "gold.fact_carsales") and load_incremental == '1':
    deltatbl = DeltaTable.forName(spark, "cars-catalog.gold.fact_carsales")

    deltatbl.alias("t").merge(df_fact.alias("s"), "t.dim_branch_key = s.dim_branch_key AND t.dim_dealer_key = s.dim_dealer_key AND t.dim_model_key = s.dim_model_key AND t.dim_date_key = s.dim_date_key")\
        .whenMatchedUpdateAll()\
        .whenNotMatchedInsertAll()\
        .execute()

else:
    df_fact.write.format("delta")\
        .mode("overwrite")\
        .option("path", "abfss://gold@stgcarsdatalake.dfs.core.windows.net/fact_carsales")\
        .saveAsTable("`cars-catalog`.gold.fact_carsales")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from `cars-catalog`.gold.fact_carsales