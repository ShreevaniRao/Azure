## **ADF Pipelines**

Below is the list of Azure Data Factory (ADF) pipelines developed, categorized by their functionality and stored under respective folders:

1. **Pipeline to Ingest Data Using API**  
   - Ingests data from APIs into Azure Data Lake Storage using ADF. Includes handling for pagination and authentication mechanisms.

2. **Pipeline to Copy Selected Files with Transformations**  
   - Copies specific files from Azure Blob Storage to other destinations, applying transformation rules (e.g., column mapping or format conversion) during the process.

3. **Pipeline to Copy Selected Files Using Storage Event Trigger**  
   - Executes automatically when new files are uploaded to Azure Blob Storage by leveraging **event triggers**.

4. **Pipeline Using Set Variable**  
   - Demonstrates dynamic pipeline behavior by using variables to parameterize and control activities within ADF.

5. **Pipeline Orchestration**  
   - Orchestrates multiple dependent pipelines, using features like activity chaining, conditional execution, and monitoring.

---

### **How to Explore**
Each pipeline is stored under its respective folder within the ADF directory. Navigate through the repository to dive into the JSON definitions, workflows, and features of these pipelines.

Explore these pipelines to understand how they handle different data engineering scenarios, optimize workflows, and adhere to Azure best practices!

### **What I Learned from ADF Pipelines**:

- Designing efficient pipelines for **complex workflows** using native Azure tools.
- Implementing **parameters and variables** for reusable, modular pipelines.
- Debugging pipelines and handling **error management** effectively.

---
