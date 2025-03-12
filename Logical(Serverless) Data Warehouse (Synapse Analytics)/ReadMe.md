
<div align="center">
  <div id="user-content-toc">
    <ul>
      <summary><h1 style="display: inline-block;"> Azure Logical/Serverless Data Warehouse - Synapse Analytics </h1></summary>
    </ul>
  </div>
</div>

<div align="left">
  
### The logical data warehouse (LDW) pattern lays a lightweight virtualized relational layer on top of data that's stored in a data lake or database. This virtualization layer provides data warehouse access without requiring data movement. This solution can combine online transaction processing (OLTP) data with analytical data from data lakes for a low-complexity, low-latency way to serve business intelligence (BI) and analytics workloads.
### Azure Synapse serverless SQL pools define an LDW that has logical tables and views accessible through the Azure Synapse workspace serverless SQL pool on-demand endpoint. It uses a pay-per-query costing model where you pay for the compute per TB of data processed while executing the query and not for the minimum reserved resources for the compute(dedicated SQL pool). You just pay for the storage of the data.
### Reporting, BI, and other analytics applications access LDW data and views by using the Azure Synapse workspace serverless SQL endpoint for a quick data exploration of the data in the data lake by avoiding time consuming ETL processes alongwith the benefit of familiar T-SQL code.

