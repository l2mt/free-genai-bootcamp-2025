import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.get_transcript import YouTubeTranscriptDownloader
import streamlit as st
from typing import Dict
import json
from collections import Counter
import re
from datetime import datetime
 
from backend.chat import OpenAIChat
from backend.question_generator import QuestionGenerator
from backend.vector_store import QuestionVectorStore

# Page config
st.set_page_config(
    page_title="Spanish Listening Practice",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'question_generator' not in st.session_state:
    st.session_state.question_generator = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'feedback' not in st.session_state:
    st.session_state.feedback = None
if 'selected_answer' not in st.session_state:
    st.session_state.selected_answer = None
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 0
if 'question_history' not in st.session_state:
    st.session_state.question_history = []

def render_header():
    """Render the header section"""
    st.title("🎧 Spanish Listening Practice")
    st.markdown("""
    Practice your Spanish comprehension with interactive questions.
    Select a topic and answer questions to improve your Spanish skills.
    """)

def render_sidebar():
    """Render the sidebar with question history"""
    with st.sidebar:
        st.header("📚 Question History")
        
        if not st.session_state.question_history:
            st.info("No questions answered yet")
            return
            
        for idx, hist in enumerate(reversed(st.session_state.question_history)):
            with st.expander(f"Question {len(st.session_state.question_history) - idx}", expanded=False):
                st.markdown(f"**Topic:** {hist['topic']}")
                st.markdown(f"**Result:** {'✅ Correct' if hist['correct'] else '❌ Incorrect'}")
                if st.button("Load Question", key=f"load_{idx}"):
                    st.session_state.current_question = hist['question']
                    st.session_state.feedback = None
                    st.session_state.selected_answer = None
                    st.rerun()

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
    
    # Initialize question generator if it doesn't exist
    if not st.session_state.question_generator:
        with st.spinner("Initializing question generator..."):
            try:
                st.session_state.question_generator = QuestionGenerator()
                st.success("System ready!")
            except Exception as e:
                st.error(f"Error initializing: {str(e)}")
                return
    
    # Metrics in one line
    col1, col2, col3, _ = st.columns([1, 1, 1, 3])
    with col1:
        st.metric("Questions", st.session_state.total_questions)
    with col2:
        st.metric("Correct", st.session_state.correct_answers)
    with col3:
        accuracy = (st.session_state.correct_answers / st.session_state.total_questions * 100) if st.session_state.total_questions > 0 else 0
        st.metric("Accuracy", f"{accuracy:.1f}%")
    
    # Topic selection
    st.subheader("Choose a Topic")
    topics = {
        "Astronomy": "🌟",
        "Geography": "🌍",
        "History": "📚",
        "Science": "🔬",
        "Art": "🎨",
        "Sports": "⚽",
        "Other": "🔄"
    }
    
    selected_topic = st.selectbox(
        "Select a topic:",
        options=list(topics.keys()),
        format_func=lambda x: f"{topics[x]} {x}",
        label_visibility="collapsed"
    )
    
    # Custom topic field
    if selected_topic == "Other":
        custom_topic = st.text_input("Enter a custom topic:")
        topic_to_use = custom_topic
    else:
        topic_to_use = selected_topic
    
    # Generate button
    generate_button = st.button("📝 Generate New Question", 
                              use_container_width=True, 
                              type="primary", 
                              disabled=not topic_to_use)
    
    # CSS styles remain the same
    st.markdown("""
    <style>
    .scenario-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 20px;
    }
    .correct-option {
        padding: 10px;
        border-radius: 5px;
        background-color: #90EE90;
        color: #000;
        margin-bottom: 8px;
    }
    .incorrect-option {
        padding: 10px;
        border-radius: 5px;
        background-color: #FFB6C1;
        color: #000;
        margin-bottom: 8px;
    }
    .normal-option {
        padding: 10px;
        border-radius: 5px;
        background-color: #f0f2f6;
        color: #000;
        margin-bottom: 8px;
        cursor: pointer;
    }
    .question-container {
        margin-top: 20px;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Question generation logic
    if topic_to_use and generate_button:
        with st.spinner(f"Generating question about '{topic_to_use}'..."):
            try:
                question = st.session_state.question_generator.generate_similar_question(topic_to_use)
                if question:
                    st.session_state.current_question = question
                    st.session_state.feedback = None
                    st.session_state.selected_answer = None
                    st.success("Question generated!")
                else:
                    st.warning("Could not generate a question. Try a different topic.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Display generated question
    if st.session_state.current_question:
        # Context and Question together
        st.markdown("**📖 Context**")
        context = st.session_state.current_question.get('Context', 'No context available')
        st.write(context)
        
        st.markdown("**❓ Question**")
        question = st.session_state.current_question.get('Question', 'No question available')
        st.write(question)
        
        # Options with improved display
        st.markdown("**🎯 Options**")
        options = st.session_state.current_question.get('Options', [])
        
        # Get correct answer if feedback exists
        correct_answer = None
        if st.session_state.feedback:
            correct_answer = st.session_state.feedback.get('correct_answer', 1)
        
        # Option columns
        option_cols = st.columns(2)
        for i, option in enumerate(options, 1):
            col_idx = (i - 1) % 2
            with option_cols[col_idx]:
                if st.session_state.feedback is None:
                    # Option buttons before selection
                    if st.button(
                        f"{i}. {option}",
                        key=f"option_{i}",
                        use_container_width=True
                    ):
                        st.session_state.selected_answer = i
                        try:
                            feedback = st.session_state.question_generator.get_feedback(
                                st.session_state.current_question, 
                                st.session_state.selected_answer
                            )
                            st.session_state.feedback = feedback
                            st.session_state.total_questions += 1
                            if feedback.get('correct', False):
                                st.session_state.correct_answers += 1
                            
                            # Add to history
                            history_entry = {
                                'topic': topic_to_use,
                                'question': st.session_state.current_question,
                                'correct': feedback.get('correct', False),
                                'timestamp': str(datetime.now())
                            }
                            st.session_state.question_history.append(history_entry)
                            
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                else:
                    # Show styled options after selection
                    option_style = "incorrect-option"
                    if i == correct_answer:
                        option_style = "correct-option"
                    
                    st.markdown(f'<div class="{option_style}">{i}. {option}</div>', unsafe_allow_html=True)
        
        # Show feedback
        if st.session_state.feedback:
            is_correct = st.session_state.feedback.get('correct', False)
            result_text = "✅ Correct!" if is_correct else "❌ Incorrect"
            st.markdown(f"### {result_text}")
            
            # Explanation
            explanation = st.session_state.feedback.get('explanation', 'No explanation available')
            st.write(explanation)
            
            # Next question button
            if st.button("📝 Next Question", 
                       key="next_question",
                       use_container_width=True,
                       type="primary"):
                st.session_state.current_question = None
                st.rerun()
    else:
        # Initial message
        st.info("👆 Select a topic and click 'Generate New Question' to start practicing.")

def main():
    render_header()
    render_sidebar()
    render_interactive_stage()

if __name__ == "__main__":
    main()