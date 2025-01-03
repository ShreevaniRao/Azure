# Azure Data Factory Project: Pipeline Orchestration

This project demonstrates my ability to design, orchestrate, and manage data workflows using ADF pipelines. Below is an overview of the pipeline logic and skills applied in this project.

## Overview

This project uses Azure Data Factory to orchestrate multiple activities and workflows by executing one pipeline after another with dependencies and parameter passing. The following pipeline setup is implemented:

- **Pipeline 1**: Executes another pipeline (`pl_set_variable`) that sets some necessary variables.
- **Pipeline 2**: Dependent on the success of **Pipeline 1**, it executes a pipeline (`pl_copy_csv_files`) that performs specific actions such as copying CSV files and passing parameters from the previous pipeline.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20Orchestration/ExecutePipelinesActivityOutput.jpg" width=850 height=500>

## Pipeline Architecture

The ADF pipeline orchestration demonstrates:

### 1. **Execute Pipeline 1**
- **Type**: ExecutePipeline
- **Dependency**: No dependencies. This pipeline runs independently.
- **Description**: Runs the `pl_set_variable` pipeline, which is responsible for initializing and setting any necessary variables for subsequent workflows.
- **Key Features**:
  - Wait for completion.
  - No input parameters or complex configurations for the execution stage.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20Orchestration/ParentPipelineWithSetVarActivity.jpg" width=850 height=500>

### 2. **Execute Pipeline 2**
- **Type**: ExecutePipeline
- **Dependency**: Depends on the successful execution of **Pipeline 1** (via `Succeeded` dependency condition).
- **Description**: Runs the `pl_copy_csv_files` pipeline, responsible for copying CSV files, and passes necessary parameters (e.g., `pl_relativeurl`) from **Pipeline 1**'s output to this activity.
- **Key Features**:
  - Wait for completion.
  - Utilizes **dependency management** to trigger only upon successful execution of the preceding pipeline.
  - Dynamic **parameter passing** from output values (`@activity('Execute Pipeline1').output.pipelineReturnValue.pl_relativeurl`).

### 3. **Dynamic Parameter Passing**
- Parameter `pl_relativeurl` is dynamically passed from **Pipeline 1** to **Pipeline 2** using:
  ```json
  "@activity('Execute Pipeline1').output.pipelineReturnValue.pl_relativeurl"

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20Orchestration/ExecutePipelineActivityWithChildPipeline.jpg" width=900 height=500>

