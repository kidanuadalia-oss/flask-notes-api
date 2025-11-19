"""
Flask application setup and configuration
"""
import os
from flask import Flask
from flask_cors import CORS
from src.db import init_db
from src.routes import notes_bp
from src.metrics import metrics_bp, init_metrics

def create_app():
    """
    Creates and configures the Flask application.
    Sets up CORS, initializes database connection, registers blueprints, and configures logging.
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
        """Logs all incoming requests for debugging and monitoring"""
        from src.metrics import log_request_metric
        log_request_metric()
    
    @app.route('/health')
    def health():
        """Health check endpoint for monitoring"""
        return {'status': 'healthy'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=(app.config['FLASK_ENV'] == 'development'))

