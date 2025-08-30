from flask import Flask
from flask_cors import CORS
from app.routes import api_bp

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for frontend
    CORS(app, origins=["http://localhost:3000", "https://devocosm.com"])
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Chinese Learning API is running'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)



