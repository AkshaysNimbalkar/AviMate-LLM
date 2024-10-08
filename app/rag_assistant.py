import os
import openai
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import pandas as pd
from tqdm.auto import tqdm
import re
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, BulkIndexError
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import json

# Set OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Elasticsearch client
#ELASTIC_URL = os.getenv("ELASTIC_URL", "http://elasticsearch:9200")
#es_client = Elasticsearch(ELASTIC_URL)

ELASTIC_URL_LOCAL = os.getenv("ELASTIC_URL_LOCAL", "http://localhost:9200")
es_client = Elasticsearch(ELASTIC_URL_LOCAL)

# Load Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')
index_name = 'flight_manuals'

def get_user_query(query):
    # For demonstration, you can hardcode a query or accept input
    return query

def get_query_embedding(query):
    return model.encode(query).tolist()

def elastic_search(query_vector, index_name, es_client, top_k=3):
    # Define the script query
    script_query = {
        "script_score": {
            "query": {
                "match_all": {}
            },
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'text_vector') + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }
    
    try:
        # Execute the search query
        response = es_client.search(
            index=index_name,
            body={
                "size": top_k,
                "query": script_query,
                "_source": ["manual_section", "scenario", "instructions", "text", "id"]  # Adjust fields as needed
            }
        )
        
        # Collect the search results
        result_docs = [hit['_source'] for hit in response['hits']['hits']]
        
        return result_docs  # Return the results for further processing if needed
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def retrieve_documents(query):
    query_vector = get_query_embedding(query)
    retrieved_docs = elastic_search(query_vector, index_name, es_client, top_k=3)
    return retrieved_docs

def format_retrieved_documents(retrieved_docs):
    formatted_docs = ""
    for doc in retrieved_docs:
        formatted_docs += f"Manual Section: {doc['manual_section']}\n"
        formatted_docs += f"Scenario: {doc['scenario']}\n"
        formatted_docs += f"Instructions: {doc['instructions']}\n"
        formatted_docs += f"Text: {doc['text']}\n\n"
    return formatted_docs

def build_prompt(question, retrieved_docs):

    prompt_template = """
    You are an assistant helping pilots with flight procedures. Based on the following flight manual information, answer the question:

    Flight Manual Information:
    {retrieved_docs}

    Question:
    {question}

    Answer:
    """.strip()

    # Format the retrieved documents
    formatted_docs = format_retrieved_documents(retrieved_docs)
    
    # Construct the prompt
    prompt = prompt_template.format(retrieved_docs=formatted_docs, question=question)
    
    return prompt

def generate_answer(prompt):
    response = openai_client.chat.completions.create(
        model = 'gpt-4o-mini', 
        messages = [{'role':'assistant', 'content':prompt}],
        max_tokens = 2500,
        temperature=0.5
    )
    answer = response.choices[0].message.content

    return answer

def rag(query):
    query = get_user_query(query)
    retrieved_docs = retrieve_documents(query)
    prompt = build_prompt(query, retrieved_docs)
    answer = generate_answer(prompt)
    #print("\nAnswer:\n", answer)

    return answer
