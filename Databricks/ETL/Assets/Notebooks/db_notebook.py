# Databricks notebook source
# MAGIC %md
# MAGIC ### Create Catalog

# COMMAND ----------

# MAGIC %md
# MAGIC I created using UI, but we can create with SQL - CREATE CATALOG 'cars-catalog'

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Schema

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA `cars-catalog`.silver

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA `cars-catalog`.gold

# COMMAND ----------

