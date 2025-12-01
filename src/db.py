"""
MongoDB database connection and initialization
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

logger = logging.getLogger(__name__)

# Global database connection
db_client = None
db = None

def init_db(mongo_uri):
    """Initialize MongoDB connection and create indexes for performance"""
    global db_client, db
    
    try:
        db_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)
        # Test connection
        db_client.server_info()
        
        # Extract database name from URI or use default
        # Handle connection strings with query parameters
        db_name = mongo_uri.split('/')[-1].split('?')[0] if '/' in mongo_uri else 'notes'
        if not db_name:
            db_name = 'notes'
        db = db_client[db_name]
        
        # Create indexes for better search performance
        db.notes.create_index([('title', 'text'), ('body', 'text')])
        db.notes.create_index('created_at')
        
        logger.info(f"Successfully connected to MongoDB: {db_name}")
    except (ConnectionFailure, Exception) as e:
        logger.warning(f"Failed to connect to MongoDB on startup: {e}")
        logger.warning("App will start, but database operations will fail until connection is established")
        # Don't raise - let the app start, connections will be retried on requests

def get_db():
    """Get the database instance"""
    if db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return db

def close_db():
    """Close the database connection."""
    global db_client
    if db_client:
        db_client.close()
        logger.info("MongoDB connection closed")

