# **Azure Data Factory Pipeline: Copy and Transform Selected Files Using Metadata**

## **Pipeline Summary**
This Azure Data Factory pipeline demonstrates how to 
- Filter specific files from a source folder using metadata,
- Copy them to a destination folder,
- Transform the copied files.
- It highlights advanced capabilities like dynamic file handling, metadata-driven workflows, and flexible transformations, making it ideal for scalable data engineering scenarios.

---

## **Key Features**
1. **Metadata Activity (`GetMetadata`)**:
   - Extracts detailed file information from the source folder.
   - Enables dynamic processing of files based on their properties.

2. **ForEach Activity**:
   - Iterates through metadata to process individual files.
   - Handles file-specific logic dynamically.

3. **Conditional Logic (`IfCondition`)**:
   - Filters files based on naming patterns (e.g., files starting with string `Fact`).

4. **Copy Activity (`Copy`)**:
   - Copies filtered files from the source to the destination folder dynamically.
   - Allows parameterized dataset handling.

5. **Data Flow Transformation (`ExecuteDataFlow`)**:
   - Applies custom transformations to the processed files.
   - Leverages Azure Data Flow for efficient transformation at scale.

     

---

## **Pipeline Steps to Recreate**

### **1. Metadata Retrieval**
- **Activity**: `GetMetadata`
- **Purpose**: Retrieve a list of files from the source folder.
- **Configuration**:
  - Reference the dataset (`ds_source_api_meta`) pointing to the source folder.
  - Extract the `childItems` property to fetch file details.
- **Output**: A list of files available for processing.

### **2. Iterate Through Metadata**
- **Activity**: `ForEach`
- **Purpose**: Loop through the metadata output for file-by-file processing.
- **Configuration**:
  - Set the `items` property to:
    ```json
    "@activity('ac_getmetadata_adlsg2_source').output.childItems"
    ```
  - Enable sequential execution to process one file at a time.

#### **Inside `ForEach`**
1. **Filter Files**
   - **Activity**: `IfCondition`
   - **Purpose**: Check if the file name starts with `Fact`.
   - **Condition Expression**:
     ```json
     "@startswith(item().name, 'Fact')"
     ```

2. **Copy Filtered Files**
   - **Activity**: `Copy`
   - **Purpose**: Copy files meeting the condition to the destination folder.
   - **Configuration**:
     - Source: `ds_parameterized_source` with the file name set dynamically:
       ```json
       "filename": "@item().name"
       ```
     - Sink: `ds_reporting` for the destination folder.

---

### **3. Transform Copied Files**
- **Activity**: `ExecuteDataFlow`
- **Purpose**: Perform transformations on the copied files in the destination folder.
- **Configuration**:
  - Reference the Data Flow (`df_transform_data`) for the transformation logic.
  - Set compute properties:
    - **Core Count**: 8
    - **Compute Type**: General
  - Define dependencies to ensure execution only after successful file copy.

---

## **Fork and Deploy Instructions**
Follow these steps to set up and use the pipeline from this repository:

1. **Set Up Datasets**:
   - Create and configure datasets (`ds_source_api_meta`, `ds_parameterized_source`, `ds_reporting`) in Azure Data Factory:
     - **Source Dataset**: Fetch file metadata.
     - **Parameterized Dataset**: Use for dynamic file reading.
     - **Sink Dataset**: Point to the destination folder.

2. **Deploy the Data Flow**:
   - Import the `df_transform_data` file from the repository and customize it for your transformation needs.

3. **Recreate Activities**:
   - Use the pipeline steps provided to define activities and their relationships.

4. **Run the Pipeline**:
   - Trigger the pipeline execution and monitor activity progress in the Azure portal.
