
<div align="center">
  <div id="user-content-toc">
    <ul>
      <summary><h1 style="display: inline-block;"> Azure Logical/Serverless Data Warehouse - Synapse Analytics </h1></summary>
    </ul>
  </div>
</div>

<div align="left">
  
### The logical data warehouse (LDW) pattern lays a lightweight virtualized relational layer on top of data that's stored in a data lake or database. This virtualization layer provides data warehouse access without requiring data movement. This solution can combine online transaction processing (OLTP) data with analytical data from data lakes for a low-complexity, low-latency way to serve business intelligence (BI) and analytics workloads.
### Azure Synapse serverless SQL pools define an LDW that has logical tables and views accessible through the Azure Synapse workspace serverless SQL pool on-demand endpoint.
### Reporting, BI, and other analytics applications access LDW data and views by using the Azure Synapse workspace serverless SQL endpoint.

##  Table of Contents
1. [Project Overview](#introduction)
2. [Project Architecture](#project-architecture)
3. [Resources](#Resources)
4. [LDW Details](#Details)
5. 
<a name="introduction"></a>
## Project Overview 
This project attempts the use case to 
1. Build a Serverless/Logical Data Warehouse using **Azure Synapse Analytics** that allows creation of relational database objects like tables and views over collections of data files that represent logical entities to store the data in **Azure Data Lake** that can be used to read data from Delimited text files(CSV). Then using **CETAS (Create External Table as Select)** write back to the data lakehouse to save the CSV data with a **Parquet file** This Azure Synapse workspace created includes an on-demand SQL endpoint. The endpoint lets SQL Server administrators and developers use familiar environments to work with LDWs that Azure Synapse serverless SQL pools define.
2. Showcase Incremental Fact Loading and Slowly Changing Dimensions.
3. Serve Data layer for BI - using serveless SQL endpoint connect to Power BI to showcase the analytical queries
4. Ad-hoc exploration of raw data in a data lake using LDW tables and views.
   

<a name="project-architecture"></a>
## Project Architecture

Below diagram displays the design and details of the logical data warehouse architecture :

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/ServerlessDWArchitecture.png" width="850" height="500"> 

<a name="Resources"></a>
## Resources
Using a set of tables from the **WideWorldImporters** example database which has been exported to CSV format. The main tables are Sales Order and Sales Order Lines with related tables including Items, Customers and Suppliers. The link to the dataset can be downloaded from [this link](https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Data/Source%20Data.zip)

Attempted to apply the [best practices](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/best-practices-serverless-sql-pool) recommended by Microsoft for Serverless SQL Pools.

<a name="Details"></a>
## LDW Details
