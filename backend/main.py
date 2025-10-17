import os
from flask import Flask
from flask_cors import CORS
from app.routes import api_bp
from dotenv import load_dotenv

# Load environment variables from .env file
# First try .env.local, then .env.production, then .env
env_file = '.env.local' if os.path.exists('.env.local') else '.env.production' if os.path.exists('.env.production') else '.env'
load_dotenv(env_file)

def create_app():
    app = Flask(__name__)
    
    # Get CORS origins from environment or use defaults
    allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000,https://devocosm.com,https://chinese-study.devocosm.com')
    origins_list = [origin.strip() for origin in allowed_origins.split(',')]
    
    # Enable CORS for frontend
    CORS(app, origins=origins_list)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/health')
    def health_check():
        return {
            'status': 'healthy', 
            'message': 'Chinese Learning API is running',
            'environment': os.getenv('FLASK_ENV', 'development')
        }
    
    return app

# Create the app instance for gunicorn
app = create_app()

if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', '5000'))
    app.run(debug=debug, host=host, port=port)



