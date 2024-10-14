from app import create_app
from app.controllers import tasks_bp, auth_bp
from flask_jwt_extended import JWTManager

app = create_app()

app.register_blueprint(tasks_bp)
app.register_blueprint(auth_bp)

app.config.from_object('config.Config')  # Carrega as configurações do arquivo config.py
jwt = JWTManager(app)  # Inicializa o JWTManager com as configurações do Flask

if __name__ == '__main__':
    app.run(debug=True)
