### **Azure Data Factory Pipeline Overview: Copy and Transform Selected Files Using Metadata**

## **Pipeline Summary**
This Azure Data Factory pipeline demonstrates how to 
- Filter specific files from a source folder using metadata,
- Copy them to a destination folder in a data lake folder,
- Transform the copied files and save them to another data lake folder.
- It highlights advanced capabilities like dynamic file handling, metadata-driven workflows, and flexible transformations, making it ideal for scalable data engineering scenarios.

## Key Features
- **Metadata-Based Selection**: Identifies files starting with "Fact" in their names using metadata from the source.
- **ForEach Loop**: Iterates over the identified files to process each individually.
- **Conditional Copy**: Filters files based on a naming convention and copies them to the destination folder.
- **Data Transformation**: Leverages a Data Flow activity to apply custom transformations to the copied files.
- **Automated Scheduling**: A Scheduled Trigger executes the pipeline at one-minute intervals during a defined period.
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20to%20Copy%20selected%20files%20with%20Transformations/CopySelectedFileusingPipelineRun.jpg" width="950" height="450"> 
---

## **Pipeline Steps to Recreate**

### **1. Metadata Retrieval**
- **Activity**: `GetMetadata`
- **Purpose**: Retrieve a list of files from the source folder.
- **Configuration**:
  - Reference the dataset (`ds_source_api_meta`) pointing to the source folder.
  - Extract the `childItems` property to fetch file details.
- **Output**: A list of files available for processing.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20to%20Copy%20selected%20files%20with%20Transformations/CopySelectedFilesUsingMetaData.jpg" width="950" height="450"> 

### **2. Iterate Through Metadata**
- **Activity**: `ForEach`
- **Purpose**: Loop through the metadata output for file-by-file processing.
- **Configuration**:
  - Set the `items` property to:
    ```json
    "@activity('ac_getmetadata_adlsg2_source').output.childItems"
    ```
  - Enable sequential execution to process one file at a time.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20to%20Copy%20selected%20files%20with%20Transformations/CopySelectedFileForEachActivity.jpg" width="950" height="450"> 

#### **Inside `ForEach`**
1. **Filter Files**
   - **Activity**: `IfCondition`
   - **Purpose**: Check if the file name starts with `Fact`.
   - **Condition Expression**:
     ```json
     "@startswith(item().name, 'Fact')"
     ```

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20to%20Copy%20selected%20files%20with%20Transformations/CopySelectedFileIFCondition.jpg" width="700" height="450"> 

2. **Copy Filtered Files**
   - **Activity**: `Copy`
   - **Purpose**: Copy files meeting the condition to the destination folder.
   - **Configuration**:
     - Source: `ds_parameterized_source` with the file name set dynamically:
       ```json
       "filename": "@item().name"
       ```
     - Sink: `ds_reporting` for the destination folder.


<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20to%20Copy%20selected%20files%20with%20Transformations/CopySelectedFileusingParameterizedDS-Source.jpg" width="800" height="450"> 

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20to%20Copy%20selected%20files%20with%20Transformations/CopySelectedFileusingParameterizedDS-Sink.jpg" width="800" height="450"> 
---

### **3. Transform Copied Files**
- **Activity**: `ExecuteDataFlow`
- **Purpose**: Perform transformations on the copied files in the destination folder.
- **Configuration**:
  - Reference the Data Flow (`df_transform_data`) for the transformation logic.
  - Define dependencies to ensure execution only after successful file copy.

#### **Transformations in Data Flow**
1. **Data Cleaning**:
   - Handle null values, correct data types, or fix structural issues.
2. **Data Enrichment**:
   - Derive new columns or aggregate existing data for insights.
3. **Restructuring**:
   - Optimize file layouts for downstream analysis (e.g., sorting, partitioning).
4. **Transform Result**:
  - Cleaned and transformed files are written back to the destination folder.
  - 
#### **Sink Configuration in Data Flow**:
- **Datasets Used**: `ds_reporting`
  - Destination: Configured to save transformed data with required format settings (e.g., `.txt` files with quoted text).
- **Settings**:
  - Writes transformed data dynamically for each input file.
  - Ensures all required files have been cleaned and restructured before proceeding.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20to%20Copy%20selected%20files%20with%20Transformations/DataFlowTransformation.jpg" width="900" height="450"> 
---

## **Dataset Details**

1. **`ds_source_api_meta`**:
   - **Purpose**: Fetch metadata for files in the source folder.
   - **Usage**: Referenced in `GetMetadata` activity to retrieve the file list.

2. **`ds_parameterized_source`**:
   - **Purpose**: Dynamically access individual files in the source folder.
   - **Usage**: Used in the `Copy` activity to set the file name dynamically for each iteration.

3. **`ds_reporting`**:
   - **Purpose**: Save copied and transformed files to the destination.
   - **Usage**: Acts as the destination dataset for both `Copy` and `ExecuteDataFlow` activities.

---

## Details of the Trigger: **tr_selectedfiles_with_transformation**

### Trigger Type
The pipeline is orchestrated by a **Scheduled Trigger** to run automatically at regular intervals without manual intervention.

### Usage and Purpose
The Scheduled Trigger enables automatic pipeline execution for streamlined data ingestion and transformation. During the active timeframe (from December 29 to December 31, 2024), it runs every minute, allowing near real-time processing of selective files.

### Trigger Properties:
- **Description**: "Copying to the sink - selected files with some transformations".
- **Recurrence Details**:
  - **Frequency**: Every 1 minute.
  - **Start Time**: `2024-12-29T23:10:00` (Central Standard Time).
  - **End Time**: `2024-12-31T00:00:00` (Central Standard Time).
  - **Time Zone**: `Central Standard Time`.
- **Pipeline Linked**:
  - Pipeline Reference: **pl_copy_select_files_with_metadata**.
    
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20to%20Copy%20selected%20files%20with%20Transformations/PipelineTriggerToCopySelectedFiles.jpg" width=850 height=500>

## **End Results**
- **Files Transformed**:
  - Only files starting with the string `Fact` are copied and transformed.
- **Saved Sink**:
  - The processed files are saved to the destination container or folder in a cleaned and structured format ready for downstream consumption.
  - The output includes meaningful transformations aligned with the requirements.
  - By adding a time-based trigger, the process becomes autonomous, offering regular updates to the data sink.

## **Conclusion**
This Azure Data Factory pipeline uses a metadata-driven approach to filter and copy specific files from a source folder to a destination folder, and subsequently transform the copied data using a Data Flow. This enables efficient file selection, dynamic data handling, and scalable transformations supplemented with an automated Scheduled Trigger.
