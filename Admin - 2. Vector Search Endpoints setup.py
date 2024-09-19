# Databricks notebook source
# MAGIC %md
# MAGIC ### Setting up Vector Search Endpoints

# COMMAND ----------

# DBTITLE 1,Install the relevant python packages
# MAGIC %pip install -U --quiet databricks-vectorsearch
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Retrieving the number of participants
dbutils.widgets.text("number_of_participants", "50", "Number of Participants")
number_of_participants = int(dbutils.widgets.get("number_of_participants"))

# COMMAND ----------

# DBTITLE 1,Determining the number of endpoints to be created
from math import ceil
number_of_endpoints = ceil(number_of_participants / 20)
if number_of_endpoints == 0: number_of_endpoints = 1
vs_endpoints = ['workshop_vs_endpoint_' + str(i) for i in range(number_of_endpoints)] 
print(str(number_of_endpoints) + ' endpoints will be created:\n')
for endpoint in vs_endpoints: print(endpoint)

# COMMAND ----------

# DBTITLE 1,Creating the endpoints and waiting until they are all up and running
from databricks.vector_search.client import VectorSearchClient
import time

vsc = VectorSearchClient(disable_notice=True)

def endpoint_exists(vsc, vs_endpoint_name):
  try:
    return vs_endpoint_name in [e['name'] for e in vsc.list_endpoints().get('endpoints', [])]
  except Exception as e:
    #Temp fix for potential REQUEST_LIMIT_EXCEEDED issue
    if "REQUEST_LIMIT_EXCEEDED" in str(e):
      print("WARN: couldn't get endpoint status due to REQUEST_LIMIT_EXCEEDED error. The demo will consider it exists")
      return True
    else:
      raise e

def wait_for_vs_endpoint_to_be_ready(vsc, vs_endpoint_name):
  for i in range(180):
    try:
      endpoint = vsc.get_endpoint(vs_endpoint_name)
    except Exception as e:
      #Temp fix for potential REQUEST_LIMIT_EXCEEDED issue
      if "REQUEST_LIMIT_EXCEEDED" in str(e):
        print("WARN: couldn't get endpoint status due to REQUEST_LIMIT_EXCEEDED error. Please manually check your endpoint status")
        return
      else:
        raise e
    status = endpoint.get("endpoint_status", endpoint.get("status"))["state"].upper()
    if "ONLINE" in status:
      return endpoint
    elif "PROVISIONING" in status or i <6:
      if i % 20 == 0: 
        print(f"Waiting for endpoint to be ready, this can take a few min... {endpoint}")
      time.sleep(10)
    else:
      raise Exception(f'''Error with the endpoint {vs_endpoint_name}. - this shouldn't happen: {endpoint}.\n Please delete it and re-run the previous cell: vsc.delete_endpoint("{vs_endpoint_name}")''')
  raise Exception(f"Timeout, your endpoint isn't ready yet: {vsc.get_endpoint(vs_endpoint_name)}")


for vs_endpoint in vs_endpoints:
    if not endpoint_exists(vsc, vs_endpoint):
        vsc.create_endpoint(name=vs_endpoint, endpoint_type="STANDARD")
for vs_endpoint in vs_endpoints:
    wait_for_vs_endpoint_to_be_ready(vsc, vs_endpoint)
    print(f"Endpoint named {vs_endpoint} is ready.")
