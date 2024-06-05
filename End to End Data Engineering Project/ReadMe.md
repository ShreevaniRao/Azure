<div align="center">
  <div id="user-content-toc">
    <ul>
      <summary><h1 style="display: inline-block;"> Azure End to End Data Engineering Project </h1></summary>
    </ul>
  </div>
  
  <p>To Analyze insights of AdventureWorks dataset by creating an Azure End to End Data Pipeline that Extracts, Loads and Transforms data to showcase with a Dashboard visualization </p>
<p> Extract On-prem DB Sql Sever Data to Azure Data Lake Storage using Azure Data Factory, Transform the ingested data using Azure Databricks with Spark cluster, Loading transformed data using Azure Synapse Analytics to Visualize in PowerBI </p>
</div>
<br>

##  Table of Contents
1. [Project Overview](#introduction)
2. [Key Insights](#key-insights)
3. [Project Architecture](#project-architecture)  
  3.1. [Data Ingestion](#data-ingestion)  
  3.2. [Data Transformation](#data-transformation)  
  3.3. [Data Loading](#data-loading)  
  3.4. [Data Reporting](#data-reporting)
4. [Credits](#credits)

## Project Overview 

This an end-to-end data engineering project using Azure cloud computing platform, which attempts the use case to build an end to end solution by ingesting the tables from on-premise SQL Server database using Azure Data Factory and then store the data in Azure Data Lake. Then Azure databricks is used to transform the RAW data to the most cleanest form of data and then using Azure Synapse Analytics to load the clean data to a Sql Serverless database and finally using Microsoft Power BI to integrate with Azure synapse analytics to build an interactive dashboard to derive & display the business insights. Also, we are using Azure Active Directory (AAD) and Azure Key Vault for the monitoring and governance purpose.

![image](https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/ProjectOverviewResize.png)

### Dataset

**AdventureWorks** is a sample database provided by Microsoft for free on online platforms. It is a product sample database originally published by Microsoft to demonstrate the supposed design of a SQL server database using SQL server 2008. Here are some key points to know about AdventureWorks:

- AdventureWorks database supports a manufacturing MNC named Adventure Works Cycles.
- It is a sample Online Transaction Processing (or OLTP) database, which is a type of data processing where multiple transactions occur concurrently. These are shipped by Microsoft with all of their SQL server products.

For this project I used the **Lightweight (LT) data**: a lightweight and pared down version of the OLTP sample. [Download here](https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorksLT2014.bak)

### Project Goals

- Connect on-premise SQL Server database to Azure cloud using SHIR - Self Hosting Integration Runtime.
- Ingest data as Parquet files into Azure Data Lake storage container using Azure Data Factory(ADF).
- Apply data cleaning and transformation logic using Pyspark & Python in Azure Databricks notebook.
- Utilize Azure Synapse Analytics to load transformed data into Delta files in Data Lake Storage container.
- Analyze and create interactive data visualizations and reports with Microsoft Power BI Desktop connecting to Azure Synapse Analytics serverless database.
- Implement Azure Active Directory (AAD) and Azure Key Vault for monitoring and governance.

## Project Architecture

Below diagram displays the design and details of the resource architecture :

<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/AzurePipeline.gif" width="850" height="500"> 

### Setup Environment
- Create the Resource group.
- Create all the resources - ADF, Azure Databricks, Azure Key Vault, Data Lake Storage container & Azure Synapse Analytics in the resource group.
- Create the Data lake storage containers structure - brone, silver & gold to support the ETL data.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/EnvironmentSetupResize.png" width="850" height="500"> >

### Data Ingestion
- Connected the on-premise SQL Server database with Azure using Microsoft Self Hosting Integration Runtime.
- Created ADF pipeline to orchestrate acitivites that lookup tablenames and creates data lake container hierarchy that includes the schema name of the tables.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/SHIRSetupResize.png" width="850" height="550">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/SHIRSetup2Resize.png" width="850" height="550">

- Ingested the extracted data from on-premise SQL Server tables to Azure Data Lake Storage Gen2.
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/CopyingDataUsingPipelineActivitiesResize.png" width="850" height="550">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/DataIngestionFoldersWithParquetFilesResize.png" width="850" height="550">


### Data Transformation
- Mounted Azure Blob Storage to Databricks to read raw data from the Data Lake 'bronze' container.
- Used Spark Cluster in Azure Databricks to transform using Pyspark & Python with multiple Azure Databricks notebooks.
- Created pipeline activities in ADF to save the transformed data in Delta file format into 'silver' & 'gold' storage containers.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/StorageMount.png" width="800" height="550">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/TransformCodeBronzetoSilver.png" width="800" height="550">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/TransformedDataInSilverContainer.png" width="800" height="550">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/CompletePipeline-ADF.png" width="800" height="400">


### Data Loading
- Created Azure Synapse Analytics pipeline to orchestrate activities to execute a stored procedure to dynamically create views for each table in a Serverless SQL database(gold_db) using table names from the 'gold' data lake storage container.
- Created Linked Service for Azure Sql database to connect to the Stored procedure.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/SynapsePipelineForGoldContainer.png" width="800" height="400">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/SynapsePipelineCreatedViews.png" width="800" height="400">

### Data Reporting
- Connected Microsoft Power BI desktop to Azure Synapse with Sql Serverless endpoint, to import the data from the Serverless database(gold_db) views to create interactive and insightful data visualization.
- Updated the data modeling to establish the relationship between the tables
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/PBDataModeling.png" width="800" height="400">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Power%20BI/Power%20BI%20Viz.png" width="800" height="400">

###  Technologies Used

- **Data Source**: SQL Server
- **Orchestration**: Azure Data Factory
- **Ingestion**: Azure Data Lake Gen2
- **Storage**: Azure Synapse Analytics
- **Authentication and Secrets Management**: Azure Active Directory and Azure Key Vault
- **Data Visualization**: PowerBI


## Credits

- This Project is inspired by the video of the [YouTube Channel "Mr. K Talks Tech"](https://www.youtube.com/watch?v=iQ41WqhHglk)  


