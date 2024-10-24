import os
import openai
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import pandas as pd
from tqdm.auto import tqdm
import re
from elasticsearch.helpers import bulk, BulkIndexError
from openai import OpenAI
import json

# Set OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
openai_client = OpenAI(api_key=OPENAI_API_KEY)


# Initialize Elasticsearch client
ELASTIC_URL_LOCAL = os.getenv("ELASTIC_URL_LOCAL", "http://localhost:9200")
es_client = Elasticsearch(ELASTIC_URL_LOCAL)


# Load Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

index_name = 'atc_communications'
index_name_flight_manuals = 'flight_manuals'
conversation_history = []

# Remove the global conversation_history variable
# conversation_history = []

def get_user_query(query):
    # For demonstration, you can hardcode a query or accept input
    return query

def get_query_embedding(query):
    return model.encode(query).tolist()

def elastic_search_combine(query_vector, index_name, es_client, top_k=10, source_fields=None):
    # Define the script query
    script_query = {
        "script_score": {
            "query": {
                "match_all": {}
            },
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
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
                "_source": source_fields or ["*"]
            }
        )
        
        # Collect the search results
        result_docs = [hit['_source'] for hit in response['hits']['hits']]
        
        return result_docs  # Return the results for further processing if needed
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def retrieve_documents_all(query):
    query_vector = get_query_embedding(query)
    # Search in ATC communications
    atc_docs = elastic_search_combine(query_vector, index_name, es_client, top_k=10)
    # serach in flight manual
    flight_manual_docs = elastic_search_combine(query_vector, index_name_flight_manuals, es_client, top_k=10)
    # Combine results
    retrieved_docs = (atc_docs or []) + (flight_manual_docs or [])

    return retrieved_docs

def format_retrieved_documents_all(retrieved_docs):
    formatted_docs = ""

    for doc in retrieved_docs:
        if doc.get('source') == "atc_communication":
            formatted_docs = f"Time: {doc['time_utc']}, Message: {doc['message']}, Phase: {doc['phase']}, Event Flag: {doc['event_flag']}\n"

        elif doc.get('source') == "flight_manual":
            formatted_docs = f"Manual Section: {doc['manual_section']}, Scenario: {doc['scenario']}, Instructions: {doc['instructions']}\n"

        else:
            # Handle other sources if any
            formatted_docs = f"{doc}\n"          

        return formatted_docs

def build_messages_combine(question, retrieved_docs, conversation_history):
    # System prompt without retrieved documents
    system_prompt = """
    You are an assistant helping pilots with giving informations such as flight manuals, ATC communications etc. Use the provided ATC communication information and flight manual to answer the user's questions.
    """.strip()

    # Build the messages list
    messages = []

    # Add the system prompt
    messages.append({'role': 'system', 'content': system_prompt})

    # Add the retrieved documents as a system message
    formatted_docs = format_retrieved_documents_all(retrieved_docs)
    messages.append({'role': 'system', 'content': f"ATC communication information:\n{formatted_docs}"})

    # Add recent conversation history (limit to last N messages to stay within token limits)
    messages.extend(conversation_history[-10:])  # Adjust N as needed

    # Add the user's latest question
    messages.append({'role': 'user', 'content': question})

    return messages

def generate_answer_all(messages):
    response = openai_client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        max_tokens=2500,
        temperature=0
    )
    answer = response.choices[0].message.content
    return answer

def rag_combine(query):
    query = get_user_query(query)
    retrieved_docs = retrieve_documents_all(query)
    messages = build_messages_combine(query, retrieved_docs, conversation_history)
    answer = generate_answer_all(messages)
    # Update the conversation history
    conversation_history.append({'role': 'user', 'content': query})
    conversation_history.append({'role': 'assistant', 'content': answer})

    return answer