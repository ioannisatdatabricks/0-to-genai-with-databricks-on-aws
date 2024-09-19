# Databricks notebook source
# MAGIC %md
# MAGIC ### Creating programmatically the serving endpoints to Bedrock
# MAGIC (Titan for Embeddings and Anthropic Claude 3.5 for chat)

# COMMAND ----------

# MAGIC %pip install -U --quiet databricks-sdk mlflow-skinny mlflow mlflow[gateway]
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Endpoint for the embeddings
from databricks.sdk import WorkspaceClient
client = WorkspaceClient()

from mlflow.deployments import get_deploy_client
from databricks.sdk.service.serving import ServingEndpointAccessControlRequest, ServingEndpointPermissionLevel
deploy_client = get_deploy_client('databricks')

embeddings_model_endpoint_name = 'amazon-titan-g1-text-02'

if embeddings_model_endpoint_name not in [endpoints['name'] for endpoints in deploy_client.list_endpoints()]:

    # Create the endpoint
    deploy_client.create_endpoint(
        name=embeddings_model_endpoint_name,
        config={
            "served_entities": [
                {
                    "external_model": {
                        "name": "titan-embed-g1-text-02",
                        "provider": "amazon-bedrock",
                        "task": "llm/v1/embeddings",
                        "amazon_bedrock_config": {
                            "aws_region": "us-east-1",
                            "aws_access_key_id": "{{secrets/amazon-bedrock-credentials/access-key-id}}",
                            "aws_secret_access_key": "{{secrets/amazon-bedrock-credentials/secret-access-key}}",
                            "bedrock_provider": "amazon"
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
chat_model_endpoint_name = 'anthropic-claude-3-5-sonnet'

if chat_model_endpoint_name not in [endpoints['name'] for endpoints in deploy_client.list_endpoints()]:

    # Create the endpoint
    deploy_client.create_endpoint(
        name=chat_model_endpoint_name,
        config={
            "served_entities": [
                {
                    "external_model": {
                        "name": "claude-3-5-sonnet-20240620-v1:0",
                        "provider": "amazon-bedrock",
                        "task": "llm/v1/chat",
                        "amazon_bedrock_config": {
                            "aws_region": "us-east-1",
                            "aws_access_key_id": "{{secrets/amazon-bedrock-credentials/access-key-id}}",
                            "aws_secret_access_key": "{{secrets/amazon-bedrock-credentials/secret-access-key}}",
                            "bedrock_provider": "anthropic"
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

