import streamlit as st
import numpy as np
import io
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import os
from st_audiorec import st_audiorec
import rag_assistant
import storage
import time
import uuid

def print_log(message):
    print(message, flush=True)

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
    # Initialize the database
    storage.init_db()

    st.title("AviMate Pilot Assistant Bot")

    # Session state initialization
    if 'count' not in st.session_state:
        st.session_state.count = 0
        print_log("Feedback count initialized to 0")
    if 'feedback_given' not in st.session_state:
        st.session_state.feedback_given = False
    if 'state' not in st.session_state:
        st.session_state.state = 'idle'
    if 'query_audio_bytes' not in st.session_state:
        st.session_state.query_audio_bytes = None

    tab1, tab2 = st.tabs(["Text Input", "Voice Input"])

    # Text Input Tab
    with tab1:
        user_input = st.text_input("Enter your query:")
        if st.button("Ask", key="text"):
            if user_input.strip() != "":
                start_time = time.time()
                output = rag_assistant.rag(user_input)
                end_time = time.time()
                print_log(f"Answer received in {end_time - start_time:.2f} seconds")
                st.success("Completed!")
                st.write(output)
                
                # Generate a new conversation_id
                conversation_id = storage.generate_unique_id()
                
                print_log("Saving conversation to database")
                # Save conversation
                storage.save_conversation(conversation_id, user_input, output)
                print_log("Conversation saved successfully")

                # Save conversation ID to session state for feedback tracking
                st.session_state.current_conversation_id = conversation_id

                # Reset feedback_given for this new conversation
                st.session_state.feedback_given = False

                # Text-to-speech
                audio_file = text_to_speech(output)
                audio_data = open(audio_file, 'rb').read()
                st.audio(audio_data, format='audio/mp3')
            else:
                st.warning("Please enter a query.")

        # Feedback buttons (only if feedback not yet given)
        if 'current_conversation_id' in st.session_state and not st.session_state.feedback_given:
            st.write("Was this answer helpful?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("+1", key="text_positive_feedback"):
                    st.session_state.count += 1
                    print_log(f"Positive feedback received. New count: {st.session_state.count}")
                    storage.save_feedback(st.session_state.current_conversation_id, 1)
                    st.session_state.feedback_given = True
                    st.success("Thank you for your positive feedback!")
            with col2:
                if st.button("-1", key="text_negative_feedback"):
                    st.session_state.count -= 1
                    print_log(f"Negative feedback received. New count: {st.session_state.count}")
                    storage.save_feedback(st.session_state.current_conversation_id, -1)
                    st.session_state.feedback_given = True
                    st.success("Thank you for your constructive feedback!")

        st.write(f"Current count: {st.session_state.count}")

        print_log("Streamlit TAB 1 loop completed")

    # Voice Input Tab
    with tab2:
        st.header("Voice Input")
        st.write("Click 'Ask' to start recording your question.")

        col1, col2 = st.columns(2)
        with col1:
            ask_button = st.button("Ask", key="voice_ask")
        with col2:
            stop_button = st.button("Stop", key="voice_stop")

        if ask_button and st.session_state.state == 'idle':
            st.session_state.state = 'recording'
            st.write("Recording... Please speak your question.")

        if st.session_state.state == 'recording':
            audio_data = st_audiorec()
            if audio_data is not None:
                st.session_state.query_audio_bytes = audio_data

        if stop_button and st.session_state.state == 'recording':
            if st.session_state.query_audio_bytes is not None:
                st.write("Processing your question...")
                transcription = transcribe_audio(st.session_state.query_audio_bytes)
                st.write(f"You said: {transcription}")
                if transcription.strip() == "":
                    st.error("Sorry, could not understand the audio.")
                else:
                    with st.spinner('Processing...'):
                        conversation_id = storage.generate_unique_id()
                        answer = rag_assistant.rag(transcription)
                        st.success("Completed!")
                        st.write(answer)

                        # Save conversation
                        storage.save_conversation(conversation_id, transcription, answer)

                        # Save conversation ID to session state for feedback tracking
                        st.session_state.current_conversation_id = conversation_id

                        # Reset feedback_given for this new conversation
                        st.session_state.feedback_given = False

                        # Text-to-speech
                        audio_file = text_to_speech(answer)
                        audio_data = open(audio_file, 'rb').read()
                        st.audio(audio_data, format='audio/mp3')

                st.session_state.state = 'idle'
                st.session_state.query_audio_bytes = None
            else:
                st.warning("No audio recorded. Please try again.")
                st.session_state.state = 'idle'
                st.session_state.query_audio_bytes = None

        # Feedback buttons (only if feedback not yet given)
        if 'current_conversation_id' in st.session_state and not st.session_state.feedback_given:
            st.write("Was this answer helpful?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("+1", key="voice_positive_feedback"):
                    storage.save_feedback(st.session_state.current_conversation_id, 1)
                    st.session_state.feedback_given = True
                    st.success("Thank you for your positive feedback!")
            with col2:
                if st.button("-1", key="voice_negative_feedback"):
                    storage.save_feedback(st.session_state.current_conversation_id, -1)
                    st.session_state.feedback_given = True
                    st.success("Thank you for your constructive feedback!")

if __name__ == "__main__":
    main()
