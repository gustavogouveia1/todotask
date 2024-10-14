from app import create_app
from app.controllers import tasks_bp, auth_bp

app = create_app()

app.register_blueprint(tasks_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
