# Databricks notebook source
# MAGIC %md
# MAGIC ## Creating programmatically the serving endpoints to Bedrock
# MAGIC (One for Embeddings and another one for Chat)

# COMMAND ----------

# MAGIC %pip install -U --quiet databricks-sdk mlflow-skinny mlflow mlflow[gateway]
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Set the AWS region here

# COMMAND ----------

# DBTITLE 1,Set the region here
aws_region = 'us-east-1' # Specify 'us-east-1' or 'us-west-2'

# COMMAND ----------

# DBTITLE 1,Model availability
# The embeddings model available per region
embeddingsModelMapping = {
    'us-east-1': "titan-embed-g1-text-02",
    'us-west-2': "titan-embed-g1-text-02"
}

embeddingsProviderMapping = {
    'us-east-1': "amazon",
    'us-west-2': "amazon"
}

# The chat model available per region
chatModelMapping = {
    'us-east-1': "claude-3-5-sonnet-20240620-v1:0",
    'us-west-2': "claude-v2:1"
}

# The chat model available per region
chatProviderMapping = {
    'us-east-1': "anthropic",
    'us-west-2': "anthropic"
}

# COMMAND ----------

# DBTITLE 1,Choice of LLM in Bedrock
embeddingsModel = embeddingsModelMapping.get(aws_region)
embeddingsProvider = embeddingsProviderMapping.get(aws_region)
chatModel = chatModelMapping.get(aws_region)
chatProvider = chatProviderMapping.get(aws_region)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. Creation of the endpoints

# COMMAND ----------

# DBTITLE 1,Endpoint for the embeddings
from databricks.sdk import WorkspaceClient
client = WorkspaceClient()

from mlflow.deployments import get_deploy_client
from databricks.sdk.service.serving import ServingEndpointAccessControlRequest, ServingEndpointPermissionLevel
deploy_client = get_deploy_client('databricks')

embeddings_model_endpoint_name = 'bedrock_embeddings'

if embeddings_model_endpoint_name not in [endpoints['name'] for endpoints in deploy_client.list_endpoints()]:

    # Create the endpoint
    deploy_client.create_endpoint(
        name=embeddings_model_endpoint_name,
        config={
            "served_entities": [
                {
                    "external_model": {
                        "name": embeddingsModel,
                        "provider": "amazon-bedrock",
                        "task": "llm/v1/embeddings",
                        "amazon_bedrock_config": {
                            "aws_region": aws_region,
                            "aws_access_key_id": "{{secrets/amazon-bedrock-credentials/access-key-id}}",
                            "aws_secret_access_key": "{{secrets/amazon-bedrock-credentials/secret-access-key}}",
                            "bedrock_provider": embeddingsProvider
                        },
                    }
                }
            ]
        },
    )

    # Update the permissions
    serving_endpoint_id = client.serving_endpoints.get(embeddings_model_endpoint_name).id
    _ = client.serving_endpoints.update_permissions(
        serving_endpoint_id,
        access_control_list=[
            ServingEndpointAccessControlRequest(
                group_name='users',
                permission_level=ServingEndpointPermissionLevel.CAN_QUERY
            )
        ]
    )
print("External model for Amazon Titan embeddings has been created: " + embeddings_model_endpoint_name)

# COMMAND ----------

# DBTITLE 1,Endpoint for the chat
chat_model_endpoint_name = 'bedrock_chat'

if chat_model_endpoint_name not in [endpoints['name'] for endpoints in deploy_client.list_endpoints()]:

    # Create the endpoint
    deploy_client.create_endpoint(
        name=chat_model_endpoint_name,
        config={
            "served_entities": [
                {
                    "external_model": {
                        "name": chatModel,
                        "provider": "amazon-bedrock",
                        "task": "llm/v1/chat",
                        "amazon_bedrock_config": {
                            "aws_region": aws_region,
                            "aws_access_key_id": "{{secrets/amazon-bedrock-credentials/access-key-id}}",
                            "aws_secret_access_key": "{{secrets/amazon-bedrock-credentials/secret-access-key}}",
                            "bedrock_provider": chatProvider
                        },
                    }
                }
            ]
        },
    )

    # Update the permissions
    serving_endpoint_id = client.serving_endpoints.get(chat_model_endpoint_name).id
    _ = client.serving_endpoints.update_permissions(
        serving_endpoint_id,
        access_control_list=[
            ServingEndpointAccessControlRequest(
                group_name='users',
                permission_level=ServingEndpointPermissionLevel.CAN_QUERY
            )
        ]
    )
print("External model for Anthropic Claude chat has been created: " + chat_model_endpoint_name)

