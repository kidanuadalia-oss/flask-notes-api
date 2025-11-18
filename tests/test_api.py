"""
API Tests using pytest
"""
import pytest
import os
from src.app import create_app
from src.db import init_db, get_db

# Set test environment variables
os.environ['FLASK_ENV'] = 'test'
os.environ['MONGO_URI'] = os.getenv('TEST_MONGO_URI', 'mongodb://localhost:27017/notes_test')
os.environ['PORT'] = '8080'

@pytest.fixture
def app():
    """Create test Flask application."""
    app = create_app()
    app.config['TESTING'] = True
    
    # Initialize test database
    init_db(os.environ['MONGO_URI'])
    
    # Clear test database before each test
    db = get_db()
    db.notes.delete_many({})
    
    yield app
    
    # Cleanup after test
    db.notes.delete_many({})

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_metrics_endpoint(client):
    """Test metrics endpoint returns 200."""
    response = client.get('/metrics')
    assert response.status_code == 200
    data = response.json
    assert 'uptime_seconds' in data
    assert 'total_requests' in data
    assert 'total_notes_in_db' in data

def test_create_note(client):
    """Test creating a note."""
    note_data = {
        'title': 'Test Note',
        'body': 'This is a test note body'
    }
    
    response = client.post('/notes', json=note_data)
    assert response.status_code == 201
    
    data = response.json
    assert data['title'] == note_data['title']
    assert data['body'] == note_data['body']
    assert '_id' in data
    assert 'created_at' in data

def test_create_note_missing_title(client):
    """Test creating a note without title fails."""
    note_data = {
        'body': 'This is a test note body'
    }
    
    response = client.post('/notes', json=note_data)
    assert response.status_code == 400

def test_list_notes(client):
    """Test listing notes."""
    # Create a note first
    note_data = {
        'title': 'Test Note',
        'body': 'Test body'
    }
    client.post('/notes', json=note_data)
    
    # List notes
    response = client.get('/notes')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 1

def test_get_note_by_id(client):
    """Test getting a note by ID."""
    # Create a note
    note_data = {
        'title': 'Test Note',
        'body': 'Test body'
    }
    create_response = client.post('/notes', json=note_data)
    note_id = create_response.json['_id']
    
    # Get the note
    response = client.get(f'/notes/{note_id}')
    assert response.status_code == 200
    assert response.json['_id'] == note_id
    assert response.json['title'] == note_data['title']

def test_get_note_invalid_id(client):
    """Test getting a note with invalid ID."""
    response = client.get('/notes/invalid_id')
    assert response.status_code == 400

def test_search_notes(client):
    """Test searching notes."""
    # Create notes
    client.post('/notes', json={'title': 'Python Tutorial', 'body': 'Learn Python'})
    client.post('/notes', json={'title': 'JavaScript Guide', 'body': 'Learn JS'})
    
    # Search for Python
    response = client.get('/notes/search?q=Python')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert 'Python' in response.json[0]['title']

def test_delete_note(client):
    """Test deleting a note."""
    # Create a note
    note_data = {
        'title': 'Test Note',
        'body': 'Test body'
    }
    create_response = client.post('/notes', json=note_data)
    note_id = create_response.json['_id']
    
    # Delete the note
    response = client.delete(f'/notes/{note_id}')
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f'/notes/{note_id}')
    assert get_response.status_code == 404

def test_delete_note_not_found(client):
    """Test deleting a non-existent note."""
    from bson import ObjectId
    fake_id = str(ObjectId())
    response = client.delete(f'/notes/{fake_id}')
    assert response.status_code == 404

