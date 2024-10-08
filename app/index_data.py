import pandas as pd
from tqdm.auto import tqdm
import re
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, BulkIndexError
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import json
import os


#ELASTIC_URL = os.getenv("ELASTIC_URL", "http://elasticsearch:9200")
#es_client = Elasticsearch(ELASTIC_URL)

ELASTIC_URL_LOCAL = os.getenv("ELASTIC_URL_LOCAL", "http://localhost:9200")
es_client = Elasticsearch(ELASTIC_URL_LOCAL)

model = SentenceTransformer('all-MiniLM-L6-v2')
index_name = 'flight_manuals'


def create_index():
    # Define index settings and mappings
    index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "manual_section": {"type": "keyword"},
            "scenario": {"type": "text"},
            "instructions": {"type": "text"},
            "id": {"type": "keyword"},
            "text": {"type": "text"},
            "text_vector": {"type": "dense_vector", "dims": 384, "index": True, "similarity": "cosine"}  # Adjust dims based on embedding size
        }
    }
}
    # Create the index
    if not es_client.indices.exists(index=index_name):
        es_client.indices.create(index=index_name, body=index_settings)
        print(f"Index '{index_name}' created.")
    else:
        print(f"Index '{index_name}' already exists.")


def get_documents():

    with open('../data/flight_manuals_documents-with-ids.json', 'rt') as f_in:
        documents = json.load(f_in)

    for doc in tqdm(documents):
        scenario = doc['scenario']
        instructions = doc['instructions']
        text = scenario + ". " +instructions
        doc['text'] = text
        doc['text_vector'] = model.encode(text)
    
    return documents

def generate_actions():
    for record in documents:
        yield {
            "_index": index_name,
            "_source": record
            
        }

def bulk_index_data(es_client, actions):
    try:
        bulk(es_client, generate_actions())
        print(f"Bulk indexing completed successfully! using {es_client}")
    except BulkIndexError as e:
        print(f"{len(e.errors)} documents failed to index")

        failed_documents = e.errors
        for i, error in enumerate(failed_documents, 1):
            action = error['index']
            error_info = action.get('error', {})
            document_id = action.get('_id', "N/A")
            status = action.get('status', "Unknown Status")

            print(f"\nFailed Document {i}:")
            print(f"ID: {document_id}")
            print(f"Status: {status}")
            print(f"Error Type: {error_info.get('type')}")
            print(f"Reason: {error_info.get('reason')}")
            document_source = action.get('data', {})
            print(f"Document Content: {document_source}")


if __name__ == "__main__":
    documents = get_documents()
    create_index()
    bulk_index_data(es_client, generate_actions())
