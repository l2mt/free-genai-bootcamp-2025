import chromadb
from chromadb.utils import embedding_functions
import json
import os
import openai
from typing import Dict, List, Optional

class OpenAIEmbeddingFunction(embedding_functions.EmbeddingFunction):
    def __init__(self, model: str = "text-embedding-3-small"):
        # Initialize the OpenAI client
        self.client = openai.OpenAI(api_key=QuestionVectorStore._openai_api_key)
        self.model = model

    def __call__(self, texts: List[str]) -> List[List[float]]:
        # Generate embeddings for a list of texts using OpenAI
        try:
            print(f"Generating embeddings for {len(texts)} texts using model {self.model}")
            response = self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            embeddings = [embedding.embedding for embedding in response.data]
            print(f"Successfully generated embeddings: {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
            # Return zero vectors as fallback (1536 dimensions for text-embedding-3-small)
            return [[0.0] * 1536 for _ in texts]

class QuestionVectorStore:
    _openai_api_key = None

    def __init__(self, persist_directory: str = "data/vectorstore"):
        """Initialize the vector store for general knowledge questions"""
        
        self.persist_directory = persist_directory
        
        # Initialize the ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Use the OpenAI embedding model
        self.embedding_fn = OpenAIEmbeddingFunction()
        
        # Create or get the collection for general knowledge questions
        self.collection = self.client.get_or_create_collection(
            name="general_knowledge_questions",
            embedding_function=self.embedding_fn,
            metadata={"description": "General knowledge questions in Spanish"}
        )
        print(f"Initialized QuestionVectorStore with collection: {self.collection.name}")

    def add_questions(self, questions: List[Dict], source_id: str):
        """Add questions to the vector store"""
        ids = []
        documents = []
        metadatas = []
        
        for idx, question in enumerate(questions):
            # Create a unique ID for each question
            question_id = f"{source_id}_{idx}"
            ids.append(question_id)
            
            # Store the full question structure as metadata
            metadatas.append({
                "source_id": source_id,
                "question_index": idx,
                "full_structure": json.dumps(question)
            })
            
            # Use the question text as the document for embeddings
            document = question.get('question', '')
            documents.append(document)
            print(f"Prepared question {question_id}: {document[:50]}...")  # Muestra los primeros 50 caracteres
        
        # Add to the collection
        print(f"Adding {len(ids)} questions to the collection")
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        print(f"Successfully added {len(ids)} questions")

    def search_similar_questions(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for similar questions in the vector store"""
        print(f"Searching for similar questions to: {query}")
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Convert the results to a more usable format
        questions = []
        for idx, metadata in enumerate(results['metadatas'][0]):
            question_data = json.loads(metadata['full_structure'])
            question_data['similarity_score'] = results['distances'][0][idx]
            questions.append(question_data)
            print(f"Found similar question: {question_data['question'][:50]}... with score {question_data['similarity_score']}")
            
        return questions

    def get_question_by_id(self, question_id: str) -> Optional[Dict]:
        """Retrieve a question by its ID"""
        print(f"Retrieving question by ID: {question_id}")
        result = self.collection.get(
            ids=[question_id],
            include=['metadatas']
        )
        
        if result['metadatas']:
            question_data = json.loads(result['metadatas'][0]['full_structure'])
            print(f"Retrieved question: {question_data['question'][:50]}...")
            return question_data
        print(f"No question found with ID: {question_id}")
        return None

    def parse_questions_from_file(self, filename: str) -> List[Dict]:
        """Parse general knowledge questions from a JSON file"""
        print(f"Parsing questions from file: {filename}")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                questions = json.load(f)
            print(f"Successfully parsed {len(questions)} questions from {filename}")
            return questions
        except Exception as e:
            print(f"Error parsing questions from {filename}: {str(e)}")
            return []

    def index_questions_file(self, filename: str):
        """Index all questions from a file in the vector store"""
        # Extract the source ID from the filename (without extension)
        source_id = os.path.splitext(os.path.basename(filename))[0]
        print(f"Indexing questions from {filename} with source_id: {source_id}")
        
        # Parse the questions from the file
        questions = self.parse_questions_from_file(filename)
        
        # Add to the vector store
        if questions:
            self.add_questions(questions, source_id)
            print(f"Indexed {len(questions)} questions from {filename}")
        else:
            print(f"No questions found in {filename}")

if __name__ == "__main__":
    # Example usage
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        print("Error: OPENAI_API_KEY not found in environment variables")
        exit(1)
    QuestionVectorStore._openai_api_key = openai_api_key
    store = QuestionVectorStore()
    
    # Index questions from JSON files
    question_files = [
        "data/questions/R-kepxbu5fM.json",  # Asegúrate de que este archivo exista
    ]
    
    for filename in question_files:
        if os.path.exists(filename):
            store.index_questions_file(filename)
        else:
            print(f"File not found: {filename}")
    
    # Search for similar questions
    similar = store.search_similar_questions("Cuál es la posición de nuestro planeta en el sistema solar", n_results=1)
    print("Similar questions found:")
    for q in similar:
        print(json.dumps(q, indent=2))