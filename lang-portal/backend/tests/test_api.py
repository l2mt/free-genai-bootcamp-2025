from fastapi.testclient import TestClient
from app.main import app
import pytest

def test_list_words(client):
    """Prueba el endpoint de listar palabras"""
    response = client.get("/api/words")
    assert response.status_code == 200
    data = response.json()
    
    # Verificar estructura de la respuesta
    assert "items" in data
    assert "pagination" in data
    assert isinstance(data["items"], list)
    
    # Si hay palabras, verificar su estructura
    if data["items"]:
        word = data["items"][0]
        assert "id" in word
        assert "spanish" in word
        assert "english" in word
        assert "correct_count" in word
        assert "wrong_count" in word

def test_get_word(client):
    """Prueba obtener una palabra específica"""
    # Asumiendo que existe al menos una palabra en la base de datos
    response = client.get("/api/words/1")
    assert response.status_code == 200
    word = response.json()
    
    assert "id" in word
    assert "spanish" in word
    assert "english" in word
    assert "correct_count" in word
    assert "wrong_count" in word

def test_get_words_by_group(client):
    """Prueba obtener palabras de un grupo"""
    # Asumiendo que existe al menos un grupo
    response = client.get("/api/groups/1/words")
    assert response.status_code == 200
    data = response.json()
    
    assert "items" in data
    assert "pagination" in data
    
    # Verificar estructura de las palabras si existen
    if data["items"]:
        word = data["items"][0]
        assert "id" in word
        assert "spanish" in word
        assert "english" in word
        assert "correct_count" in word
        assert "wrong_count" in word

def test_last_study_session(client):
    """Prueba obtener la última sesión de estudio"""
    response = client.get("/api/dashboard/last_study_session")
    assert response.status_code == 200
    data = response.json()
    
    assert "id" in data
    assert "activity_name" in data
    assert "group_name" in data
    assert "created_at" in data
    assert "study_activity_id" in data
    assert "group_id" in data
    assert "correct_count" in data
    assert "incorrect_count" in data
    assert "total_items" in data

def test_study_progress(client):
    """Prueba obtener progreso de estudio"""
    response = client.get("/api/dashboard/study_progress")
    assert response.status_code == 200
    data = response.json()
    
    assert "total_words_studied" in data
    assert "total_available_words" in data
    assert "mastery_percentage" in data
    
    # Verificaciones adicionales
    assert isinstance(data["total_words_studied"], int)
    assert isinstance(data["total_available_words"], int)
    assert isinstance(data["mastery_percentage"], int)

def test_quick_stats(client):
    """Prueba obtener estadísticas rápidas"""
    response = client.get("/api/dashboard/quick_stats")
    assert response.status_code == 200
    data = response.json()
    
    assert "success_rate" in data
    assert "total_study_sessions" in data
    assert "total_active_groups" in data
    assert "study_streak_days" in data
    
    # Verificaciones adicionales
    assert isinstance(data["success_rate"], int)
    assert isinstance(data["total_study_sessions"], int)
    assert isinstance(data["total_active_groups"], int)
    assert isinstance(data["study_streak_days"], int)