##  Table of Contents
1. [Project Overview](#introduction)
2. [Project Architecture](#project-architecture)
3. [Resources](#Resources)
4. [Logical DataWarehouse Details](#Details)
   
<a name="introduction"></a>
## Project Overview 
This project attempts to address the use case to 
1. Build a Serverless/Logical Data Warehouse using **Azure Synapse Analytics** that allows creation of relational database objects like tables and views over collections of data files that represent logical entities to store the data in **Azure Data Lake** that can be used to read data from Delimited text files(CSV).
2. Use **CETAS (Create External Table as Select)** to write back to the data lake to save the CSV data as a **Parquet file**
3. Create **Dimensional Modelling and STAR Schema**
4. Showcase **Incremental Fact Loading and Slowly Changing Dimensions**.
5. Serve Data layer for BI - using serveless SQL endpoint connect to Power BI to showcase the analytical queries
6. Ad-hoc exploration of raw data in a data lake using LDW tables and views.
7. Demonstrate the usage of SQL monitoring to guage the data processing using Power BI Date filters with **filepath()**
   

<a name="project-architecture"></a>
## Project Architecture

Below diagram displays the design and details of the logical data warehouse architecture :

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/ServerlessDWArchitecture.png" width="850" height="500"> 

<a name="Resources"></a>
## Resources
* Using a set of tables from the **WideWorldImporters** example database which has been exported to CSV format and uploaded to the storage container. The main tables are Sales Order and Sales Order Lines with related tables including Items, Customers and Suppliers. The link to the dataset can be downloaded from [this link](https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Data/Source%20Data.zip)

* Attempted to apply the [best practices](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/best-practices-serverless-sql-pool) recommended by Microsoft for Serverless SQL Pools.

* [Study Azure Synapse Serverless SQL pool](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/on-demand-workspace-overview)


<a name="Details"></a>
## Logical DataWarehouse Details

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

7. Use CETAS to transform & enhance the data of the entities by creating a **Dimensional Model with STAR Schema** and store the select query as a table in the external storage. The data in the LDW is organized and segregated as Facts and Dimensions - with FACT table in the center having foreign keys to all the Dimension tables creating a star shape.
The Fact table stores data which is usually aggregated/rolled up using the Foreign keys of the multiple Dimension tables which stores the data of the entities for which we need to report the aggregates/rollup (e.g customers, suppliers etc).

The below diagrams details the STAR schema and its uses in the data warehouse.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/CETASDiagram.png" width="1150" height="450">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/STARSchema.png" width="1150" height="450">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/StarSchemaUses.png" width="750" height="300">


8. Using CETAS to write source data as Parquet file to a destination folder for Dimensions tables for Customers, Suppliers, StockItems, Date. 
The load writes the data out to a sub-folder \01\ in each dimension (except the Date dimension) as this is the initial load. Future loads will populate a sequence of sub-folders.
Used ROW_NUMBER() to generate a **Surrogate key** as type Integer.
A ValidFromDate of 2021-01-01 is used as this is the start of our Sales data.
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/CETASToTransformDataForStarSchemaTables.png" width="1150" height="650">

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/TransformedCETASForDimCustomer.png" width="950" height="550">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/StorageContainerForDimensions.png" width="950" height="650">

Created views for the Dimensions using the parquet file data.
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/TransformViewsWithParquetData.png" width="950" height="650">

9. Using CETAS to write source data as Parquet file to a destination folder for Fact table using Sales Orders & Sales Orderline Details and its corresponding view.
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/LoadInitialFactSalesTableWithTransformation.png" width="950" height="750">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/CreateViewsForStarSchemaTables.png" width="950" height="650">

10. Analyse with queries using the transformed views of Parquet data showcasing easy joins and relationship with Fact & Dimension views to aggregate the Fact table aggregation Details.
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/QueriesUsingTransformedViews.png" width="950" height="650">

11. After initial load in the data lake, over a period of time, to address loading new and changed data of the Dimensions & Facts table details in the data warehouse, will be addressed with the below details.
* For Dimensions this will be handled by **Type 2 SCD(Slowly Changing Dimension)** , and for
* Facts details like Sales Order and SalesOrderline details - incremental loading can be tracked.
* For Dimensions - Will track an update in the Supplier Category for a Supplier, while keeping the old existing data for historical purposes. 
* A new Supplier added will also be dealt by updating the Supplier table with a new record.
* The new Supplier CSV files were uploaded to 'datalakehouse/ChangedData/2021-06-22(YYYY-MM-DD)/Purchasing_Suppliers' path.
* Will uplolad new Sales Orders and Sales Order Lines CSV files for 2 days (2021-04-18 & 2021-04-19)
* The Sales data gets uploaded in the following new folders. YYYY-MM-DD must be replaced with the date of the data.
  transformed/facts/factsales/YYYY-MM-DD/
  

Start by manually loading one of the CSV file of Sales data in the location parameter in the CETAS and by using the FilePathDate colmn in the source view to select only the data that needs to be loaded. The FilePathDate column in the View is the result of the filepath() function which can be used as a filter to only select/scan the requested folder. This reduces the amount of data processed as only the required folder and therefore data within the folder is scanned. 
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/SalesFactIncrementalLoad.png" width="950" height="650">


If we had multiple data files for increments, can use the dynamic stored procedure to process them in a loop.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/Stor_ProcForFactSalespng.png" width="950" height="650">

### Slowly Changing Dimension
Serverless SQL Pools do not support updating data in the Data Lake, it is an append-only process in that files can be added to the underlying storage but we cannot run SQL to change existing data. However, we can load new and changed dimension data into new destination folders under the root dimension folder.

The SQL code below will create a View which targets selecting changed data for Suppliers.
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/CreateViewForIncrementalChangeSuppliers.png" width="950" height="450">

The SQL code below writes the new and changed data out to a sub-folder /02 in the current Supplier dimension folder. First select the maximum surrogate key from the current dimension data and use this to continue the sequence when writing the changed and new data. Within the CSV file is a date column which indicates when the source data changed, we can use this as our ValidFrom value.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/CETASForSCD-PurchaseSupplierChanges.png" width="950" height="450">

If we now query the existing view to select data from the Supplier dimension, we get all the existing data, the changed data, and the new data. However, we are missing vital columns which are required to flag the date range validity of a dimension row.The query result shows that SupplierID 5 has changed Supplier Category.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/QuerySCDChangesSupplier.png" width="950" height="450">

To complete the [Type 2 SCD](https://learn.microsoft.com/en-us/data-engineering/playbook/articles/scd-using-change-data-feed#choose-methods-to-track-scd-type-2) the single ValidFrom date to calculate the ValidTo and also calculate the ActiveMember flag for each dimension row. We use the **LEAD** function and partition by the SupplierID (source system business key) to generate contiguous date ranges. Please note that we can also use datetime values and change the DATEADD accordingly. This below new view completes the SCD Type 2 Dimension.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/SCDViewForSupplierDim.png" width="850" height="400">

Querying from the new Dimension View, able to see date ranges and which row is the current active member.
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/QuerySupplierDimSCDChanges.png" width="850" height="400">

Now, it would be more accurate to create the Sales Facts external table using this new view with the updated supplier details using the updated stored procedure as below
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/Stored_Proc_Sales_Facts_withSCD_Suppllier.png" width="950" height="450">


12. Finally using  PowerBI to connect to these Serverless dimensional Warehouse for reporting and analytical purposes. Created a simple date visualization to display the use of the Date dimension to filter the Sales aggregations for the selected dates by showing Sales Order Quantity by Month Name, to demonstrate the partition prune and therefore reduced data processed.

13. Create a copy of the Dim Date object as Dim Date Filter and used this as the filter whilst keeping the original Dim Date as a chart axis in the data visualisation and we see data processed in the Sql Monitor to guage the data processed.
14. Conclude that if Power BI passes the date filters using **IN** then Serverless SQL Pools will successfully use the filepath() filter and data processed is reduced.
15. First we connect to the Serverless warehouse using **Serverless SQL endpoint** by specifying the the database name - **sqllogicaldw** ensuring **DirectoQuery** connectivity mode.
16. Establish the data modeling by making sure the relationships are set.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/PBIModelling.png" width="950" height="450">

Create Report and Test Date Filters
* Click File > Options & Settings > Options then under Current File > Query Reduction > Filters select Add a single Apply button to the filter pane to apply changes at once then click OK
 Click on the Report icon to switch the view to the canvas.
 Select the DimDate.MonthName column and in the Column tools menu at the top, select Sort By Column > Month (this will sort the names of the Month by the Month number to get the correct order).
* Drag the FactSales.SalesOrderQuantity column onto the canvas to create simple column chart visualisation, this will now trigger a query on the Serverless SQL Pool to return the SUM of this column.
* Drag the DimDate.MonthName column onto the column chart to add the Month name as the axis.
* Expand the Filters pane on the right and drag the DimDate.Year and DimDate.Month columns into the filters and change the filter type to Basic filtering.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/PBIVIz.png" width="950" height="450">

17. Check SQL Syntax from Power BI
Let’s check the SQL that has been run on the Serverless SQL Pools database. We do this in Synapse Studio by clicking Monitor > SQL Requests

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/SQLRequestsFromPBI.png" width="950" height="550">
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/SQLCodeGeneratedPBI.png" width="950" height="750">

If we now use the Year and Month filters to specify a particular month, in this case we’ll select 2021 and 4. This is the SQL that is sent from Power BI, as you can see there is a JOIN between the Fact Sales and the Dim Date views then a WHERE filter on the Dim Date view.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/PBISQLWIthDateFilter.png" width="950" height="800">

**Changing the Power BI Data Model to Composite**
If we set the Dim Date table to **Import** mode whilst keeping the Fact Sales table as DirectQuery, then the SQL query passed to Serverless SQL Pools will still use JOIN.

However, if we then remove the Month Name from the data visualisation, we now see IN being used to filter dates which will successfully filter only on the required source folders and we see data processed reduced.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Logical(Serverless)%20Data%20Warehouse%20(Synapse%20Analytics)/Assets/PBISqlCodeDateWithINClause.png" width="1150" height="1000">

18. Summarsing the fndings - If we expose the **filepath()** function in a View to return the YYYY-MM-DD value, we can then use this to filter the source folders and reduce data processed. However, to invoke this from Power BI we need to set the Date dimension as **Import** and only use this as a filter. This will send the list of dates as an **IN** filter. However for big date ranges this too might create a big SQL statement, to cater this situation we might want to breakdown the **SalesOrderPathDate** column in FactSales into 4 columns for MOnth, Year, Quarter & Day by applying transformation to this column with duplication and extracting month, quarter, day & year.
