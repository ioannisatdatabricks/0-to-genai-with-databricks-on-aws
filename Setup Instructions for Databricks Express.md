# 0 to GenAI with Databricks and AWS
## Setup instructions for Databricks Express workspaces

### 1. Install the demo content
- Create a new notebook and name it, for example, "Content Setup"
- Add the following cells and run the notebook:
  - **cell 1**

    `%pip install -U dbdemos`
  
    `%restart_python`
    
  - **cell 2**

    `import dbdemos`
  
    `dbdemos.list_demos()`

  - **cell 3**

    `dbdemos.install('llm-rag-chatbot')`
  
###  2. Patch the demo notebook
- Go to your home folder in the workspace and enter the folder **llm-rag-chatbot/01-first-step**
- Open the notebook **01-First-Step-RAG-On-Databricks**
- Perform the following edits:
  - **cell 2**
    
    update the version of the **mlflow-skinny**, **mlflow**, and **mlflow[gateway]** packages to **2.20.0rc0**.

  - **cell 23**

    add one more argument in the `mlflow.langchain.log_model` call:

    `pip_requirements=["mlflow", "cloudpickle", "databricks-connect", "databricks-vectorsearch", "ipykernel", "langchain-community", "langchain", "numpy", "pandas", "pyarrow", "pydantic", "pyspark"]`
