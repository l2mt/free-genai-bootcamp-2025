import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.get_transcript import YouTubeTranscriptDownloader
import streamlit as st
from typing import Dict
import json
from collections import Counter
import re
 
from backend.chat import OpenAIChat
from backend.question_generator import QuestionGenerator
from backend.vector_store import QuestionVectorStore

# Page config
st.set_page_config(
    page_title="Spanish Learning Assistant",
    page_icon="🇪🇸",
    layout="wide"
)

# Initialize session state
if 'transcript' not in st.session_state:
    st.session_state.transcript = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'question_generator' not in st.session_state:
    st.session_state.question_generator = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'feedback' not in st.session_state:
    st.session_state.feedback = None
if 'selected_answer' not in st.session_state:
    st.session_state.selected_answer = None

def render_header():
    """Render the header section"""
    st.title("Spanish Learning Assistant")
    st.markdown("""
    Transform YouTube transcripts into interactive learning experiences for Spanish.
    
    This tool demonstrates:
    - Basic LLM Capabilities
    - RAG (Retrieval Augmented Generation)
    - OpenAI Integration
    - Agent-based Learning Systems
    """)

def render_sidebar():
    """Render the sidebar with component selection"""
    with st.sidebar:
        st.header("Development Stages")
        
        # Main component selection
        selected_stage = st.radio(
            "Select Stage:",
            [
                "1. Chat with GPT",
                "2. Raw Transcript",
                "3. Structured Data",
                "4. RAG Implementation",
                "5. Interactive Learning"
            ]
        )
        
        # Stage descriptions
        stage_info = {
            "1. Chat with GPT": """
            **Current Focus:**
            - Basic Spanish learning
            - Understanding LLM capabilities
            - Identifying limitations
            """,
            
            "2. Raw Transcript": """
            **Current Focus:**
            - YouTube transcript download
            - Raw text visualization
            - Initial data examination
            """,
            
            "3. Structured Data": """
            **Current Focus:**
            - Text cleaning
            - Dialogue extraction
            - Data structuring
            """,
            
            "4. RAG Implementation": """
            **Current Focus:**
            - Bedrock embeddings
            - Vector storage
            - Context retrieval
            """,
            
            "5. Interactive Learning": """
            **Current Focus:**
            - Scenario generation
            - Audio synthesis
            - Interactive practice
            """
        }
        
        st.markdown("---")
        st.markdown(stage_info[selected_stage])
        
        return selected_stage

def render_chat_stage():
    """Render an improved chat interface"""
    st.header("Chat with GPT")

    # Initialize GPT chat instance if not in session state
    if 'gpt_chat' not in st.session_state:
        st.session_state.gpt_chat = OpenAIChat()

    # Introduction text
    st.markdown("""
    Start by exploring GPT's Spanish language capabilities. Try asking questions about Spanish grammar, 
    vocabulary, or cultural aspects.
    """)

    # Initialize chat history if not exists
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])

    # Chat input area
    if prompt := st.chat_input("Ask about the Spanish language..."):
        # Process the user input
        process_message(prompt)

    # Example questions in sidebar
    with st.sidebar:
        st.markdown("### Try These Examples")
        example_questions = [
            "How do I say 'Where is the train station?' in Spanish?",
            "Explain the difference between 'ser' and 'estar'",
            "What is the formal form of 'comer'?",
            "How do I count objects in Spanish?",
            "What is the difference between 'hola' and 'buenas noches'?",
            "How do I ask for directions politely?"
        ]
        
        for q in example_questions:
            if st.button(q, use_container_width=True, type="secondary"):
                # Process the example question
                process_message(q)
                st.rerun()

    # Add a clear chat button
    if st.session_state.messages:
        if st.button("Clear Chat", type="primary"):
            st.session_state.messages = []
            st.rerun()

def process_message(message: str):
    """Process a message and generate a response"""
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": message})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(message)

    # Generate and display assistant's response using OpenAIChat (GPT)
    with st.chat_message("assistant", avatar="🤖"):
        response = st.session_state.gpt_chat.generate_response(message)
        if response:
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

def count_characters(text):
    """Count alphabetic characters and total characters in text"""
    if not text:
        return 0, 0
        
    letter_count = sum(1 for char in text if char.isalpha())
    return letter_count, len(text)

