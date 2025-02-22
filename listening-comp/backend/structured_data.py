from openai import OpenAI
import os
from typing import Optional, Dict, List
import json

class TranscriptStructurer:
    def __init__(self):
        """Initialize OpenAI client and set up the prompt for question extraction"""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.prompt = """
            Extract all the questions and answers in Spanish from the following transcript and return them in a structured JSON format as follows:

            ```json
            [
                {
                    "question": "[The question in Spanish, including all answer choices]",
                    "options": ["[Option 1]", "[Option 2]", "[Option 3]"],
                    "answer": "[The correct answer]",
                    "comment": "[Additional comment after the answer]"
                }
            ]
            
            Expected Output Example:
            ```json
            [
                {
                    "question": "¿Cuál es la posición de la Tierra con respecto al Sol? ¿La primera, La segunda o La tercera?",
                    "options": ["La primera", "La segunda", "La tercera"],
                    "answer": "La tercera",
                    "comment": "¡Es el tercer planeta después de Mercurio y Venus!"
                }
            ]
            ```
            """

    def _invoke_openai(self, transcript: str) -> Optional[str]:
        """Call OpenAI API to process the transcript"""
        try:
            print("\n=== Starting OpenAI API Call ===")
            print(f"Transcript length: {len(transcript)} characters")
            print("Sending request to OpenAI...")
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{
                    "role": "user", 
                    "content": f"{self.prompt}\n\nHere's the transcript:\n{transcript}"
                }],
                temperature=0.1  # Añadido para mayor consistencia
            )
            
            result = response.choices[0].message.content.strip()
            
            print("\n=== OpenAI Response ===")
            print("First 100 characters of response:")
            print(result[:100] + "...")
            print("\nFull response:")
            print("=" * 80)
            print(result)
            print("=" * 80)
            print("\nResponse length:", len(result))
            
            # Verificar si la respuesta parece JSON
            if not (result.startswith('[') or result.startswith('{')):
                print("\nWARNING: Response doesn't appear to start with JSON markers")
                print("Expected: Should start with '[' or '{'")
                print(f"Actual: Starts with '{result[:10]}'")
            
            return result
            
        except Exception as e:
            print("\n=== OpenAI API Error ===")
            print(f"Type: {type(e).__name__}")
            print(f"Error: {str(e)}")
            print("=" * 80)
            return None

    def structure_transcript(self, transcript: str) -> Optional[List[Dict]]:
        """Process transcript and return structured questions"""
        print("\n=== Processing Transcript ===")
        result = self._invoke_openai(transcript)
        
        if not result:
            print("No result received from OpenAI")
            return None
            
        try:
            print("\n=== Parsing JSON Response ===")
            print("Attempting to parse response as JSON...")
            
            # Limpiar los marcadores de código si existen
            result = result.replace('```json', '').replace('```', '').strip()
            
            parsed_json = json.loads(result)
            
            print("\nJSON Structure Overview:")
            print(f"Type: {type(parsed_json)}")
            print(f"Number of questions: {len(parsed_json) if isinstance(parsed_json, list) else 'Not a list'}")
            
            if isinstance(parsed_json, list):
                print("\nFirst question structure:")
                if parsed_json:
                    print(json.dumps(parsed_json[0], indent=2, ensure_ascii=False))
            
            return parsed_json
            
        except json.JSONDecodeError as e:
            print("\n=== JSON Parsing Error ===")
            print(f"Error position: line {e.lineno}, column {e.colno}")
            print(f"Error message: {str(e)}")
            print("\nProblematic content near error:")
            error_context = result[max(0, e.pos-50):min(len(result), e.pos+50)]
            print(f"...{error_context}...")
            return None

    def save_questions(self, questions: List[Dict], filename: str) -> bool:
        """Save structured questions to a JSON file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Save questions to JSON file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(questions, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving questions: {str(e)}")
            return False

    def load_transcript(self, filename: str) -> Optional[str]:
        """Load transcript from a file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading transcript: {str(e)}")
            return None

if __name__ == "__main__":
    print("Starting transcript processing...")
    structurer = TranscriptStructurer()
    
    print("\nLoading transcript file...")
    transcript = structurer.load_transcript("data/transcripts/R-kepxbu5fM.txt")
    if transcript:
        print("Transcript loaded successfully!")
        structured_questions = structurer.structure_transcript(transcript)
        if structured_questions:
            print("\nSaving structured questions...")
            success = structurer.save_questions(
                structured_questions, 
                "data/questions/R-kepxbu5fM.json"
            )
            if success:
                print("Questions saved successfully!")
            else:
                print("Failed to save questions.")
        else:
            print("Failed to structure transcript.")
    else:
        print("Failed to load transcript.")