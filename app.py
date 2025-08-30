from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from database import init_app as init_db
from auth import auth_bp
from routes import main_bp

def create_app():
    app = Flask(__name__)
    init_db(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)