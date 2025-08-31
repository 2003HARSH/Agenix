# Agenix/routes.py
from flask import Blueprint, render_template, request, session,redirect, url_for
from flask_login import login_required, current_user
from graph import runnable
from langchain_core.messages import HumanMessage
from models import Chat
from database import db
import uuid

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.chat_index'))
    return render_template('index.html')

@main_bp.route('/chat', methods=['GET'])
@login_required
def chat_index():
    # Redirect to the most recent chat, or create one if none exist
    first_chat = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.id.desc()).first()
    if not first_chat:
        return redirect(url_for('main.new_chat'))
    return redirect(url_for('main.chat', chat_id=first_chat.id))

@main_bp.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
@login_required
def chat(chat_id):
    chat = Chat.query.filter_by(id=chat_id, user_id=current_user.id).first_or_404()
    
    thread_id = chat.thread_id
    config = {"configurable": {"thread_id": thread_id}}
    session['thread_id'] = thread_id

    if request.method == 'POST':
        prompt = request.form.get('prompt')
        if prompt:
            inputs = {"messages": [("user", prompt)]}
            runnable.invoke(inputs, config=config)

    state = runnable.get_state(config)
    
    messages = []
    if state:
        raw_messages = state.values.get('messages', [])
        for msg in raw_messages:
            if isinstance(msg, HumanMessage) and msg.name is None:
                msg.name = 'user'

            if msg.name in ('user', 'assistant'):
                messages.append(msg)
    
    user_chats = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.id.desc()).all()
        
    return render_template('chat.html', messages=messages, chats=user_chats, active_chat_id=chat_id)

@main_bp.route('/new_chat', methods=['GET'])
@login_required
def new_chat():
    new_thread_id = str(uuid.uuid4())
    # Default name is the thread_id
    chat = Chat(user_id=current_user.id, thread_id=new_thread_id, name=new_thread_id)
    db.session.add(chat)
    db.session.commit()
    return redirect(url_for('main.chat', chat_id=chat.id))

# REMOVED the /edit_chat_name endpoint