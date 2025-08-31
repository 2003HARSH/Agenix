# Agenix/routes.py
from flask import Blueprint, render_template, request, session,redirect, url_for
from flask_login import login_required, current_user
from graph import runnable
from langchain_core.messages import HumanMessage, AIMessage

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.chat'))
    return render_template('index.html')

@main_bp.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    thread_id = current_user.thread_id
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
        
    return render_template('chat.html', messages=messages)