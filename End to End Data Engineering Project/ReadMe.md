<div align="center">
  <div id="user-content-toc">
    <ul>
      <summary><h1 style="display: inline-block;"> Azure End to End Data Engineering Project </h1></summary>
    </ul>
  </div>
</div>

<div align="left">

### To analyze insights and create a Power BI visualization using sample AdventureWorks dataset with Azure End to End Data Engineering pipeline that ingests data from On-Premise Sql Server database by orchestrating Ingestion, Transform and Load activities. 

### Azure Data Factory pipeline orchestrates activities to ingest On-premise Sql Sever Data to Azure Data Lake Storage, transforms the ingested data using Azure Databricks notebooks that code the logic using Pyspark & Python with Spark cluster. Azure Synapse Analytics pipeline loads the transformed data from Data lake containers into Serveless SQL database views created dynamically using a stored procedure, which finally Power BI desktop imports by connecting to the Serverless SQL Endpoint of Azure Synapse database. 
</div>
<br>

##  Table of Contents
1. [Project Overview](#introduction)
2. [Project Architecture](#project-architecture)
  * 2.1. [Data Ingestion](#data-ingestion)  
  * 2.2. [Data Transformation](#data-transformation)  
  * 2.3. [Data Loading](#data-loading)
  * 2.4. [Data Visualization](#data-reporting)
  * 2.5. [End to End Pipeline Testing](#pipeline-trigger)
3. [Credits](#credits)
   
<a name="introduction"></a>
## Project Overview 

This is an end-to-end data engineering project using **Azure cloud computing platform**, which attempts the use case to build an end to end solution by ingesting the tables from on-premise SQL Server database using **Azure Data Factory** pipeline to store the data in **Azure Data Lake** using Self hosting integration runtime and transform the raw data with multiple **Azure Databricks** notebooks using Pyspark & Python. **Azure Synapse Analytics** uses pipeline to orchestrate activities that load the transformed data to a Sql Serverless database to create dynamic database views which can always get updated for any changes in the schema and data in data lake. Finally using **Microsoft Power BI** to integrate with Azure synapse analytics to import the data from the views to build an interactive dashboard to derive & display the business insights. Also, I have used **Azure Active Directory** (AAD) and **Azure Key Vault** for the monitoring and governance purpose. A **medallion architecture** of data design pattern is used, to logically organize data in a lakehouse, with the goal of incrementally improving the quality of data as it flows through various layers.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/ProjectOverviewUpdatedColors.png" width="850" height="500"> 

### Dataset

**AdventureWorks** is a sample database provided by Microsoft for free on online platforms. It is a product sample database originally published by Microsoft to demonstrate the supposed design of a SQL server database using SQL server 2008. Here are some key points to know about AdventureWorks:

- AdventureWorks database supports a manufacturing MNC named Adventure Works Cycles.
- It is a sample Online Transaction Processing (or OLTP) database, which is a type of data processing where multiple transactions occur concurrently. These are shipped by Microsoft with all of their SQL server products.

For this project I used the **Lightweight (LT) data**: a lightweight and pared down version of the OLTP sample. [Download here](https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorksLT2014.bak)

### Project Goals

Demonstrate using multiple Azure resources to
- Connect on-premise SQL Server database to Azure cloud using SHIR - **Self Hosting Integration Runtime**.
- Ingest data as **Parquet files** into Azure Data Lake storage container using Azure Data Factory(ADF).
- Apply data cleaning and transformation logic using Pyspark & Python in Azure Databricks notebook.
- Utilize Azure Synapse Analytics to load transformed data into **Delta files** in Data Lake Storage container.
- Analyze and create interactive data visualizations and reports with Microsoft Power BI Desktop connecting to Azure Synapse Analytics serverless database.
- Implement Azure Active Directory (AAD) and Azure Key Vault for monitoring and governance.

<a name="project-architecture"></a>
## Project Architecture

Below diagram displays the design and details of the resource architecture :

<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/AzurePipeline.gif" width="850" height="500"> 

<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/MedallionArchitecture.png" width="850" height="500"> 

### Setup Environment
- Create the Resource group.
- Create all the resources - ADF, Azure Databricks, Azure Key Vault, Data Lake Storage container & Azure Synapse Analytics in the resource group.
- Create the Data lake storage containers structure - brone, silver & gold to contain the ETL data.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/EnvironmentSetupResize.png" width="850" height="500"> >

<a name="data-ingestion"></a>
### Data Ingestion
- Connected the on-premise SQL Server database with Azure using Microsoft Self Hosting Integration Runtime.
- Created ADF pipeline to orchestrate acitivites that lookup tablenames and creates data lake container hierarchy using the schema and table names.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/SHIRSetupResize.png" width="850" height="550">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/SHIRSetup2Resize.png" width="850" height="550">

- Ingested the extracted data from on-premise SQL Server tables to Azure Data Lake Storage Gen2.
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/CopyingDataUsingPipelineActivitiesResize.png" width="850" height="550">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/DataIngestionFoldersWithParquetFilesResize.png" width="850" height="550">

<a name="data-transformation"></a>
### Data Transformation
- Mounted Azure Blob Storage to Databricks to read raw data from the Data Lake 'bronze' container.
- Used Spark Cluster in Azure Databricks to transform using Pyspark & Python with multiple Azure Databricks notebooks.
- Created pipeline activities in ADF to save the transformed data in Delta file format into 'silver' & 'gold' storage containers.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/StorageMount.png" width="800" height="550">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/TransformCodeBronzetoSilver.png" width="800" height="550">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/TransformedDataInSilverContainer.png" width="800" height="550">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/CompletePipeline-ADF.png" width="800" height="400">

<a name="data-loading"></a>
### Data Loading
- Created Azure Synapse Analytics pipeline to orchestrate activities to execute a stored procedure to dynamically create views for each table in a Serverless SQL database(gold_db) using table names from the 'gold' data lake storage container.
- Created Linked Service for Azure Sql database to connect to the Stored procedure.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/SynapsePipelineForGoldContainer.png" width="800" height="400">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/SynapsePipelineCreatedViews.png" width="800" height="400">

<a name="data-reporting"></a>
### Data Visualization
- Connected Microsoft Power BI desktop to Azure Synapse with Sql Serverless endpoint, to import the data from the Serverless database(gold_db) views to create interactive and insightful data visualization.
- Updated the data modeling to establish the relationship between the tables
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/PBDataModeling.png" width="800" height="400">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Power%20BI/Power%20BI%20Viz.png" width="800" height="400">

<a name="pipeline-trigger"></a>
### End to End Pipeline Testing
- Created a scheduled trigger in Azure Data Factory that runs the pipeline to copy the new data inserted (new customers) in the On-Premise database tables.
- The Power BI visualization dynamically updates the latest data connected to the Serverless Sql database in Azure Synapse Analytics.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/ScheduleTriggerCompletePipeline.png" width="800" height="400">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Assets/CompletePipelineRunSuceeded.png" width="800" height="400">
</br>
<p>
<img src="https://github.com/ShreevaniRao/Azure/blob/main/End%20to%20End%20Data%20Engineering%20Project/Power%20BI/PowerBIVizAfterPipelineRun.png" width="800" height="400">
</p>




--------------------------------------------------------------------------------------------------------------------------------------------------------
###  Technologies Used

- **Data Source**: SQL Server
- **Orchestration**: Azure Data Factory & Azure Databricks
- **Ingestion**: Azure Data Lake Gen2
- **Storage**: Azure Synapse Analytics
- **Authentication and Secrets Management**: Azure Active Directory and Azure Key Vault
- **Data Visualization**: Power BI Desktop

<a name="credits"></a>
## Credits
- This Project is inspired by the video of the [YouTube Channel "Mr. K Talks Tech"](https://www.youtube.com/watch?v=iQ41WqhHglk)  


