# Databricks notebook source
# MAGIC %md
# MAGIC # This notebooks should NOT TO BE SHOWN to the participants

# COMMAND ----------

# MAGIC %md
# MAGIC ### Setting up the Secrets for the Bedrock endpoints

# COMMAND ----------

# DBTITLE 1,Install the relevant python packages
# MAGIC %pip install -U --quiet databricks-sdk
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Specify the access keys here
aws_access_key_id = <ACCESS_KEY_ID>
aws_secret_access_key = <SECRET_ACCESS_KEY>

# COMMAND ----------

# DBTITLE 1,Storing the AWS credentials for accessing Bedrock in Databricks Secrets
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import ResourceAlreadyExists
from databricks.sdk.service.workspace import AclPermission

client = WorkspaceClient()
try: client.secrets.create_scope(scope="amazon-bedrock-credentials")
except ResourceAlreadyExists: pass

client.secrets.put_secret(
    scope="amazon-bedrock-credentials",
    key="access-key-id",
    string_value=aws_access_key_id
)

client.secrets.put_secret(
    scope="amazon-bedrock-credentials",
    key="secret-access-key",
    string_value=aws_secret_access_key
)

client.secrets.put_acl(
    scope="amazon-bedrock-credentials",
    principal="users",
    permission=AclPermission.READ
)
