import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io
import random
from utils.gemini_utils import evaluate_handwriting
from utils.image_utils import process_uploaded_image
from data.sentences import get_sentence_groups, get_sentences_from_group

# Page configuration
st.set_page_config(
    page_title="Spanish Language Practice",
    page_icon="🇪🇸",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Apply custom CSS styles
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
    }
    .sentence-display {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        font-size: 1.5rem;
        text-align: center;
        color: #000;
        font-weight: bold;
        border: 2px solid #1E88E5;
    }
    .instruction {
        font-size: 1.2rem;
        color: #555;
        margin: 15px 0;
    }
    .feedback-correct {
        background-color: #CCFFD8;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #00C853;
    }
    .feedback-incorrect {
        background-color: #FFECEB;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #FF5252;
    }
</style>
""", unsafe_allow_html=True)

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Verify that the API key is available
if not GOOGLE_API_KEY:
    st.error("❌ Google API key not found in .env file")
    st.stop()

# Configure the Gemini model
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    # Model for image analysis
    vision_model = genai.GenerativeModel('gemini-1.5-flash')
    st.session_state.setup_complete = True
except Exception as e:
    st.error(f"❌ Error configuring Gemini model: {str(e)}")
    st.session_state.setup_complete = False

# Application title
st.markdown("<h1 class='main-header'>🇪🇸 Spanish Language Practice</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Practice your Spanish writing skills with English phrases</p>", unsafe_allow_html=True)

# Señal de que la aplicación está funcionando correctamente
st.success("✅ Application is running correctly. Select a work group below to begin.")

# Initialize session state variables if they don't exist
if 'current_sentence' not in st.session_state:
    st.session_state.current_sentence = None
if 'current_group' not in st.session_state:
    st.session_state.current_group = None
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_attempts' not in st.session_state:
    st.session_state.total_attempts = 0
if 'feedback' not in st.session_state:
    st.session_state.feedback = None
if 'image_result' not in st.session_state:
    st.session_state.image_result = None

# Function to generate a new random sentence
def get_new_sentence(group_name):
    sentences = get_sentences_from_group(group_name)
    if sentences:
        return random.choice(sentences)
    return None

# Function to reset the current sentence
def reset_current_sentence():
    st.session_state.current_sentence = get_new_sentence(st.session_state.current_group)
    st.session_state.feedback = None
    st.session_state.image_result = None

# Function to handle group change
def change_group():
    st.session_state.current_sentence = get_new_sentence(st.session_state.current_group)
    st.session_state.feedback = None
    st.session_state.image_result = None

# Check that everything is configured correctly
if not st.session_state.get('setup_complete', False):
    st.warning("⚠️ There are issues with the environment setup")
    st.stop()

# Sidebar with information and statistics
with st.sidebar:
    st.header("Information")
    st.info("""
    This app helps you practice Spanish writing.
    
    1. Select a work group
    2. Write the Spanish translation on paper
    3. Upload a photo or use the webcam
    4. Get feedback on your translation
    """)
    
    st.header("Statistics")
    if st.session_state.total_attempts > 0:
        accuracy = (st.session_state.score / st.session_state.total_attempts) * 100
        st.metric("Accuracy", f"{accuracy:.1f}%")
    st.metric("Score", st.session_state.score)
    st.metric("Attempts", st.session_state.total_attempts)
    
    if st.button("Reset Statistics"):
        st.session_state.score = 0
        st.session_state.total_attempts = 0
        st.rerun()

# Section 1: Work Group Selection
st.header("1. Select a Work Group")
groups = get_sentence_groups()
selected_group = st.selectbox(
    "Work group:",
    options=groups,
    index=groups.index(st.session_state.current_group) if st.session_state.current_group in groups else 0,
    on_change=change_group,
    key="group_selector"
)

# Update the current group
if st.session_state.current_group != selected_group:
    st.session_state.current_group = selected_group
    # Debug - Log grupo seleccionado
    st.write(f"Debug - Changed group to: {selected_group}")
    reset_current_sentence()

# If there is no current sentence, get a new one
if st.session_state.current_sentence is None:
    # Debug - Log cuando se necesita generar una nueva oración
    st.write("Debug - No current sentence, getting a new one")
    reset_current_sentence()
    
# Debug - Ver el estado actual
st.write(f"Debug - Current session state: Group={st.session_state.current_group}, Has sentence: {st.session_state.current_sentence is not None}")

# Section 2: Display the sentence to translate
st.header("2. Translate this sentence to Spanish")
if st.session_state.current_sentence:
    english_text = st.session_state.current_sentence["english"]
    # Debug information
    st.write(f"Debug - Current sentence: {english_text}")
    
    # Mostrar la oración de múltiples maneras para asegurar visibilidad
    st.markdown(f"<div class='sentence-display'>{english_text}</div>", unsafe_allow_html=True)
    
    # Adicional: mostrar también con componentes nativos de Streamlit
    st.success(f"**Translate this:** {english_text}")
    
    st.markdown("<p class='instruction'>Write the Spanish translation on paper, then upload a photo or use the webcam.</p>", unsafe_allow_html=True)
else:
    st.error("Could not load a sentence. Please select another work group.")
    st.stop()

# Section 3: Upload image or use webcam
st.header("3. Upload a photo of your written translation")
upload_option = st.radio(
    "Select how you want to upload your translation:",
    options=["Upload image", "Use webcam"],
    horizontal=True
)

uploaded_image = None

if upload_option == "Upload image":
    uploaded_file = st.file_uploader("Upload an image of your written translation", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        uploaded_image = process_uploaded_image(uploaded_file)
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded image", use_column_width=True)
else:  # Use webcam
    st.info("Make sure your camera is connected and working.")
    webcam_image = st.camera_input("Take a photo of your written translation")
    if webcam_image:
        uploaded_image = process_uploaded_image(webcam_image)
        if uploaded_image:
            st.success("Image captured successfully!")

# Section 4: Evaluate the translation
st.header("4. Evaluate your translation")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    evaluate_button = st.button(
        "Evaluate Translation", 
        disabled=uploaded_image is None,
        type="primary",
        use_container_width=True
    )

# Process evaluation
if evaluate_button and uploaded_image:
    with st.spinner("Analyzing your translation..."):
        # Get the English sentence and its correct translation
        english_text = st.session_state.current_sentence["english"]
        correct_spanish = st.session_state.current_sentence["spanish"]
        
        # Evaluate the image with Gemini
        result = evaluate_handwriting(
            image=uploaded_image,
            english_sentence=english_text,
            model=vision_model
        )
        
        # Save results in session state
        st.session_state.image_result = result
        
        # Increment attempt counter
        st.session_state.total_attempts += 1
        
        # Update score if correct
        if result.get("is_correct", False):
            st.session_state.score += 1
        
        # Prepare feedback
        feedback_html = ""
        if "error" in result:
            feedback_html = f"<div class='feedback-incorrect'>Error: {result['error']}</div>"
        elif result.get("is_correct", False):
            feedback_html = f"""
            <div class='feedback-correct'>
                <h3>Correct! 👏</h3>
                <p>Your translation: {result.get('extracted_text', '')}</p>
                <p>Correct translation: {correct_spanish}</p>
            </div>
            """
        else:
            feedback_html = f"""
            <div class='feedback-incorrect'>
                <h3>Needs improvement 🤔</h3>
                <p>Your translation: {result.get('extracted_text', '')}</p>
                <p>Correct translation: {correct_spanish}</p>
                <p>Feedback: {result.get('feedback', '')}</p>
            </div>
            """
        
        st.session_state.feedback = feedback_html

# Show feedback if it exists
if st.session_state.feedback:
    st.markdown(st.session_state.feedback, unsafe_allow_html=True)
    
    # Button to continue with another sentence
    if st.button("Continue with another sentence", type="primary"):
        reset_current_sentence()
        st.rerun() 