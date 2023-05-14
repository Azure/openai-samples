import logging
import faiss
import numpy as np
import pandas as pd
import json
import os
from azure.data.tables import TableServiceClient
from azure.core.credentials import AzureNamedKeyCredential
import openai
import azure.functions as func

account_name = os.environ["azure_table_account_name"]
account_key = os.environ["azure_table_key"]
table_name = os.environ["azure_table_name"]

# creating a client to connect to Azure Tables
credential = AzureNamedKeyCredential(account_name, account_key)
table_service_client = TableServiceClient(endpoint="https://{}.table.core.windows.net/".format(account_name), credential=credential)

# settings for the OpenAI SDK
openai.api_type = "azure"
openai.api_key = os.environ['open_ai_api_key']
openai.api_base = "https://{}.openai.azure.com/".format(os.environ["open_ai_resource_name"])
openai.api_version = os.getenv('open_ai_api_version') or "2022-12-01"
embedding_model = os.environ["open_ai_deployment_name"]

def get_openai_embedding(text, model):
    result = openai.Embedding.create(
      engine=model,
      input=text
    )
    return np.array(result["data"][0]["embedding"])

# function to load the data from the Azure Table
def load_data():
    table_client = table_service_client.get_table_client(table_name=table_name)

    entities = table_client.list_entities()
    df = pd.DataFrame(entities)

    # create an array of the embeddings
    vectors = df["embedding"].apply(lambda x: np.array(json.loads(x)))
    np_vectors = np.array(vectors.values.tolist()).astype(np.float32)

    return np_vectors, df

# code outside of main() function executes when the Azure Function is first spun up
# this allows the data and and index to be cached across multiple invocations
vectors, df = load_data()

# creating a FAISS index from the embeddings stored in the Azure Table
index = faiss.IndexFlatL2(1024)
index.add(vectors)

def main(req: func.HttpRequest) -> func.HttpResponse:
    global index
    global df

    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    # read in the parameters
    text = req_body.get('text')
    n = req_body.get('n') or 5
    force_reload = req_body.get('force_reload') or False

    # reload the data if needed
    if force_reload or index == None:
        index = faiss.IndexFlatL2(1024)
        vectors, df = load_data()
        index.add(vectors)

    # get the embedding from the input text
    embedding = get_openai_embedding(text, embedding_model)

    # find the n most similar vectors to the input vector
    _, similar = index.search(embedding.reshape(1, -1).astype(np.float32), n)

    # prep the output
    output = {
        "nearest_neighbors": similar[0].tolist(),
        "text": df.iloc[similar[0].tolist()]["content"].tolist()
    }

    logging.info(output)

    # return the results object
    return func.HttpResponse(json.dumps(output), mimetype="application/json")
