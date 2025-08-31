# Agenix/auth.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User, Chat
from flask_login import login_user, logout_user, login_required
import uuid

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=True)
        return redirect(url_for('main.chat_index'))

    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_user = User(
            email=request.form.get('email'), 
            name=request.form.get('name'), 
            password=generate_password_hash(request.form.get('password')),
        )

        db.session.add(new_user)
        db.session.commit()

        # Create a default chat for the new user, named after its thread_id
        thread_id = str(uuid.uuid4())
        new_chat = Chat(user_id=new_user.id, thread_id=thread_id, name=thread_id)
        db.session.add(new_chat)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))