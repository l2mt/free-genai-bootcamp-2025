# Sentences organized by work groups
# Each group has a set of English sentences and their correct Spanish translations

SENTENCE_GROUPS = {
    "Greetings": [
        {"english": "Hello, how are you?", "spanish": "Hola, ¿cómo estás?"},
        {"english": "Good morning!", "spanish": "¡Buenos días!"},
        {"english": "My name is John.", "spanish": "Me llamo John."},
        {"english": "Nice to meet you.", "spanish": "Encantado de conocerte."},
        {"english": "See you tomorrow!", "spanish": "¡Hasta mañana!"},
    ],
    
    "Food": [
        {"english": "I want a coffee, please.", "spanish": "Quiero un café, por favor."},
        {"english": "The restaurant is closed.", "spanish": "El restaurante está cerrado."},
        {"english": "This food is delicious.", "spanish": "Esta comida está deliciosa."},
        {"english": "Can I have the menu?", "spanish": "¿Puedo ver el menú?"},
        {"english": "I am vegetarian.", "spanish": "Soy vegetariano."},
    ],
    
    "Travel": [
        {"english": "Where is the hotel?", "spanish": "¿Dónde está el hotel?"},
        {"english": "How much is the ticket?", "spanish": "¿Cuánto cuesta el boleto?"},
        {"english": "I need a taxi.", "spanish": "Necesito un taxi."},
        {"english": "Is this the train to Madrid?", "spanish": "¿Este es el tren a Madrid?"},
        {"english": "I am lost.", "spanish": "Estoy perdido."},
    ],
    
    "Shopping": [
        {"english": "How much does this cost?", "spanish": "¿Cuánto cuesta esto?"},
        {"english": "I like this shirt.", "spanish": "Me gusta esta camisa."},
        {"english": "Do you have it in blue?", "spanish": "¿Lo tienen en azul?"},
        {"english": "I want to pay by card.", "spanish": "Quiero pagar con tarjeta."},
        {"english": "This is expensive.", "spanish": "Esto es caro."},
    ],
    
    "Daily Activities": [
        {"english": "I wake up at 7 AM.", "spanish": "Me despierto a las 7 de la mañana."},
        {"english": "I need to go to work.", "spanish": "Necesito ir al trabajo."},
        {"english": "What time is it?", "spanish": "¿Qué hora es?"},
        {"english": "I like to read books.", "spanish": "Me gusta leer libros."},
        {"english": "I am going to the gym.", "spanish": "Voy al gimnasio."},
    ],
}

def get_sentence_groups():
    """Returns the list of available sentence groups"""
    return list(SENTENCE_GROUPS.keys())

def get_sentences_from_group(group_name):
    """Returns the list of sentences for a specific group"""
    if group_name in SENTENCE_GROUPS:
        return SENTENCE_GROUPS[group_name]
    return [] 