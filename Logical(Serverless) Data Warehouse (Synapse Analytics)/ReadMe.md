
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
1. Build a Serverless/Logical Data Warehouse using **Azure Synapse Analytics** that allows creation of relational database objects like tables and views over collections of data files that represent logical entities to store the data in **Azure Data Lake** that can be used to read data from Delimited text files(CSV).
2. Use **CETAS (Create External Table as Select)** to write back to the data lake to save the CSV data as a **Parquet file**
3. Create Dimensional Modelling and STAR Schema
4. Showcase Incremental Fact Loading and Slowly Changing Dimensions.
5. Serve Data layer for BI - using serveless SQL endpoint connect to Power BI to showcase the analytical queries
6. Ad-hoc exploration of raw data in a data lake using LDW tables and views.
   

<a name="project-architecture"></a>
## Project Architecture

Below diagram displays the design and details of the logical data warehouse architecture :

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/ServerlessDWArchitecture.png" width="850" height="500"> 

<a name="Resources"></a>
## Resources
Using a set of tables from the **WideWorldImporters** example database which has been exported to CSV format. The main tables are Sales Order and Sales Order Lines with related tables including Items, Customers and Suppliers. The link to the dataset can be downloaded from [this link](https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Data/Source%20Data.zip)

Attempted to apply the [best practices](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/best-practices-serverless-sql-pool) recommended by Microsoft for Serverless SQL Pools.

[Study Azure Synapse Serverless SQL pool](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/on-demand-workspace-overview)


<a name="Details"></a>
## LDW Details

1.  Azure Synapse Analytics Workspace setup - create the resource group, storage container and Synapse Analytics studio
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/CreaterResource%26Services.png" width="950" height="500"> 

   From the Synapse studio, click the Develop tab and create a new SQL script.
  <img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/SynapseCreateDW.png" width="950" height="450"> 

2. Setup security - The user account which is being used in the Synapse Studio will need to be added to the Azure Storage Access Control (IAM) as a **Storage Blob Data Contributor**. to be able to read and write to the storage account.
   
3. Create Views in the Serverless SQL database to enable querying of the source data using **OPENROWSET** function The OPENROWSET(BULK...) function allows to access files in Azure Storage to read contents of a remote data source (for example file) and returns the content as a set of rows. Serverless SQL Pools includes 2 SQL functions, [**Filepath**](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/best-practices-serverless-sql-pool#use-filename-and-filepath-functions-to-target-specific-partitions) and [**Filename**](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/best-practices-serverless-sql-pool#use-filename-and-filepath-functions-to-target-specific-partitions), that can be used to return the folder path/name and file name from the data in the source Azure storage account. These 2 functions can also be used to filter on certain folders and files in the data lake to reduce the amount of data processed and also to improve read performance. This leads to saving both time and money(You need to pay for executed queries and the pricing varies based on the amount of data processed by each query).

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/CreateViewWithFilePath.png" width="950" height="550"> 

Create views with different ways to define the column definition using OPENROWSET....
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/CreateViewsWithColumnNames.jpg" width="950" height="750"> 

4. We can now ad-hoc explore the source data by querying the views for useful data agregations, use Filepath function to scan only the required folder(reduces the amount of data scanned), and moreover create complex views using the base views in the LDW to denormalize and query.
   
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/BasicQueriesUsingLoadedTablesFromCSVFilespng.png" width="950" height="750"> 
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/ComplexViewsWithBaseViews.jpg" width="1150" height="650">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/Ad-hocqueryusingcomplexviews.png" width="1150" height="350">

5. Write back to the data lake by reading the CSV files and saving them as **Parquet Files** using **CETAS (Create External Table As Select)**
6. Parquet is an open source, column-oriented data file format designed for efficient data storage and retrieval. It provides efficient data compression and encoding schemes with enhanced performance to handle complex data in bulk. It supports predicate pushdown which is used to filter data at the data source(as early as possible), reducing the amount of data transmitted and processed. As Parquet improves performance in terms of reading file-based data from data lakes and also reduces the amount of data stored and processed, it is a preferable format for data analytics projects.

7. Use CETAS to transform the data of the entities by creating a **Dimensional Model with STAR Schema** and store the select query as a table in the external storage. The data in the LDW is organized and segregated as Facts and Dimensions - with FACT table in the center having foreign keys to all the Dimension tables.
The Fact table stores data which is usually aggregated/rolled up using the Foreign keys of the multiple Dimension tables which stores the data for which we need to report the queries for.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/CETASDiagram.png" width="1150" height="450">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/STARSchema.png" width="1150" height="450">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/StarSchemaUses.png" width="1150" height="550">


8. Using CETAS to write source data as Parquet file to a destination folder for Dimensions tables for Customers, Suppliers, StockItems, Date. 
The load writes the data out to a sub-folder \01\ in each dimension (except the Date dimension) as this is the initial load. Future loads will populate a sequence of sub-folders.
Ued ROW_NUMBER() to generate a **Surrogate key** as type Integer.
A ValidFromDate of 2021-01-01 is used as this is the start of our Sales data.
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/CETASToTransformDataForStarSchemaTables.png" width="1150" height="650">

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/TransformedCETASForDimCustomer.png" width="950" height="550">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/StorageContainerForDimensions.png" width="950" height="650">

Created views for the Dimensions using the parquet file data.
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/TransformViewsWithParquetData.png" width="950" height="650">

9. Using CETAS to write source data as Parquet file to a destination folder for Fact table using Sales Orders & Sales Orderline Details .
    <img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/LoadInitialFactSalesTableWithTransformation.png" width="950" height="750">
