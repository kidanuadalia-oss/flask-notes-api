"""
Metrics Tracking Module
"""
import time
import logging
from datetime import datetime
from flask import Blueprint, jsonify
from src.db import get_db

logger = logging.getLogger(__name__)

metrics_bp = Blueprint('metrics', __name__, url_prefix='/metrics')

# Global metrics
start_time = None
total_requests = 0
total_notes_created = 0

def init_metrics():
    """Initialize metrics tracking."""
    global start_time
    start_time = time.time()
    logger.info("Metrics initialized")

def log_request_metric():
    """Log a request and increment counter."""
    global total_requests
    total_requests += 1
    
    # Log request details
    from flask import request
    logger.info(f"Request: {request.method} {request.path} - {datetime.utcnow().isoformat()}")

def increment_notes_counter():
    """Increment the notes creation counter."""
    global total_notes_created
    total_notes_created += 1

def get_uptime():
    """Get application uptime in seconds."""
    if start_time is None:
        return 0
    return int(time.time() - start_time)

def get_total_notes_in_db():
    """Get total number of notes in database."""
    try:
        db = get_db()
        return db.notes.count_documents({})
    except Exception as e:
        logger.error(f"Error counting notes: {e}")
        return 0

@metrics_bp.route('', methods=['GET'])
def get_metrics():
    """Get application metrics."""
    try:
        uptime_seconds = get_uptime()
        
        # Convert uptime to human-readable format
        hours = uptime_seconds // 3600
        minutes = (uptime_seconds % 3600) // 60
        seconds = uptime_seconds % 60
        uptime_formatted = f"{hours}h {minutes}m {seconds}s"
        
        metrics = {
            'uptime_seconds': uptime_seconds,
            'uptime_formatted': uptime_formatted,
            'total_requests': total_requests,
            'total_notes_in_db': get_total_notes_in_db(),
            'total_notes_created': total_notes_created
        }
        
        logger.info("Metrics retrieved")
        return jsonify(metrics), 200
    
    except Exception as e:
        logger.error(f"Error retrieving metrics: {e}")
        return jsonify({'error': 'Failed to retrieve metrics'}), 500

