# Azure Data Factory Pipeline overview - pl_prod

This project demonstrates my ability to design, orchestrate, and manage data workflows using ADF pipelines. Below is an overview of the pipeline logic and skills applied in this project.

## Overview

This project uses Azure Data Factory to orchestrate multiple activities and workflows by executing one pipeline after another with dependencies and parameter passing. The following pipeline setup is implemented:

- **Pipeline 1**: Executes another pipeline (`pl_set_variable`) that sets some necessary variables.
- **Pipeline 2**: Dependent on the success of **Pipeline 1**, it executes a pipeline (`pl_copy_csv_files`) that performs specific actions such as copying CSV files and passing parameters from the previous pipeline.

## Key Skills Highlighted
This project highlights a range of key skills in Azure Data Factory and pipeline orchestration:

- Pipeline Orchestration: Managing complex workflows by sequencing and controlling the execution of multiple dependent pipelines.
- Data Transformation and Movement: Orchestrating the movement and transformation of data, particularly related to file copying tasks in Azure Data Factory.
- Error Handling and Dependency Management: Setting conditional dependencies between activities to ensure that workflows execute in the correct sequence and only proceed if the previous activity is successful.
- Parameterization: Using dynamic expression-based parameters and referencing outputs from other activities within the same pipeline.
- Monitoring and Management: Using ADF’s monitoring capabilities to track and manage pipeline executions, handling errors, and ensuring smooth execution.

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
  - 
<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20Orchestration/DependentPipelineForExecutePipeline.jpg" width=900 height=500>

### 3. **Dynamic Parameter Passing**
- Parameter `pl_relativeurl` is dynamically passed from **Pipeline 1** to **Pipeline 2** using:
  ```json
  "@activity('Execute Pipeline1').output.pipelineReturnValue.pl_relativeurl"

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20Orchestration/ExecutePipelineActivityWithChildPipeline.jpg" width=900 height=500>

## Summary

This pipeline demonstrates advanced Azure Data Factory orchestration capabilities, showcasing:

- **Dependable Sequencing**: Pipelines are designed with clear dependencies, ensuring seamless execution and minimal errors.
- **Dynamic Parameterization**: Outputs from preceding pipelines dynamically inform subsequent pipeline parameters, enabling flexible and reusable workflows.
- **Robust Automation**: Automated copying of data (e.g., CSV files) between Azure resources simplifies and streamlines data engineering tasks.
- **Real-World Problem-Solving**: Reflects a practical solution for modular and efficient pipeline management in large-scale data projects.

By leveraging conditional dependencies, parameter passing, and modular design, this pipeline effectively handles complex workflows, highlighting my expertise in orchestrating end-to-end data pipelines in Azure Data Factory.
