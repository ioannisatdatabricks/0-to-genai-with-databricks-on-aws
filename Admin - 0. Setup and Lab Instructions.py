# Databricks notebook source
# MAGIC %md
# MAGIC # Admin Setup and Lab Instructions
# MAGIC
# MAGIC ## 1. Workspace preparation
# MAGIC
# MAGIC ### 1.1 Create a catalog in UC
# MAGIC Using the workspace UI, the workshop admin creates a **workshop** catalog in UC granting `USE_CATALOG` and `CREATE_SCHEMA` to all the users.
# MAGIC
# MAGIC ### 1.2 Set up the secrets for the Bedrock credentials
# MAGIC
# MAGIC #### 1.2.1 Operations on the AWS account
# MAGIC This is executed:
# MAGIC - by the workshop admin, if a single AWS account is used for Bedrock access
# MAGIC - by every participant, if each of then has access to a dedicated AWS account (eg. through Workshop Studio)
# MAGIC
# MAGIC In an AWS account create an IAM user, with programmatic access only. For permissions one can:
# MAGIC - either attach the `AmazonBedrockFullAccess` IAM policy, or
# MAGIC - create an inline policy allowing bedrock:Invoke* to all resources.
# MAGIC
# MAGIC Create a new access key (to be invalidated at the end of the workshop) and save the access key Id and the secret access key.
# MAGIC
# MAGIC #### 1.2.2 Storing the AWS credentials in Databricks secrets (if needed)
# MAGIC *This is applicable only in the case where the admin will create a single set of serving endpoints to Bedrock that will be used by all participants.*
# MAGIC
# MAGIC Open the **Admin - 1. Secrets Setup For Bedrock** notebook
# MAGIC - Edit cell 4 and set the values of `aws_access_key_id` and `aws_secret_access_key` variables with the access key id and the secret access key from the above step.
# MAGIC - Attach to a serverless compute and run all cells of the notebook.
# MAGIC
# MAGIC This will set the values for the secrets `amazon-bedrock-credentials/access-key-id` and `amazon-bedrock-credentials/secret-access-key`
# MAGIC
# MAGIC This notebook should not be shared with the participants to avoid revealing the actual AWS credentials
# MAGIC
# MAGIC ### 1.3 Pre-create the Vector Search Endpoints
# MAGIC Given that a Vector Search endpoint can handle up to 50 indexes and the fact that each participant will create 2 indexes upon completion of the lab, the admin will need to pre-create a sufficience number of Vector Search Endpoints to accomodate all the participants.
# MAGIC
# MAGIC This is done by running the **Admin - 2. Vector Search Endpoints setup** notebook, after the admin has to set the `Number of Participants` notebook widget to the number of participants of the workshop.
# MAGIC
# MAGIC A Vector Search endpoint is created per 20 users and has a name such as `workshop_vs_endpoint_0`, `workshop_vs_endpoint_1`, `workshop_vs_endpoint_2`,...
# MAGIC
# MAGIC ### 1.4 Copy the participant install notebook to the Shared folder
# MAGIC The admin/participant copies (by cloning) the **Participant - Install and Configure Demo** notebook in the `Shared` folder of the Workspace.
# MAGIC
# MAGIC In case a different catalog name will be used (instead of the default `workshop`), before cloning the admin/presenter edits cell 4 and sets the `catalog` argument accordingly.
# MAGIC
# MAGIC ## 2. Lab Instructions
# MAGIC
# MAGIC ### 2.1 Content download and configuration
# MAGIC - Each participant copied (by cloning) the **Participant - Install and Configure Demo** notebook in the `Shared` folder to her/his home directory in the Workspace.
# MAGIC - The participant
# MAGIC   - opens the notebook, attaches Serverless compute, and runs all cells.
# MAGIC   - enters the **llm-rag-chatbot** folder under her/his home Workspace directory
# MAGIC   - opens the **config** notebook
# MAGIC   - updates the value of the **VECTOR_SEARCH_ENDPOINT_NAME** variable to be one of the pre-installed Vector Search Endpoints, already created by the admin. (the admin should instruct which participant should be using which endpoint name, assuring that the participants are evenly distributed across the endpoints)
# MAGIC
# MAGIC ### 2.2 Demo first pass (default content)
# MAGIC #### 2.2.1 Participant actions
# MAGIC Each participant
# MAGIC - enters the **01-first-step** folder
# MAGIC   - opens the **01-First-Step-RAG-On-Databricks** notebook
# MAGIC     - attaches it to Serverless compute
# MAGIC     - runs all cells.
# MAGIC
# MAGIC Note that that timeout errors may appear when running the cells that
# MAGIC - create the Vector Search index
# MAGIC - set up the model serving endpoint
# MAGIC If this happens, the participants are instructed to rerun the failing cell, as well as all the rest following it. (by clicking on the arrow next to the *play* button of the cell and selecting `Run all below`).
# MAGIC
# MAGIC #### 2.2.1 Presenter actions
# MAGIC - The presenter scrolls through the notebook explaining the logic being executed.
# MAGIC
# MAGIC - Once the presenter reaches cell 25 and while waiting for the endpoint to start, this is a good time to open the Catalog page on a different tab and walk the participants through the differentiating features of Unity Catalog:
# MAGIC   - Different asset types under the schema
# MAGIC     - Tabular data (tables, views, indexes)
# MAGIC     - Unstructured or semi-structured data on Volumes (S3 locations)
# MAGIC     - AI models; **show the model that was just created**.
# MAGIC   - Permissions on every asset type
# MAGIC   - Lineage information (from the model to the index)
# MAGIC   - Table popularity and statistics
# MAGIC   - AI-generated documentation
# MAGIC   The presenter discussed the fact that all the above feed the Databricks Intelligence Engine that allows Unity Catalog to discover data assets and the I.E. to respond questions asked in natural language.
# MAGIC
# MAGIC   **Typical business problems and value added discussed at this point**:
# MAGIC   - Traceability requirements, solved with end-to-end lineage across data assets
# MAGIC   - Data and AI democratization, from the fact that business users may ask business questions in natural language to be responded from the Lakehouse data and meta data in Unity.
# MAGIC
# MAGIC - The presenter opens on a new tab the serving page and shows the newly created endpoint
# MAGIC
# MAGIC - Once the presenter reaches cell 27, (s)he clicks on the generated link with the chatbot app is hosted
# MAGIC   - and demoes the chatbot capabilities and the feedback mechanism but running a couple of queries.
# MAGIC   - discusses inference tables and show them in UC (it's the table called `basic_rag_payload`).
# MAGIC
# MAGIC - Once the presenter reaches cell 31, (s)he clicks on the `view evaluation results` button, which opens in a new tab the evaluation page of the run corresponding to the registered model within the Experiments page of the workspace.
# MAGIC
# MAGIC ### 2.3 Creation of the Bedrock model serving endpoints
# MAGIC - The presenter/admin goes to the *Serving* page of the workspace shows how a serving endpoint is setup in the UI.
# MAGIC
# MAGIC - Endpoint creation:
# MAGIC   - If there is a single AWS account used for the Bedrock, the presenter/admin shows and runs the notebook **Admin - 3. Bedrock Endpoints Setup**.
# MAGIC   - If every participant has an AWS account, the admin guides the participants to create the endpoints (with their user name appended to the endpoint name) in the UI.
# MAGIC
# MAGIC - The presenter/admin shows the new endpoints, and runs a test query on the endpoint set up for the chat task
# MAGIC
# MAGIC - The presenter/admin goes to the *Playground* page of the workspace and demonstrates prompt engineering by comparing side-by-side Llama3, DBRX, and the Bedrock model from the external model serving endpoint just created.
# MAGIC
# MAGIC ### 2.4 Demo second pass (using the Bedrock Endpoints)
# MAGIC #### 2.4.1 Participant actions
# MAGIC Each participant
# MAGIC - clones the **01-First-Step-RAG-On-Databricks** notebook to **01a-First-Step-RAG-On-Databricks-with-Bedrock** on the same folder
# MAGIC - edits cell 8 (where the vector search index is defined)  
# MAGIC   - and appends a *_titan* suffix in the index name to create a different one:
# MAGIC   
# MAGIC     `vs_index_fullname = f"{catalog}.{db}.databricks_documentation_vs_index_titan"`
# MAGIC   - define the model to be used for the embeddings (it should be the name of the endpoint created in the previous step):
# MAGIC
# MAGIC     `embedding_model_endpoint_name='bedrock_embeddings' #The embedding endpoint used to create the embeddings`
# MAGIC - edits cell 13 (where the chain configuration is defined)
# MAGIC   - specifies the LLM for the chat from Bedrock (it should be the name of the endpoint created in the previous step)
# MAGIC
# MAGIC     `"llm_model_serving_endpoint_name": "bedrock_chat",  # the foundation model we want to use`
# MAGIC   - specifies the new vector search index to be used
# MAGIC
# MAGIC     `"vector_search_index": f"{catalog}.{db}.databricks_documentation_vs_index_titan",`
# MAGIC
# MAGIC - edits cell 23 (where the final model is deployed)
# MAGIC   - updating the run name by adding a *_bedrock* suffix:
# MAGIC     
# MAGIC     `with mlflow.start_run(run_name="basic_rag_bot_bedrock"):`
# MAGIC   - updating the model name by adding a *_bedrock* suffix:
# MAGIC
# MAGIC     `MODEL_NAME = "basic_rag_demo_bedrock"`
# MAGIC
# MAGIC - attaches the notebook to Serveless compute and runs all cells in the notebook
# MAGIC
# MAGIC #### 2.4.2 Presenter actions
# MAGIC - Goes to the `Catalog` page of the Workspace and shows the new index and new model that has been created.
# MAGIC - Scrolls to the point where the URL for the UI of the chatbot app has been generated, and tries out the new app.
# MAGIC - Scrolls to the point where the model evaluation is happening, opens the evaluation results and comments on the difference from the previous run with the original LLMs used.
# MAGIC
# MAGIC **Typical business problems and value added discussed at this point**:
# MAGIC - Minimising experimentation costs for Generative AI by maximising choice for LLMs and serving platforms, which accelerates innovation.
# MAGIC
# MAGIC ## 3. Proposed next steps / call to action
# MAGIC - Running the other, more complete examples of the demo
# MAGIC - Showing the LLM fine-tuning demo
