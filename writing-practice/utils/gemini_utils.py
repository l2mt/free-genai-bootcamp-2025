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
    
    Please respond with the following EXACTLY formatted sections:

    1. Handwritten Spanish Text: [Extract the text visible in the image]
    
    2. Grammatical Correctness and Meaning: [Evaluate if the translation is grammatically correct and conveys the same meaning]
    
    3. Specific Feedback on Errors: [Provide specific feedback on any errors, or state "There are no grammatical errors" if correct]
    
    4. Correct Translation: [Provide the correct Spanish translation of the English sentence]
    
    5. VERDICT: [CORRECT or INCORRECT - Use CORRECT only if the translation is fully accurate with no grammatical or meaning errors]
    
    IMPORTANT: Always include all 5 numbered sections and maintain this exact format.
    """
    
    try:
        print("[LOG] Enviando solicitud a Gemini...")
        response = model.generate_content([prompt, image])
        response_text = response.text
        
        # Log the complete response for debugging
        print("[LOG] Respuesta completa de Gemini:")
        print("-"*50)
        print(response_text)
        print("-"*50)
        
        # Extract verdict to determine correctness
        is_correct = "VERDICT: CORRECT" in response_text
        print(f"[LOG] ¿Contiene 'VERDICT: CORRECT'?: {is_correct}")
        
        # Check for alternative positive indicators
        alternative_correct = ("grammatically correct" in response_text.lower() and 
                              "perfectly" in response_text.lower() and 
                              "no errors" in response_text.lower() and
                              not "VERDICT: INCORRECT" in response_text)
        
        print(f"[LOG] Indicadores alternativos de corrección: {alternative_correct}")
        
        # If the model says it's correct but doesn't include the exact VERDICT format
        if alternative_correct and not is_correct:
            print("[LOG] La respuesta parece indicar que es correcta por contexto, aunque falta VERDICT")
            is_correct = True
        
        # Try to extract text from various formats
        extracted_text = None
        correct_translation = None
        
        # Extract based on common patterns
        if "1. Handwritten Spanish Text:" in response_text:
            print("[LOG] Extrayendo texto usando patrón 'Handwritten Spanish Text:'")
            extracted_text = response_text.split("1. Handwritten Spanish Text:")[1].split("\n")[0].strip()
        elif "handwritten Spanish text:" in response_text.lower():
            print("[LOG] Extrayendo texto usando patrón alternativo 'handwritten Spanish text:'")
            parts = response_text.lower().split("handwritten Spanish text:")
            if len(parts) > 1:
                extracted_text = parts[1].split("\n")[0].strip()
        
        # Extract correct translation
        if "4. Correct Translation:" in response_text:
            print("[LOG] Extrayendo traducción correcta usando patrón 'Correct Translation:'")
            correct_translation = response_text.split("4. Correct Translation:")[1].split("\n")[0].strip()
        elif "correct translation:" in response_text.lower():
            print("[LOG] Extrayendo traducción usando patrón alternativo 'correct translation:'")
            parts = response_text.lower().split("correct translation:")
            if len(parts) > 1:
                correct_translation = parts[1].split("\n")[0].strip()
        
        print(f"[LOG] Texto extraído: '{extracted_text}'")
        print(f"[LOG] Traducción correcta extraída: '{correct_translation}'")
        
        # Process the response to extract structured information
        result = {
            "extracted_text": extracted_text or "Texto no detectado claramente",
            "is_correct": is_correct,
            "feedback": response_text,
            "correct_translation": correct_translation or "No se pudo determinar la traducción correcta"
        }
        
        print(f"[LOG] Resultado final: correcto={is_correct}")
        return result
    except Exception as e:
        print(f"[ERROR] Error al analizar la imagen: {str(e)}")
        return {
            "error": str(e),
            "extracted_text": None,
            "is_correct": False,
            "feedback": f"Error analyzing the image: {str(e)}",
            "correct_translation": None
        }

def generate_sentence_with_gemini(topic, model):
    """
    Genera una oración en inglés y su traducción al español usando Gemini, basado en un tema.
    
    Args:
        topic: El tema sobre el que generar la oración
        model: Modelo Gemini configurado
        
    Returns:
        dict: Diccionario con las claves 'english' y 'spanish', o None si hay un error
    """
    
    prompt = f"""
    Genera una sola oración en inglés y su traducción al español sobre el tema: "{topic}".
    
    La oración debe ser simple, adecuada para practicar español básico o intermedio.
    No generes listas, diálogos ni párrafos, solo UNA oración sencilla.
    
    Devuelve SOLAMENTE un objeto JSON con este formato exacto:
    {{
      "english": "Oración en inglés",
      "spanish": "Traducción en español"
    }}
    
    No incluyas ningún texto adicional, explicación, introducción, ni formato markdown.
    """
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Extraer el JSON de la respuesta
        import json
        import re
        
        # Eliminar caracteres de formato si existen
        json_text = re.sub(r'^```json|```$', '', response_text).strip()
        
        # Convertir a diccionario
        result = json.loads(json_text)
        
        if 'english' in result and 'spanish' in result:
            return result
        else:
            raise ValueError("Respuesta del modelo no tiene el formato esperado")
            
    except Exception as e:
        print(f"Error al generar oración con Gemini: {str(e)}")
        return None 