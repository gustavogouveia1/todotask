from flask import Flask
from flask_cors import CORS
from .routes import bp as main_bp

def create_app():
    app = Flask(__name__, template_folder='../front-end/templates', static_folder='../front-end/static')
    CORS(app) 
    app.register_blueprint(main_bp)
    return app