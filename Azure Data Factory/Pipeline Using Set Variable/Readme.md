# Azure Data Factory Pipeline Overview: `pl_set_variable`

## Summary

The `pl_set_variable` pipeline demonstrates the usage of the **Set Variable** activity to manipulate and store pipeline parameters dynamically. Specifically, it is designed to extract and process information from an input URL (pipeline parameter `relativeurl`) to isolate the relevant filename. This pipeline is intended to be invoked by another parent pipeline using the **Execute Pipeline** activity, showcasing a modular and reusable pipeline architecture.

---

## Key Features

1. **Dynamic Parameter Handling**:
   - Accepts an API URL as a pipeline parameter (`relativeurl`) to process dynamically.
2. **Conditional Logic**:
   - Uses an **IfCondition** activity to evaluate whether the URL ends with `.csv`.
3. **Variable Setting**:
   - Sets the variable `pipelineReturnValue` to store the extracted URL, which can be passed to subsequent activities or pipelines.
4. **Reusability**:
   - Can be executed by a parent pipeline, allowing for seamless integration into larger workflows.

---

## Pipeline Details

### Parameters
- **`relativeurl`**:
  - **Type**: String
  - **Default Value**:  
    `ShreevaniRao/Azure/refs/heads/main/Azure%20Data%20Factory/Fact_Sales_1.csv`  
  - **Purpose**: Represents an API URL passed to the pipeline for processing.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20Using%20Set%20Variable/SetVariableWithPipelineParameter.jpg" width="850" height="500">

---

### Activities

1. **If Condition: `If Condition1`**
   - **Type**: IfCondition
   - **Expression**: `@endswith(pipeline().parameters.relativeurl, '.csv')`
   - **Purpose**: Checks if the `relativeurl` parameter ends with `.csv`.

2. **Set Variable: `Set variable1`**
   - **Type**: SetVariable
   - **Triggered When**: Condition in `If Condition1` evaluates to **True**.
   - **Variable Name**: `pipelineReturnValue`
   - **Value Set**:
     - Key: `pl_relativeurl`
     - Value: Extracted value from the `relativeurl` parameter.
     - Expression: `@pipeline().parameters.relativeurl`
   - **Purpose**: Stores the validated URL as a variable for use in downstream activities.

<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20Using%20Set%20Variable/ParentPipelineWithSetVarActivity.jpg" width="850" height="500">


<img src="https://github.com/ShreevaniRao/Azure/blob/main/Azure%20Data%20Factory/Pipeline%20Using%20Set%20Variable/PipelineWithSetVariable.jpg" width="850" height="500">
---

## Usage Scenarios

1. **Pipeline Modularity**:
   - This pipeline processes URL-based parameters, making it modular and reusable.
   - Can be invoked in a **parent pipeline** using the **Execute Pipeline** activity.
2. **Dynamic File Handling**:
   - Extracts meaningful file information from URLs, enabling dynamic file-based operations in subsequent pipelines.

---

## Conclusion

The `pl_set_variable` pipeline showcases the ability to work dynamically with input parameters using conditional logic and variable manipulation. This modular design makes it an excellent candidate for reusability, as it can be seamlessly integrated into complex workflows, enabling efficient data transformation and parameter passing across pipelines.

