# Databricks notebook source
# MAGIC %md
# MAGIC # Installing and Configuring the workshop content

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Install the demo content
# MAGIC **Connect** to the *Serverless* Compute and **Run all** cells of this notebook. 
# MAGIC
# MAGIC Then scroll to the end of this notebook and follow the instructions on the last cell

# COMMAND ----------

# DBTITLE 1,Install DBDEMOS
# MAGIC %pip install -U dbdemos
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Install the LLM RAG Chatbot demo
import dbdemos
email = spark.sql('select current_user() as user').collect()[0]['user']
username = email.split('@')[0].replace('.', '_')
dbdemos.install('llm-rag-chatbot',catalog='workshop',schema=username,path='/Users/' + email, overwrite=True)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. Configure the demo
# MAGIC - Enter the **llm-rag-chatbot** folder
# MAGIC - Open the **config** notebook
# MAGIC - Update the value of the **VECTOR_SEARCH_ENDPOINT_NAME** variable to be one of the pre-installed Vector Search Endpoints, already created by the admin
