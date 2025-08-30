# Agenix/database.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool
# ADDED: Import the correct serializer
# from langgraph.checkpoint.serde import JsonPlusSerializer

db = SQLAlchemy()
login_manager = LoginManager()

# Create a single, shared connection pool instance
pool = ConnectionPool(
    conninfo=os.environ.get("DATABASE_URL"), 
    min_size=1, 
    max_size=5
)

def setup_langgraph_checkpointer():
    """Initializes the LangGraph checkpointer and sets up the database schema."""
    with pool.connection() as conn:
        conn.autocommit = True
        # Use the explicit serializer during setup
        memory = PostgresSaver( conn=conn)
        memory.setup()

def init_app(app):
    """Initializes the database and login manager for the Flask app."""
    from models import User

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL").replace(
        "postgresql://", "postgresql+psycopg://"
    )
    db.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
    
    setup_langgraph_checkpointer()