## Pipeline Summary

The `pl_show_storage_event_trigger` pipeline, coupled with the **Blob Event Trigger**, automates the process of handling files uploaded to Azure Blob Storage. It focuses on identifying filenames prefixed with **"Fact"**, moving them to a destination container, and cleaning up the source location. This setup demonstrates how ADF pipelines can react to real-time storage events, showcasing a robust event-driven architecture.

---

## Key Features

- **Event-Driven Automation**:
  - The pipeline is initiated by a **Blob Event Trigger** when a new file matching the criteria is uploaded to the source.
- **Conditional Processing**:
  - Filters files with names starting with **"Fact"** using metadata-based checks.
- **Iterative Handling**:
  - Loops through identified files to process them dynamically.
- **Efficient Data Management**:
  - Copies processed files to a destination and deletes the source files to optimize storage use.
- **Comprehensive Variables Usage**:
  - Demonstrates the use of variables for dynamic configuration and runtime flexibility.

---

## Trigger Details

### Blob Event Trigger: `tr_storage_event_copy_selected_files`
- **Description**: Triggers the pipeline when a file is created in the specified source folder.
- **Scope**: 
  - Monitors the Blob container for changes in the path: `/source/blobs/csvfiles/`.
- **Event Type**: 
  - Listens for the **Microsoft.Storage.BlobCreated** event to initiate the pipeline.
- **Properties**:
  - **Ignore Empty Blobs**: Enabled to avoid triggering on empty blob creations.
  - **Linked Storage Account**: `dp203test`, associated with the specified resource group and subscription.

---

 ## Pipeline Steps and Activities - `pl_show_storage_event_trigger`

### 1. **Trigger Initialization**
   - **Trigger**: `tr_storage_event_copy_selected_files`
   - **Purpose**: Activates the pipeline upon detecting new uploads in the source folder.
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20to%20Copy%20selected%20files%20using%20Storage%20Event%20Trigger/TriggerForStorageEvent.jpg" width = 850, height = 500>

### 2. **Extract Metadata from Source Folder**
   - **Activity**: `ac_getmetadata_adlsg2_source`
   - **Purpose**: Fetches the list of files from the source folder for processing.
   - **Configuration**:
     - Dataset: `ds_source_api_meta`.
     - Retrieves the **childItems** of the specified path.

### 3. **Iterate Over Metadata Entries**
   - **Activity**: `ac_foreach_metadata_file`
   - **Purpose**: Loops through the metadata entries from the previous step.
   - **Key Configuration**:
     - Source Expression: `@activity('ac_getmetadata_adlsg2_source').output.childItems`

### 4. **Conditional File Selection**
   - **Activity**: `ac_if_foreach_item_select`
   - **Purpose**: Processes files with names beginning with **"Fact"**.
   - **Expression**: `@startswith(item().name, 'Fact')`

### 5. **Copy Selected Files**
   - **Activity**: `ac_copy_selected_item`
   - **Purpose**: Transfers filtered files to a destination container.
   - **Configuration**:
     - Source Dataset: `ds_parameterized_source` (Dynamic file resolution).
     - Destination Dataset: `ds_reporting`.
     - Transformation:
       - Ensures all text is quoted.
       - Sets file extension to `.txt`.

### 6. **Delete Source Files**
   - **Activity**: `ac_delete_copied_files`
   - **Purpose**: Removes successfully copied files from the source container.
   - **Key Configuration**:
     - Enables logging for deletion activities.
     - Logs stored in the `HttpAzureDataLakeStorage` linked service.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20to%20Copy%20selected%20files%20using%20Storage%20Event%20Trigger/PipelineWithStorageEventTrigger.jpg" width="850" height="500">
---

## List of Datasets and Their Usage

1. **`ds_source_api_meta`**:
   - **Purpose**: Used for fetching metadata and deleting files.
   - **Type**: Azure Blob File System.
   - **Path**: Points to the source folder containing input files.

2. **`ds_parameterized_source`**:
   - **Purpose**: Dynamically references files during the processing loop.
   - **Type**: Parameterized Azure Blob dataset.

3. **`ds_reporting`**:
   - **Purpose**: Destination for the processed files.
   - **Type**: Azure Blob File System.

---

## Conclusion

The `pl_show_storage_event_trigger` pipeline, integrated with a Blob Event Trigger (`tr_storage_event_copy_selected_files`), provides a scalable, event-driven file-processing workflow. This solution handles files uploaded to Azure Blob Storage efficiently by combining event detection, metadata-based processing, and structured data movement. The deletion of source files post-processing ensures clean storage management, showcasing real-world use cases of ADF pipelines for automation.

