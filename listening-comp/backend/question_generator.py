import json
import google.generativeai as genai
from typing import Dict, List, Optional
from backend.vector_store import QuestionVectorStore
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class QuestionGenerator:
    def __init__(self):
        self.vector_store = QuestionVectorStore()
        # Configure Gemini API
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if not google_api_key:
            print("Warning: GOOGLE_API_KEY not found in environment variables")
            google_api_key = QuestionVectorStore._google_api_key
        
        if not google_api_key:
            raise ValueError("No se pudo encontrar GOOGLE_API_KEY. Por favor, configura esta variable en el archivo .env")
            
        genai.configure(api_key=google_api_key)
        self.model = "gemini-1.5-flash"

    def _invoke_gemini(self, prompt: str) -> Optional[str]:
        try:
            # Configurar el modelo con parámetros seguros
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            
            # Inicializar el modelo
            model = genai.GenerativeModel(
                model_name=self.model,
                generation_config=generation_config
            )
            
            # Ejecutar la generación
            response = model.generate_content(prompt)
            
            # Extraer el texto de la respuesta
            if hasattr(response, 'text'):
                return response.text
            elif hasattr(response, 'parts') and len(response.parts) > 0:
                return response.parts[0].text
            else:
                print("Error: Formato de respuesta inesperado")
                return None
                
        except Exception as e:
            print(f"Error invoking Gemini: {str(e)}")
            return None

    def _translate_topic_to_spanish(self, topic: str) -> str:
        """Translate topic from English to Spanish if needed"""
        # Common topics translation dictionary
        topic_translations = {
            "Astronomy": "Astronomía",
            "Geography": "Geografía",
            "History": "Historia",
            "Science": "Ciencia",
            "Art": "Arte",
            "Sports": "Deportes",
            "Other": "Otro"
        }
        
        # Check if the topic is in our dictionary
        if topic in topic_translations:
            return topic_translations[topic]
        
        # For custom topics, use Gemini to translate
        try:
            prompt = f"Translate this topic from English to Spanish. Return ONLY the Spanish translation without any additional text or explanation: '{topic}'"
            translation = self._invoke_gemini(prompt)
            if translation:
                # Clean the response
                translation = translation.strip().strip('"\'')
                print(f"Translated topic '{topic}' to '{translation}'")
                return translation
            return topic  # Return original if translation failed
        except Exception as e:
            print(f"Error translating topic: {str(e)}")
            return topic  # Return original topic in case of error

    def generate_similar_question(self, topic: str) -> Dict:
        print(f"Looking for questions similar to: {topic}")
        
        # Translate topic to Spanish if it's in English
        spanish_topic = self._translate_topic_to_spanish(topic)
        print(f"Searching with Spanish topic: {spanish_topic}")
        
        similar_questions = self.vector_store.search_similar_questions(spanish_topic, n_results=3)
        
        if not similar_questions:
            print("No similar questions found")
            return None
        
        print(f"Found {len(similar_questions)} similar questions")
        for q in similar_questions:
            print(f"Question: {q.get('question', '')[:50]}...")
            
        context = self._build_context(similar_questions)
        print(f"Context built, length: {len(context)}")
        prompt = self._build_prompt(context, spanish_topic)
        print("Invoking Gemini API...")
        response = self._invoke_gemini(prompt)
        
        if not response:
            print("No response received from Gemini")
            return None

        print(f"Response received (length: {len(response)})")
        return self._parse_response(response)

    def _build_context(self, similar_questions: List[Dict]) -> str:
        """Build context from similar questions to guide the model"""
        context = []
        for q in similar_questions:
            question_text = q.get('question', '')
            answer = q.get('answer', '')
            correct_option = q.get('correct_option', '')
            options = q.get('options', [])
            
            if options and correct_option:
                context.append(f"QUESTION: {question_text}")
                for i, option in enumerate(options, 1):
                    context.append(f"OPTION {i}: {option}")
                context.append(f"CORRECT OPTION: {correct_option}")
                if answer:
                    context.append(f"ANSWER EXPLANATION: {answer}")
            else:
                context.append(f"Q: {question_text}")
                if answer:
                    context.append(f"A: {answer}")
            
            context.append("---")
            
        return "\n".join(context)
        
    def _build_prompt(self, context: str, topic: str) -> str:
        """Build prompt for generating a question based on context"""
        return f"""You are a Spanish language learning assistant that creates engaging multiple-choice quiz questions.

INSTRUCTIONS:
1. Create a multiple-choice question in Spanish related to the topic: {topic}
2. The question should test the user's Spanish comprehension while teaching them about the topic
3. Make the question challenging but fair, like those in the examples below
4. Include 3-4 possible answers in Spanish with only one correct answer
5. Add a brief scenario or context in Spanish to make the question more interesting
6. Return ONLY a JSON object with the following fields:
   - Question: The question text in Spanish
   - Options: Array of possible answers in Spanish
   - CorrectAnswer: Number of the correct option (1-indexed)
   - Context: A brief scenario that introduces the question in Spanish

EXAMPLES FROM THE DATABASE:
{context}

FORMAT YOUR RESPONSE AS VALID JSON:
{{
  "Question": "Your question in Spanish",
  "Options": ["Option 1 in Spanish", "Option 2 in Spanish", "Option 3 in Spanish"],
  "CorrectAnswer": 1,
  "Context": "Brief scenario in Spanish"
}}
"""

    def _parse_response(self, response: str) -> Dict:
        """Parse the model response into a structured question format"""
        try:
            # Try to extract JSON part from response
            json_start = response.find("{")
            json_end = response.rfind("}")
            
            if json_start != -1 and json_end != -1:
                json_str = response[json_start:json_end + 1]
                data = json.loads(json_str)
                
                return {
                    "Question": data.get("Question", ""),
                    "Options": data.get("Options", []),
                    "CorrectAnswer": data.get("CorrectAnswer", 1),
                    "Context": data.get("Context", "")
                }
            else:
                print("Failed to extract JSON from response")
                return None
                
        except Exception as e:
            print(f"Error parsing response: {str(e)}")
            print(f"Response: {response}")
            return None
            
    def get_feedback(self, question: Dict, selected_answer: int) -> Dict:
        """Get feedback for the user's answer"""
        if not question:
            return {"correct": False, "explanation": "Question not available"}
            
        # Check if the answer is correct
        correct_answer = question.get('CorrectAnswer', 1)
        is_correct = selected_answer == correct_answer
        
        # Prepare prompt for feedback
        context = f"""
Question in Spanish: {question.get('Question', '')}

Options:
{chr(10).join([f"{i+1}. {option}" for i, option in enumerate(question.get('Options', []))])}

Correct answer number: {correct_answer}
Selected answer number: {selected_answer}
"""
        prompt = f"""You are a helpful Spanish language tutor providing feedback on a student's answer to a multiple-choice question.

CONTEXT:
{context}

TASK:
1. Determine if the student's answer is correct or incorrect
2. Provide a helpful explanation in English about why the answer is correct or incorrect
3. Include some educational points about both the content of the question and relevant Spanish vocabulary or grammar
4. Keep your explanation concise but informative
5. Return ONLY a JSON object with the following fields:
   - correct: boolean (true if the student's answer matches the correct answer)
   - explanation: string with your explanation in English
   - correct_answer: number of the correct option

FORMAT YOUR RESPONSE AS VALID JSON:
{{
  "correct": true/false,
  "explanation": "Your explanation in English",
  "correct_answer": {correct_answer}
}}
"""
        print(f"Prompt generated for feedback (length: {len(prompt)})")
        
        # Get response from model
        response = self._invoke_gemini(prompt)
        if not response:
            return {"correct": is_correct, "explanation": "Unable to generate detailed feedback"}
            
        # Parse the response
        try:
            # Try to extract JSON part from response
            print(f"Gemini response: {response[:100]}...")
            json_start = response.find("{")
            json_end = response.rfind("}")
            
            if json_start != -1 and json_end != -1:
                json_str = response[json_start:json_end + 1]
                data = json.loads(json_str)
                
                return {
                    "correct": data.get("correct", is_correct),
                    "explanation": data.get("explanation", "No explanation provided"),
                    "correct_answer": data.get("correct_answer", correct_answer)
                }
            else:
                return {"correct": is_correct, "explanation": "Unable to parse feedback"}
                
        except Exception as e:
            print(f"Error parsing feedback: {str(e)}")
            return {"correct": is_correct, "explanation": "Error generating feedback"}