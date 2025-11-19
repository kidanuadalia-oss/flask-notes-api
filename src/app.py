"""
Flask Notes API - Main Application

This module initializes the Flask application, configures middleware,
registers blueprints, and sets up request logging.

Author: Flask Notes API Team
License: MIT
"""
import os
from flask import Flask
from flask_cors import CORS
from src.db import init_db
from src.routes import notes_bp
from src.metrics import metrics_bp, init_metrics

def create_app():
    """
    Create and configure the Flask application.
    
    This factory function creates a Flask app instance, configures CORS,
    initializes the database connection, sets up metrics tracking, and
    registers all API blueprints.
    
    Environment Variables:
        MONGO_URI: MongoDB connection string (default: mongodb://mongo:27017/notes)
        FLASK_ENV: Flask environment mode (default: development)
        PORT: Port to run the application on (default: 8080)
    
    Returns:
        Flask: Configured Flask application instance
    
    Raises:
        ConnectionFailure: If MongoDB connection fails
    """
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Load configuration from environment variables
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://mongo:27017/notes')
    app.config['FLASK_ENV'] = os.getenv('FLASK_ENV', 'development')
    
    # Initialize database connection
    init_db(app.config['MONGO_URI'])
    
    # Initialize metrics
    init_metrics()
    
    # Register blueprints
    app.register_blueprint(notes_bp)
    app.register_blueprint(metrics_bp)
    
    # Request logging middleware
    @app.before_request
    def log_request():
        """
        Log all incoming requests before processing.
        
        This middleware runs before every request and logs the HTTP method,
        path, and timestamp. It also increments the request counter for metrics.
        """
        from src.metrics import log_request_metric
        log_request_metric()
    
    @app.route('/health')
    def health():
        """
        Health check endpoint for monitoring and load balancers.
        
        Returns:
            dict: JSON response with status 'healthy'
            int: HTTP status code 200
        
        Example:
            GET /health -> {"status": "healthy"}
        """
        return {'status': 'healthy'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=(app.config['FLASK_ENV'] == 'development'))

