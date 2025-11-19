"""
Notes API Routes

This module defines all REST API endpoints for note management:
- Create, read, update, delete operations
- Search functionality
- Error handling and validation

Author: Flask Notes API Team
License: MIT
"""
from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from src.db import get_db
from src.metrics import increment_notes_counter
import logging

logger = logging.getLogger(__name__)

notes_bp = Blueprint('notes', __name__, url_prefix='/notes')

def serialize_note(note):
    """
    Convert MongoDB document to JSON-serializable format.
    
    Converts ObjectId to string and datetime objects to ISO format strings
    for JSON serialization.
    
    Args:
        note (dict): MongoDB document with _id and created_at fields
    
    Returns:
        dict: JSON-serializable note document, or None if note is None
    """
    if note:
        note['_id'] = str(note['_id'])
        if 'created_at' in note and isinstance(note['created_at'], datetime):
            note['created_at'] = note['created_at'].isoformat()
    return note

@notes_bp.route('', methods=['POST'])
def create_note():
    """
    Create a new note.
    
    Request Body:
        title (str, required): Note title
        body (str, optional): Note content
    
    Returns:
        dict: Created note with _id and created_at
        int: HTTP status code (201 on success, 400/500 on error)
    
    Example:
        POST /notes
        {
            "title": "My Note",
            "body": "Note content"
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        title = data.get('title', '').strip()
        body = data.get('body', '').strip()
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        db = get_db()
        note = {
            'title': title,
            'body': body,
            'created_at': datetime.utcnow()
        }
        
        result = db.notes.insert_one(note)
        note['_id'] = str(result.inserted_id)
        
        increment_notes_counter()
        
        logger.info(f"Created note: {note['_id']}")
        return jsonify(serialize_note(note)), 201
    
    except Exception as e:
        logger.error(f"Error creating note: {e}")
        return jsonify({'error': 'Failed to create note'}), 500

@notes_bp.route('', methods=['GET'])
def list_notes():
    """
    List all notes, sorted by creation date (newest first).
    
    Returns:
        list: Array of note documents
        int: HTTP status code (200 on success, 500 on error)
    
    Example:
        GET /notes -> [{"_id": "...", "title": "...", ...}, ...]
    """
    try:
        db = get_db()
        notes = list(db.notes.find().sort('created_at', -1))
        
        # Serialize all notes
        serialized_notes = [serialize_note(note) for note in notes]
        
        logger.info(f"Retrieved {len(serialized_notes)} notes")
        return jsonify(serialized_notes), 200
    
    except Exception as e:
        logger.error(f"Error listing notes: {e}")
        return jsonify({'error': 'Failed to retrieve notes'}), 500

@notes_bp.route('/<note_id>', methods=['GET'])
def get_note(note_id):
    """
    Get a specific note by ID.
    
    Args:
        note_id (str): MongoDB ObjectId of the note
    
    Returns:
        dict: Note document, or error message
        int: HTTP status code (200 on success, 400/404/500 on error)
    
    Example:
        GET /notes/507f1f77bcf86cd799439011
    """
    try:
        if not ObjectId.is_valid(note_id):
            return jsonify({'error': 'Invalid note ID'}), 400
        
        db = get_db()
        note = db.notes.find_one({'_id': ObjectId(note_id)})
        
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        logger.info(f"Retrieved note: {note_id}")
        return jsonify(serialize_note(note)), 200
    
    except Exception as e:
        logger.error(f"Error retrieving note: {e}")
        return jsonify({'error': 'Failed to retrieve note'}), 500

@notes_bp.route('/search', methods=['GET'])
def search_notes():
    """
    Search notes by title or body substring (case-insensitive).
    
    Query Parameters:
        q (str, required): Search query string
    
    Returns:
        list: Array of matching note documents
        int: HTTP status code (200 on success, 400/500 on error)
    
    Example:
        GET /notes/search?q=python -> [notes containing "python"]
    """
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        db = get_db()
        
        # Use regex for case-insensitive substring search
        search_filter = {
            '$or': [
                {'title': {'$regex': query, '$options': 'i'}},
                {'body': {'$regex': query, '$options': 'i'}}
            ]
        }
        
        notes = list(db.notes.find(search_filter).sort('created_at', -1))
        serialized_notes = [serialize_note(note) for note in notes]
        
        logger.info(f"Found {len(serialized_notes)} notes matching query: {query}")
        return jsonify(serialized_notes), 200
    
    except Exception as e:
        logger.error(f"Error searching notes: {e}")
        return jsonify({'error': 'Failed to search notes'}), 500

@notes_bp.route('/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    """
    Delete a note by ID.
    
    Args:
        note_id (str): MongoDB ObjectId of the note to delete
    
    Returns:
        dict: Success message or error message
        int: HTTP status code (200 on success, 400/404/500 on error)
    
    Example:
        DELETE /notes/507f1f77bcf86cd799439011
    """
    try:
        if not ObjectId.is_valid(note_id):
            return jsonify({'error': 'Invalid note ID'}), 400
        
        db = get_db()
        result = db.notes.delete_one({'_id': ObjectId(note_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Note not found'}), 404
        
        logger.info(f"Deleted note: {note_id}")
        return jsonify({'message': 'Note deleted successfully'}), 200
    
    except Exception as e:
        logger.error(f"Error deleting note: {e}")
        return jsonify({'error': 'Failed to delete note'}), 500

