from PIL import Image
import io
import streamlit as st

def process_uploaded_image(uploaded_file):
    """
    Processes an image uploaded by the user.
    
    Args:
        uploaded_file: The file uploaded by the user through Streamlit
        
    Returns:
        PIL.Image: Processed image ready to send to Gemini
    """
    if uploaded_file is None:
        return None
    
    try:
        # Read image
        image_bytes = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Perform basic pre-processing
        # Resize if necessary (keep below API limits)
        max_size = 1600
        if max(image.size) > max_size:
            # Resize while maintaining aspect ratio
            ratio = max_size / max(image.size)
            new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
            image = image.resize(new_size, Image.LANCZOS)
        
        return image
    
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None 