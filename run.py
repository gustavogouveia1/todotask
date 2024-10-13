from app import create_app
from app.controllers import tasks_bp 

app = create_app()

app.register_blueprint(tasks_bp)

if __name__ == '__main__':
    app.run(debug=True)
