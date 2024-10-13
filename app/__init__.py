from flask import Flask
from flask_cors import CORS
from .controllers import tasks 
from .controllers import auth 

def create_app():
    app = Flask(__name__, template_folder='../front-end/templates', static_folder='../front-end/static')
    CORS(app)  # Habilita CORS para todas as rotas

    app.register_blueprint(tasks.bp)
    
    return app
