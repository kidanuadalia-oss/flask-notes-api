"""
MongoDB Database Connection Module

This module handles MongoDB connection initialization, database access,
and connection management. It creates indexes for optimal query performance.
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

logger = logging.getLogger(__name__)

# Global database connection
db_client = None
db = None

def init_db(mongo_uri):
    """
    Initialize MongoDB connection.
    
    Args:
        mongo_uri: MongoDB connection URI
    """
    global db_client, db
    
    try:
        db_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # Test connection
        db_client.server_info()
        
        # Extract database name from URI or use default
        db_name = mongo_uri.split('/')[-1] if '/' in mongo_uri else 'notes'
        db = db_client[db_name]
        
        # Create indexes for better search performance
        db.notes.create_index([('title', 'text'), ('body', 'text')])
        db.notes.create_index('created_at')
        
        logger.info(f"Successfully connected to MongoDB: {db_name}")
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

def get_db():
    """
    Get the database instance.
    
    Returns:
        Database instance
    """
    if db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return db

def close_db():
    """Close the database connection."""
    global db_client
    if db_client:
        db_client.close()
        logger.info("MongoDB connection closed")

