import google.generativeai as genai
from PIL import Image

def evaluate_handwriting(image, english_sentence, model):
    """
    Evaluates the handwritten Spanish translation using Gemini.
    
    Args:
        image: PIL Image containing the handwriting
        english_sentence: The original English sentence
        model: Configured Gemini model
        
    Returns:
        dict: Evaluation results including:
            - extracted_text: Text extracted from the image
            - is_correct: Whether the translation is correct
            - feedback: Detailed feedback
            - correct_translation: The correct translation
    """
    
    prompt = f"""
    Analyze this image containing a handwritten Spanish translation of the following English sentence:
    
    Original English sentence: "{english_sentence}"
    
    Please:
    1. Extract the handwritten Spanish text from the image
    2. Evaluate if the translation is grammatically correct and conveys the same meaning
    3. Provide specific feedback on errors (if any)
    4. Provide the correct translation for reference
    
    Return your response in structured format.
    """
    
    try:
        response = model.generate_content([prompt, image])
        
        # Process the response to extract structured information
        # This is simplified and will be improved in later steps
        return {
            "extracted_text": "Extracted text", # Full parsing will be implemented later
            "is_correct": False,
            "feedback": response.text,
            "correct_translation": "Reference correct translation"
        }
    except Exception as e:
        return {
            "error": str(e),
            "extracted_text": None,
            "is_correct": False,
            "feedback": f"Error analyzing the image: {str(e)}",
            "correct_translation": None
        } 