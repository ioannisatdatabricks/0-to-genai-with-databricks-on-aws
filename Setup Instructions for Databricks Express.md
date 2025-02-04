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

    Assuming dbdemos version 0.6.8:
    - update the version of the **mlflow-skinny**, **mlflow**, and **mlflow[gateway]** packages to **2.20.1**.
    - add **bs4** in the list of packages to be pip-installed.
   
    After these changes the cell should like like this:

    `%pip install -U --quiet databricks-sdk==0.40.0 databricks-agents==0.15.0 mlflow-skinny==2.20.1 mlflow==2.20.1 mlflow[gateway]==2.20.1 databricks-vectorsearch langchain==0.2.1 langchain_core==0.2.5 langchain_community==0.2.4 bs4`

    `dbutils.library.restartPython()`