def render_transcript_stage():
    """Render the raw transcript stage"""
    st.header("Raw Transcript Processing")
    
    # URL input
    url = st.text_input(
        "YouTube URL",
        placeholder="Enter a Spanish lesson YouTube URL"
    )
    
    # Download button and processing
    if url:
        if st.button("Download Transcript"):
            try:
                downloader = YouTubeTranscriptDownloader()
                transcript = downloader.get_transcript(url)
                print(transcript)
                if transcript:
                    # Store the raw transcript text in session state
                    transcript_text = "\n".join([entry['text'] for entry in transcript])
                    st.session_state.transcript = transcript_text
                    st.success("Transcript downloaded successfully!")
                else:
                    st.error("No transcript found for this video.")
            except Exception as e:
                st.error(f"Error downloading transcript: {str(e)}")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Raw Transcript")
        if st.session_state.transcript:
            st.text_area(
                label="Raw text",
                value=st.session_state.transcript,
                height=400,
                disabled=True
            )
        else:
            st.info("No transcript loaded yet")
    
    with col2:
        st.subheader("Transcript Stats")
        if st.session_state.transcript:
            # Calculate stats
            letters, total_chars = count_characters(st.session_state.transcript)
            total_lines = len(st.session_state.transcript.split('\n'))
            
            # Display stats
            st.metric("Total Characters", total_chars)
            st.metric("Alphabetic Characters", letters)
            st.metric("Total Lines", total_lines)
        else:
            st.info("Load a transcript to see statistics")

def render_structured_stage():
    """Render the structured data stage"""
    st.header("Structured Data Processing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dialogue Extraction")
        # Placeholder for dialogue processing
        st.info("Dialogue extraction will be implemented here")
        
    with col2:
        st.subheader("Data Structure")
        # Placeholder for structured data view
        st.info("Structured data view will be implemented here")

def render_rag_stage():
    """Render the RAG implementation stage"""
    st.header("RAG System")
    
    # Initialize vector store if not in session state
    if 'vector_store' not in st.session_state:
        try:
            from backend.vector_store import QuestionVectorStore
            st.session_state.vector_store = QuestionVectorStore()
        except Exception as e:
            st.error(f"Error initializing vector store: {str(e)}")
            return

    # Query input
    query = st.text_input(
        "Test Query",
        placeholder="Enter a question about Spanish..."
    )
    
    col1, col2 = st.columns(2)
    
    if query:
        try:
            # Search for similar questions
            similar_questions = st.session_state.vector_store.search_similar_questions(query, n_results=3)
            
            with col1:
                st.subheader("Retrieved Context")
                for idx, question in enumerate(similar_questions):
                    with st.expander(f"Similar Question {idx + 1}"):
                        st.write("Question:", question['question'])
                        st.write("Similarity Score:", f"{question['similarity_score']:.4f}")
                        if 'answer' in question:
                            st.write("Answer:", question['answer'])
            
            with col2:
                st.subheader("Generated Response")
                if similar_questions:
                    # Use the most similar question's answer as context
                    context = "\n".join([
                        f"Q: {q['question']}\nA: {q.get('answer', 'No answer available')}"
                        for q in similar_questions
                    ])
                    
                    if 'gpt_chat' in st.session_state:
                        response = st.session_state.gpt_chat.generate_response(
                            f"Based on these similar questions and answers:\n{context}\n\nUser question: {query}"
                        )
                        st.write(response)
                    else:
                        st.warning("Chat system not initialized")
                else:
                    st.info("No similar questions found in the database")
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")
    else:
        with col1:
            st.info("Enter a question to search for similar content")
        with col2:
            st.info("The response will appear here")

