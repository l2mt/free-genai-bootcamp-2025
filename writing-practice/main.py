import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io
import random
from utils.gemini_utils import evaluate_handwriting, generate_sentence_with_gemini
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
    .ai-badge {
        background-color: #7B1FA2;
        color: white;
        font-size: 0.8rem;
        padding: 3px 8px;
        border-radius: 10px;
        display: inline-block;
        margin-left: 10px;
    }
    .instruction {
        font-size: 1.2rem;
        color: #555;
        margin: 15px 0;
    }
    .feedback-correct {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 15px;
        margin: 20px 0;
        border-radius: 5px;
    }
    .feedback-incorrect {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 15px;
        margin: 20px 0;
        border-radius: 5px;
        color: #000000;
    }
    .feedback-correct h3, .feedback-incorrect h3 {
        margin-top: 0;
        font-size: 1.2rem;
        font-weight: bold;
        color: #000000;
    }
    .feedback-correct p, .feedback-incorrect p {
        margin: 8px 0;
        font-size: 1rem;
        color: #000000;
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
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False  # Debug mode is disabled by default

# Helper function to display debug messages
def debug(message):
    if st.session_state.debug_mode:
        st.write(f"Debug - {message}")

# Function to generate a new random sentence
def get_new_sentence(group_name, use_ai=True):
    """
    Generates a new sentence based on the selected work group.
    
    Args:
        group_name: Name of the group or custom topic
        use_ai: If True, tries to use Gemini to generate the sentence
        
    Returns:
        dict: Dictionary with 'english' and 'spanish' keys
    """
    # Check if it's a custom topic (not in predefined groups)
    is_custom_topic = group_name not in get_sentence_groups()
    
    # If it's a custom topic or we want to use AI (and have connection)
    if use_ai and (is_custom_topic or random.random() > 0.3):  # 70% chance of using AI for predefined topics
        try:
            # Show generation message
            with st.spinner(f"Generating a sentence about '{group_name}' with AI..."):
                generated_sentence = generate_sentence_with_gemini(group_name, vision_model)
                
                if generated_sentence:
                    # Add a marker to know it was generated by AI
                    generated_sentence["generated_by_ai"] = True
                    return generated_sentence
        except Exception as e:
            # If it fails, show an error message and use the predefined version
            st.warning(f"Could not generate a sentence with AI: {str(e)}. Using predefined sentences as fallback.")
    
    # Use predefined sentences as fallback
    if not is_custom_topic:
        sentences = get_sentences_from_group(group_name)
        if sentences:
            return random.choice(sentences)
    
    # If it's a custom topic and AI generation failed, create a generic sentence
    return {
        "english": f"I am learning about {group_name}.",
        "spanish": f"Estoy aprendiendo sobre {group_name}.",
        "fallback": True
    }

# Function to reset the current sentence
def reset_current_sentence():
    """Limpia completamente el estado actual y genera una nueva oración"""
    # Get the use_ai value from the session or use True as default
    use_ai = st.session_state.get('use_ai', True)
    
    # Limpiar completamente todos los estados relacionados con la pregunta actual
    st.session_state.current_sentence = None
    st.session_state.feedback = None
    st.session_state.image_result = None
    
    # Limpiar elementos de la UI
    if 'uploaded_file' in st.session_state:
        del st.session_state.uploaded_file
    if 'webcam_image' in st.session_state:
        del st.session_state.webcam_image
    if 'file_uploader' in st.session_state:
        del st.session_state.file_uploader
    if 'webcam_input' in st.session_state:
        del st.session_state.webcam_input
        
    # Solo generar nueva oración si hay un grupo seleccionado
    if st.session_state.current_group:
        # Generar nueva oración
        st.session_state.current_sentence = get_new_sentence(st.session_state.current_group, use_ai)
        return True
    
    return False

# Function to handle group change
def change_group():
    """Actualiza el grupo actual y limpia el estado"""
    # Tomamos nota del grupo antes de que se actualice
    previous_group = st.session_state.current_group
    new_group = st.session_state.group_selector
    
    # Si el grupo realmente cambió
    if previous_group != new_group:
        debug(f"Grupo cambiado de {previous_group} a {new_group}")
        # Actualizar el grupo en session_state
        st.session_state.current_group = new_group
        # Limpiar completamente - ya no generamos automáticamente
        st.session_state.current_sentence = None
        st.session_state.feedback = None
        st.session_state.image_result = None
        
        # Limpiar elementos de la UI
        for key in ['uploaded_file', 'webcam_image', 'file_uploader', 'webcam_input']:
            if key in st.session_state:
                del st.session_state[key]

# Check that everything is configured correctly
if not st.session_state.get('setup_complete', False):
    st.warning("⚠️ There are issues with the environment setup")
    st.stop()

# Sidebar with information and statistics
with st.sidebar:
    st.header("Information")
    st.info("""
    This app helps you practice Spanish writing.
    
    1. Select a work group or custom topic
    2. Write the Spanish translation on paper
    3. Upload a photo or use the webcam
    4. Get feedback on your translation
    """)
    
    st.header("Settings")
    st.session_state.use_ai = st.checkbox(
        "Generate sentences with AI", 
        value=True,
        help="Disable this option if you prefer to use only predefined sentences or if you have connection issues."
    )
    
    # Añadimos opción de diagnóstico
    st.session_state.debug_mode = st.checkbox(
        "Show debugging information", 
        value=st.session_state.get('debug_mode', False),
        help="Enable this to see detailed information about the application's operation"
    )
    
    # Añadimos sección de diagnóstico
    if st.session_state.debug_mode:
        st.header("Diagnosis")
        if st.session_state.get('image_result'):
            st.subheader("Last Evaluation Result")
            st.json(st.session_state.image_result)
    
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
st.header("1. Select a Work Group or Enter a Custom Topic")

# Opción para elegir entre grupos predefinidos o tema personalizado
selection_mode = st.radio(
    "Selection mode:",
    options=["Predefined groups", "Custom topic"],
    horizontal=True,
    key="selection_mode"
)

if selection_mode == "Predefined groups":
    # Mostrar los grupos predefinidos
    groups = get_sentence_groups()
    selected_group = st.selectbox(
        "Work group:",
        options=groups,
        index=groups.index(st.session_state.current_group) if st.session_state.current_group in groups else 0,
        on_change=change_group,
        key="group_selector"
    )
else:
    # Campo para ingresar un tema personalizado
    custom_topic = st.text_input(
        "Enter a custom topic (e.g., 'animals', 'technology', 'sports'):",
        key="custom_topic"
    )
    
    if st.button("Create sentence with this topic", key="custom_topic_button"):
        if custom_topic:
            # Actualizar el grupo actual con el tema personalizado
            st.session_state.current_group = custom_topic
            # Limpiar el estado y obtener una nueva oración para el tema personalizado
            success = reset_current_sentence()
            # Mostrar confirmación
            if success:
                st.success(f"✅ Custom topic selected: {custom_topic}")
            else:
                st.warning(f"Custom topic selected but could not generate a sentence.")
            # Recargar la página para mostrar la nueva oración
            st.rerun()
        else:
            st.error("Please enter a topic to generate a sentence.")
    
    selected_group = st.session_state.current_group

# Update the current group if using predefined groups
if selection_mode == "Predefined groups" and st.session_state.current_group != selected_group:
    st.session_state.current_group = selected_group
    # Debug - Log selected group
    debug(f"Changed group to: {selected_group}")
    # Limpiar la oración actual para forzar la selección manual
    st.session_state.current_sentence = None

# Mostrar un botón para generar una nueva oración
if st.session_state.current_group:
    if st.button("Generate New Sentence", key="generate_new_sentence"):
        # Solo aquí llamamos a reset_current_sentence para generar una nueva oración
        success = reset_current_sentence()
        if success:
            st.success(f"Generated new sentence for: {st.session_state.current_group}")
        else:
            st.warning(f"Could not generate a sentence for: {st.session_state.current_group}")
        st.rerun()

# Si ya hay una oración actual, la mostramos, pero no generamos una nueva automáticamente
# Si no hay una oración actual y hay un grupo seleccionado, mostramos un mensaje para que generen una
if st.session_state.current_sentence is None and st.session_state.current_group:
    st.info(f"Group '{st.session_state.current_group}' selected. Click 'Generate New Sentence' above to get a sentence to translate.")
    # No generamos automáticamente
    # Debug - View current state
    debug(f"Current session state: Group={st.session_state.current_group}, Has sentence: {st.session_state.current_sentence is not None}")
elif st.session_state.current_sentence is None:
    st.info("Please select a work group or enter a custom topic, then click 'Generate New Sentence'.")
else:
    # Debug - View current state
    debug(f"Current session state: Group={st.session_state.current_group}, Has sentence: {st.session_state.current_sentence is not None}")
    
    # Section 2: Display the sentence to translate - SOLO se muestra cuando hay una oración
    st.header("2. Translate this sentence to Spanish")
    english_text = st.session_state.current_sentence["english"]
    # Debug information
    debug(f"Current sentence: {english_text}")
    
    # Verificar si la oración fue generada por IA
    is_ai_generated = st.session_state.current_sentence.get("generated_by_ai", False)
    
    # Mostrar la oración con un badge si fue generada por IA
    if is_ai_generated:
        st.markdown(f"<div class='sentence-display'>{english_text} <span class='ai-badge'>AI</span></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='sentence-display'>{english_text}</div>", unsafe_allow_html=True)
    
    # Adicional: mostrar también con componentes nativos de Streamlit
    st.success(f"**Translate this:** {english_text}")
    
    st.markdown("<p class='instruction'>Write the Spanish translation on paper, then upload a photo or use the webcam.</p>", unsafe_allow_html=True)

    # Section 3: Upload image or use webcam - SOLO se muestra cuando hay una oración
    st.header("3. Upload a photo of your written translation")
    upload_option = st.radio(
        "Select how you want to upload your translation:",
        options=["Upload image", "Use webcam"],
        horizontal=True
    )

    uploaded_image = None

    if upload_option == "Upload image":
        uploaded_file = st.file_uploader("Upload an image of your written translation", type=["jpg", "jpeg", "png"], key="file_uploader")
        if uploaded_file:
            uploaded_image = process_uploaded_image(uploaded_file)
            if uploaded_image:
                st.image(uploaded_image, caption="Uploaded image", use_column_width=True)
                # Save in session_state for later cleanup
                st.session_state.uploaded_file = uploaded_file
    else:  # Use webcam
        st.info("Make sure your camera is connected and working.")
        webcam_image = st.camera_input("Take a photo of your written translation", key="webcam_input")
        if webcam_image:
            uploaded_image = process_uploaded_image(webcam_image)
            if uploaded_image:
                st.success("Image captured successfully!")
                # Save in session_state for later cleanup
                st.session_state.webcam_image = webcam_image

    # Section 4: Evaluate the translation - SOLO se muestra cuando hay una oración
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
                feedback_html = f"""
                <div class='feedback-incorrect'>
                    <h3>Analysis Error</h3>
                    <p><strong>Error message:</strong> {result['error']}</p>
                </div>
                """
            elif result.get("is_correct", False):
                feedback_html = f"""
                <div class='feedback-correct'>
                    <h3>Correct! 👏</h3>
                    <p><strong>Your translation:</strong> {result.get('extracted_text', '')}</p>
                    <p><strong>Correct translation:</strong> {correct_spanish}</p>
                </div>
                """
            else:
                # Comprobación adicional para detectar si el análisis es positivo aunque falte VERDICT: CORRECT
                response_text = result.get('feedback', '')
                has_positive_indicators = (
                    "grammatically correct" in response_text.lower() and 
                    "perfectly" in response_text.lower() and 
                    "no errors" in response_text.lower()
                )
                
                if has_positive_indicators:
                    feedback_html = f"""
                    <div class='feedback-correct'>
                        <h3>Correct! 👏</h3>
                        <p><strong>Your translation:</strong> {result.get('extracted_text', '')}</p>
                        <p><strong>Correct translation:</strong> {correct_spanish}</p>
                        <p><em>Note: The system detected your translation as correct based on feedback context.</em></p>
                    </div>
                    """
                else:
                    feedback_html = f"""
                    <div class='feedback-incorrect'>
                        <h3>Needs improvement 🤔</h3>
                        <p><strong>Your translation:</strong> {result.get('extracted_text', '')}</p>
                        <p><strong>Correct translation:</strong> {correct_spanish}</p>
                        <p><strong>Feedback:</strong> {result.get('feedback', '')}</p>
                    </div>
                    """
                
                # Si el modo debug está activo, añadimos información de diagnóstico
                if st.session_state.debug_mode:
                    debug_info = f"""
                    <div style='background-color: #f0f0f0; padding: 10px; margin-top: 15px; border-left: 5px solid #555;'>
                        <h4>Diagnostic Information</h4>
                        <p><strong>Is Correct Flag:</strong> {result.get('is_correct', False)}</p>
                        <p><strong>Has Positive Indicators:</strong> {has_positive_indicators}</p>
                    </div>
                    """
                    feedback_html += debug_info
            
            st.session_state.feedback = feedback_html

    # Show feedback if it exists
    if st.session_state.feedback:
        st.markdown(st.session_state.feedback, unsafe_allow_html=True)
        
        # Button to continue with another sentence
        if st.button("Continue with another sentence", type="primary", key="continue_button"):
            # Limpiamos completamente el estado pero SIN generar una nueva oración
            # Esto asegura que volvamos al paso 1
            
            # Guardar el grupo actual para mantenerlo seleccionado
            current_group = st.session_state.current_group
            
            # Limpiar todos los estados relacionados con la pregunta actual
            st.session_state.current_sentence = None
            st.session_state.feedback = None
            st.session_state.image_result = None
            
            # Limpiar elementos de la UI
            for key in ['uploaded_file', 'webcam_image', 'file_uploader', 'webcam_input']:
                if key in st.session_state:
                    del st.session_state[key]
                
            # Restaurar el grupo actual
            st.session_state.current_group = current_group
            
            # Confirmar que se ha reiniciado
            st.success(f"Ready to practice with '{current_group}' again. Click 'Generate New Sentence' to continue.")
            
            # Recargar la aplicación para mostrar solo el paso 1
            st.rerun() 