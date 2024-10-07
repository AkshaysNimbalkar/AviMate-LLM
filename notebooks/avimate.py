import streamlit as st
import numpy as np
import io
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
from openai import OpenAI
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from st_audiorec import st_audiorec


# Initialize OpenAI client
client = OpenAI()

# Initialize Elasticsearch client
es_client = Elasticsearch('http://localhost:9200')

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
        formatted_docs += f"Instructions: {doc['instructions']}\n\n"
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
    response = client.chat.completions.create(
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

def transcribe_audio(audio_bytes):
    r = sr.Recognizer()
    audio = sr.AudioFile(io.BytesIO(audio_bytes))
    with audio as source:
        audio_data = r.record(source)
    try:
        text = r.recognize_google(audio_data)
    except (sr.UnknownValueError, sr.RequestError):
        text = ""
    return text.lower()

def text_to_speech(text):
    tts = gTTS(text)
    audio_file = "response.mp3"
    tts.save(audio_file)
    return audio_file

def main():
    st.title("AviMate Pilot Assistant Bot")

    # Initialize session state variables
    if 'state' not in st.session_state:
        st.session_state.state = 'idle'
    if 'query_audio_bytes' not in st.session_state:
        st.session_state.query_audio_bytes = None

    # Tabs for Text and Voice Input
    tab1, tab2 = st.tabs(["Text Input", "Voice Input"])

    # Text Input Tab
    with tab1:
        user_input = st.text_input("Enter your query:")
        if st.button("Ask", key="text"):
            if user_input.strip() != "":
                output = rag(user_input)
                st.success("Completed!")
                st.write(output)
                # Convert answer to speech
                audio_file = text_to_speech(output)
                audio_data = open(audio_file, 'rb').read()
                st.audio(audio_data, format='audio/mp3')
            else:
                st.warning("Please enter a query.")

    # Voice Input Tab
    with tab2:
        st.header("Voice Input")

        # Instructions for the user
        st.write("Click 'Ask' to start recording your question.")

    # Voice Input Tab
        # Ask and Stop buttons
        col1, col2 = st.columns(2)
        with col1:
            ask_button = st.button("Ask", key="voice_ask")
        with col2:
            stop_button = st.button("Stop", key="voice_stop")

        if ask_button and st.session_state.state == 'idle':
            st.session_state.state = 'recording'
            st.write("Recording... Please speak your question.")

        if st.session_state.state == 'recording':
            # Record audio for the user's question
            audio_data = st_audiorec()
            if audio_data is not None:
                st.session_state.query_audio_bytes = audio_data

        if stop_button and st.session_state.state == 'recording':
            if st.session_state.query_audio_bytes is not None:
                # Process the query audio
                st.write("Processing your question...")
                transcription = transcribe_audio(st.session_state.query_audio_bytes)
                st.write(f"You said: {transcription}")
                if transcription.strip() == "":
                    st.error("Sorry, could not understand the audio.")
                else:
                    with st.spinner('Processing...'):
                        answer = rag(transcription) 
                        st.success("Completed!")
                        st.write(answer)
                        # Convert answer to speech
                        audio_file = text_to_speech(answer)
                        audio_data = open(audio_file, 'rb').read()
                        st.audio(audio_data, format='audio/mp3')
                
                # Reset the state
                st.session_state.state = 'idle'
                st.session_state.query_audio_bytes = None
            else:
                st.warning("No audio recorded. Please try again.")
                st.session_state.state = 'idle'
                st.session_state.query_audio_bytes = None


if __name__ == "__main__":
    main()