def render_interactive_stage():
    """Render the interactive learning stage with question generation"""
    st.header("Interactive Spanish Learning")
    
    # Initialize question generator if it doesn't exist
    if not st.session_state.question_generator:
        with st.spinner("Initializing question generator (this may take a moment on first run)..."):
            try:
                # Make sure the vector database is loaded
                st.info("Setting up the question system... This may take a moment on first run.")
                # Force recreation of the collection only if necessary
                QuestionVectorStore._force_recreate = False
                vector_store = QuestionVectorStore()
                # Check if the database has indexed questions
                try:
                    # Quick search test to verify if there's data
                    test_result = vector_store.search_similar_questions("test", n_results=1)
                    if not test_result:
                        st.warning("Question database appears to be empty. Running initial indexing...")
                        # Index example questions
                        question_files = [
                            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                        "data/questions/R-kepxbu5fM.json")
                        ]
                        for filename in question_files:
                            if os.path.exists(filename):
                                vector_store.index_questions_file(filename)
                            else:
                                st.error(f"Question file not found: {filename}")
                except Exception as e:
                    st.warning(f"Error checking database: {str(e)}")
                
                # Now initialize the question generator
                st.session_state.question_generator = QuestionGenerator()
                st.success("Question generator ready!")
            except Exception as e:
                st.error(f"Error initializing question generator: {str(e)}")
                return
    
    # Topic selector
    topics = ["Astronomy", "Geography", "History", "Science", "Art", "Sports", "Other"]
    selected_topic = st.selectbox("Select a topic:", topics)
    
    # Custom topic field
    if selected_topic == "Other":
        custom_topic = st.text_input("Enter a custom topic:")
        topic_to_use = custom_topic
    else:
        topic_to_use = selected_topic
    
    # Button to generate question
    if topic_to_use and st.button("Generate Question"):
        with st.spinner(f"Generating question about '{topic_to_use}'..."):
            try:
                # Generate question using RAG
                question = st.session_state.question_generator.generate_similar_question(topic_to_use)
                if question:
                    st.session_state.current_question = question
                    st.session_state.feedback = None
                    st.session_state.selected_answer = None
                    st.success("Question generated!")
                else:
                    st.warning("Could not generate a question. Try a different topic.")
            except Exception as e:
                st.error(f"Error generating question: {str(e)}")
    
    # Display the generated question
    if st.session_state.current_question:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Scenario (in Spanish)")
            st.info(st.session_state.current_question.get('Context', 'No context available'))
            
            st.subheader("Question (in Spanish)")
            st.write(st.session_state.current_question.get('Question', 'No question available'))
            
            # Display options as buttons
            st.subheader("Options")
            options = st.session_state.current_question.get('Options', [])
            
            for i, option in enumerate(options, 1):
                # Disable buttons if there's already feedback
                disabled = st.session_state.feedback is not None
                if st.button(f"{i}. {option}", key=f"option_{i}", disabled=disabled):
                    st.session_state.selected_answer = i
                    # Get feedback
                    try:
                        feedback = st.session_state.question_generator.get_feedback(
                            st.session_state.current_question, 
                            st.session_state.selected_answer
                        )
                        st.session_state.feedback = feedback
                        st.rerun()  # Update UI
                    except Exception as e:
                        st.error(f"Error getting feedback: {str(e)}")
        
        with col2:
            # Display feedback if it exists
            if st.session_state.feedback:
                st.subheader("Feedback")
                
                # Show if correct or incorrect
                is_correct = st.session_state.feedback.get('correct', False)
                if is_correct:
                    st.success("Correct answer! 🎉")
                else:
                    st.error("Incorrect answer")
                    
                # Show explanation
                st.write("**Explanation:**")
                st.write(st.session_state.feedback.get('explanation', 'No explanation available'))
                
                # Show correct answer
                correct_answer_num = st.session_state.feedback.get('correct_answer', 1)
                if correct_answer_num <= len(options):
                    st.write(f"**Correct answer:** {correct_answer_num}. {options[correct_answer_num-1]}")
                
                # Show button for new question
                if st.button("Generate New Question"):
                    st.session_state.current_question = None
                    st.session_state.feedback = None
                    st.session_state.selected_answer = None
                    st.rerun()  # Update UI
    else:
        # Message when there's no generated question
        st.info("Select a topic and click 'Generate Question' to start.")

def main():
    render_header()
    selected_stage = render_sidebar()
    
    # Render appropriate stage
    if selected_stage == "1. Chat with GPT":
        render_chat_stage()
    elif selected_stage == "2. Raw Transcript":
        render_transcript_stage()
    elif selected_stage == "3. Structured Data":
        render_structured_stage()
    elif selected_stage == "4. RAG Implementation":
        render_rag_stage()
    elif selected_stage == "5. Interactive Learning":
        render_interactive_stage()
    
    # Debug section at the bottom
    with st.expander("Debug Information"):
        st.json({
            "selected_stage": selected_stage,
            "transcript_loaded": st.session_state.transcript is not None,
            "chat_messages": len(st.session_state.messages)
        })

if __name__ == "__main__":
    main()
