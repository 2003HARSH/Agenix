# Agenix/app.py
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from database import init_app as init_db
from auth import auth_bp
from routes import main_bp

def create_app():
    """App factory to create and configure the Flask app."""
    flask_app = Flask(__name__)
    init_db(flask_app)

    # Register blueprints
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(main_bp)

    return flask_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)