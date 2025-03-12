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

    Upon successful installation in the notebook output, there should be a link to the notebook **01-first-step/01-First-Step-RAG-On-Databricks**. That will be the main notebook to work with.
  
### 2. Create model serving endpoints to Bedrock
For the below it is assumed that every user has access to an AWS account where an IAM user with Bedrock access privileges is defined and the Anthropic Claude Sonnet and Amazon Titan models have been enabled.

- **a** Using the UI create an external model serving endpoint for the embeddings. Select Bedrock as external serving provider, Amazon Titan as the model for the embeddings and the credentials of the IAM user with the Bedrock access privileges
- **b** Repeat for the chat model (use Claude Sonnet)

### 3. Update the notebook
- Navigate to the **01-first-step** folder and open the **01-First-Step-RAG-On-Databricks**
- Replace the LLMs used for the embeddings and chat:
  - **cell 8**

    define the model to be used for the embeddings (it should be the name of the endpoint created in step 2a):

    `embedding_model_endpoint_name=<Endpoint Serving Name for Embeddings> #The embedding endpoint used to create the embeddings`

  - **cell 13**
 
    define the model to be used for the chat (it should be the name of the endpoint created in step 2b):

    `"llm_model_serving_endpoint_name": "bedrock_chat",  # the foundation model we want to use`
