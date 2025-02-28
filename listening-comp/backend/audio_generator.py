import boto3
import json
import os
from typing import Dict, List, Tuple
import tempfile
import subprocess
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class AudioGenerator:
    def __init__(self):
        # AWS Polly client
        self.polly = boto3.client('polly',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        
        # Define Spanish voices by gender (standard engine)
        self.voices = {
            'male': ['Miguel'],  # Solo Miguel está disponible
            'female': ['Lupe'],  # Solo Lupe está disponible
            'announcer': 'Miguel'
        }
        
        # Create audio output directory
        self.audio_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "frontend/static/audio"
        )
        os.makedirs(self.audio_dir, exist_ok=True)

    def validate_conversation_parts(self, parts: List[Tuple[str, str, str]]) -> bool:
        """
        Validate that the conversation parts are properly formatted.
        Returns True if valid, False otherwise.
        """
        if not parts:
            print("Error: No conversation parts generated")
            return False
            
        # Check that we have an announcer for intro
        if not parts[0][0].lower() == 'announcer':
            print("Error: First speaker must be Announcer")
            return False
            
        # Check that each part has valid content
        for i, (speaker, text, gender) in enumerate(parts):
            if not speaker or not isinstance(speaker, str):
                print(f"Error: Invalid speaker in part {i+1}")
                return False
                
            if not text or not isinstance(text, str):
                print(f"Error: Invalid text in part {i+1}")
                return False
                
            if gender not in ['male', 'female']:
                print(f"Error: Invalid gender in part {i+1}: {gender}")
                return False
        
        return True

    def parse_conversation(self, question: Dict) -> List[Tuple[str, str, str]]:
        """
        Convert question into a format for audio generation.
        Returns a list of (speaker, text, gender) tuples.
        """
        print("\nGenerating conversation format from question:")
        print(json.dumps(question, ensure_ascii=False, indent=2))
        
        prompt = f"""
        You are a Spanish language listening test audio script generator. Format the following question for audio generation.

        Rules:
        1. Introduction and Question parts:
           - Must start with 'Speaker: Announcer (Gender: male)'
           - Keep as separate parts
           - Introduction should say "Listen to the following conversation and answer the question" in Spanish

        2. Conversation parts:
           - Name speakers based on their role (Student, Teacher, etc.)
           - Must specify gender EXACTLY as either 'Gender: male' or 'Gender: female'
           - Use consistent names for the same speaker
           - Split long speeches at natural pauses
           - Convert all text to Spanish

        Format each part EXACTLY like this, with no variations:
        Speaker: [name] (Gender: male/female)
        Text: [Spanish text]
        ---

        Example format:
        Speaker: Announcer (Gender: male)
        Text: Escucha la siguiente conversación y responde a la pregunta.
        ---
        Speaker: Student (Gender: female)
        Text: Perdón, ¿esta clase es la de historia?
        ---

        Question to format:
        {json.dumps(question, ensure_ascii=False, indent=2)}

        Output ONLY the formatted parts in order: introduction, conversation, question.
        Make sure to specify gender EXACTLY as shown in the example.
        """
        
        try:
            # Use Gemini to generate the conversation format
            import google.generativeai as genai
            
            # Configure Gemini
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            model = genai.GenerativeModel('gemini-1.5-pro')
            response = model.generate_content(prompt)
            
            print("\nGemini response:")
            print(response.text)
            
            # Parse the response into parts
            parts = []
            current_speaker = None
            current_gender = None
            current_text = None
            
            for line in response.text.split('\n'):
                line = line.strip()
                if not line or line == '---':
                    if current_speaker and current_text and current_gender:
                        parts.append((current_speaker, current_text, current_gender))
                        current_speaker = None
                        current_gender = None
                        current_text = None
                    continue
                
                if line.startswith('Speaker:'):
                    speaker_info = line.split('Speaker:')[1].strip()
                    current_speaker = speaker_info.split('(')[0].strip()
                    gender_part = speaker_info.split('Gender:')[1].split(')')[0].strip().lower()
                    current_gender = 'male' if 'male' in gender_part else 'female'
                
                elif line.startswith('Text:'):
                    current_text = line.split('Text:')[1].strip()
            
            # Add final part if exists
            if current_speaker and current_text and current_gender:
                parts.append((current_speaker, current_text, current_gender))
            
            print("\nParsed conversation parts:")
            for speaker, text, gender in parts:
                print(f"\nSpeaker: {speaker} ({gender})")
                print(f"Text: {text}")
            
            # Validate parts
            if self.validate_conversation_parts(parts):
                return parts
            else:
                raise Exception("Invalid conversation format generated")
                
        except Exception as e:
            print(f"Error parsing conversation: {str(e)}")
            raise

    def get_voice_for_gender(self, gender: str) -> str:
        """Get an appropriate voice for the given gender"""
        if gender == 'male':
            return self.voices['male'][0]
        else:
            return self.voices['female'][0]

    def generate_audio_part(self, text: str, voice_name: str) -> str:
        """Generate audio for a single part using Amazon Polly"""
        try:
            print(f"\nGenerating audio for text: {text}")
            print(f"Using voice: {voice_name}")
            
            response = self.polly.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId=voice_name,
                Engine='standard',
                LanguageCode='es-US'  # Cambiado a es-US para coincidir con la interfaz
            )
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_file.write(response['AudioStream'].read())
                print(f"Audio saved to: {temp_file.name}")
                return temp_file.name
                
        except Exception as e:
            print(f"Error generating audio part: {str(e)}")
            return None

    def normalize_audio(self, input_file: str) -> str:
        """Normalize audio file to consistent format"""
        try:
            output_file = input_file.replace('.mp3', '_normalized.mp3')
            result = subprocess.run([
                'ffmpeg',
                '-i', input_file,
                '-c:a', 'libmp3lame',
                '-b:a', '128k',
                '-ar', '44100',
                '-ac', '1',
                '-y',
                output_file
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"ffmpeg error: {result.stderr}")
                raise Exception("Failed to normalize audio")
            
            print(f"Normalized audio saved to: {output_file}")
            return output_file
        except Exception as e:
            print(f"Error normalizing audio: {str(e)}")
            return input_file

    def combine_audio_files(self, audio_files: List[str], output_file: str) -> bool:
        """Combine multiple audio files using ffmpeg"""
        try:
            print("\nCombining audio files:")
            for audio_file in audio_files:
                print(f"- {audio_file}")
            
            # Normalize all audio files first
            normalized_files = []
            for audio_file in audio_files:
                normalized = self.normalize_audio(audio_file)
                normalized_files.append(normalized)
            
            # Create temporary file for concatenation list
            with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as f:
                for audio_file in normalized_files:
                    f.write(f"file '{audio_file}'\n")
                concat_list = f.name
            
            print(f"\nConcatenation list created at: {concat_list}")
            
            # Combine normalized files
            result = subprocess.run([
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', concat_list,
                '-c', 'copy',
                '-y',
                output_file
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print("\nffmpeg error output:")
                print(result.stderr)
                raise Exception("ffmpeg command failed")
            
            print(f"Combined audio saved to: {output_file}")
            return True
            
        except Exception as e:
            print(f"Error combining audio files: {str(e)}")
            if os.path.exists(output_file):
                os.unlink(output_file)
            return False
            
        finally:
            # Clean up temporary files
            if 'concat_list' in locals() and os.path.exists(concat_list):
                os.unlink(concat_list)
            for audio_file in audio_files:
                if os.path.exists(audio_file) and audio_file != output_file:
                    try:
                        os.unlink(audio_file)
                    except Exception as e:
                        print(f"Error cleaning up {audio_file}: {str(e)}")
            for normalized_file in normalized_files:
                if os.path.exists(normalized_file) and normalized_file != output_file:
                    try:
                        os.unlink(normalized_file)
                    except Exception as e:
                        print(f"Error cleaning up normalized file {normalized_file}: {str(e)}")

    def generate_audio(self, question: Dict) -> str:
        """
        Generate audio for the entire question.
        Returns the path to the generated audio file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.audio_dir, f"question_{timestamp}.mp3")
        
        try:
            print("\nStarting audio generation process...")
            
            # Parse conversation into parts
            parts = self.parse_conversation(question)
            
            # Generate audio for each part
            audio_parts = []
            
            # Generate silence files for pauses
            long_pause = self.generate_silence(2000)  # 2 second pause
            short_pause = self.generate_silence(500)  # 0.5 second pause
            
            for speaker, text, gender in parts:
                # Get appropriate voice for this speaker
                voice = self.get_voice_for_gender(gender)
                print(f"\nProcessing part - Speaker: {speaker} ({gender})")
                print(f"Text: {text}")
                print(f"Voice: {voice}")
                
                # Generate audio for this part
                audio_file = self.generate_audio_part(text, voice)
                if not audio_file:
                    raise Exception(f"Failed to generate audio for {speaker}")
                
                audio_parts.append(audio_file)
                
                # Add appropriate pause
                if speaker.lower() == 'announcer':
                    audio_parts.append(long_pause)
                else:
                    audio_parts.append(short_pause)
            
            # Combine all parts into final audio
            if not self.combine_audio_files(audio_parts, output_file):
                raise Exception("Failed to combine audio files")
            
            print("\nAudio generation completed successfully!")
            return output_file
            
        except Exception as e:
            print(f"\nError generating audio: {str(e)}")
            if os.path.exists(output_file):
                os.unlink(output_file)
            raise

    def generate_silence(self, duration_ms: int) -> str:
        """Generate a silent audio file of specified duration"""
        output_file = os.path.join(self.audio_dir, f'silence_{duration_ms}ms.mp3')
        if not os.path.exists(output_file):
            subprocess.run([
                'ffmpeg',
                '-f', 'lavfi',
                '-i', f'anullsrc=r=44100:cl=mono:d={duration_ms/1000}',
                '-ar', '44100',
                '-ac', '1',
                '-b:a', '128k',
                output_file
            ], check=True)
        return output_file