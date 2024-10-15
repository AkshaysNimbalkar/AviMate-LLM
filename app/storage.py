import psycopg2
import uuid
from datetime import datetime
import os


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        database=os.getenv("POSTGRES_DB", "flight-assistant"),
        user=os.getenv("POSTGRES_USER", "root"),
        password=os.getenv("POSTGRES_PASSWORD", "root"),
        )

def init_db():
    """Initialize the database and create tables if they do not exist."""
    conn = get_connection()
    cur = conn.cursor()
    
    # Create conversations table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id VARCHAR PRIMARY KEY,
        question TEXT,
        answer TEXT,
        timestamp TIMESTAMP
    )
    """)
    
    # Create feedback table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id SERIAL PRIMARY KEY,
        conversation_id VARCHAR,
        feedback INTEGER,
        timestamp TIMESTAMP
    )
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def generate_unique_id():
    """Generate a unique ID for each conversation."""
    return str(uuid.uuid4())

def save_conversation(conversation_id, question, answer):
    """Save the conversation to the database."""
    conn = get_connection()
    cur = conn.cursor()
    insert_query = """
    INSERT INTO conversations (id, question, answer, timestamp)
    VALUES (%s, %s, %s, %s)
    """
    cur.execute(insert_query, (conversation_id, question, answer, datetime.utcnow()))
    conn.commit()
    cur.close()
    conn.close()

def save_feedback(conversation_id, feedback_value):
    """Save user feedback to the database."""
    conn = get_connection()
    cur = conn.cursor()
    insert_query = """
    INSERT INTO feedback (conversation_id, feedback, timestamp)
    VALUES (%s, %s, %s)
    """
    cur.execute(insert_query, (conversation_id, feedback_value, datetime.utcnow()))
    conn.commit()
    cur.close()
    conn.close()


