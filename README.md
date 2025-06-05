# 🤖 Agenix - A Multi-Agent Chatbot with LangGraph, Memory, and Tool Integration

A modular, memory-aware chatbot powered by **LangGraph**, designed using a **Supervisor-based multi-agent system**. This project demonstrates a production-ready LLM workflow that can handle vague prompts, recall previous conversations, and intelligently delegate tasks across specialized agents.

---

## ✨ Features

* 🔄 **Supervisor-Guided Agent Routing**
  Dynamically dispatches queries to specialized agents based on intent.

* 🧠 **SQL-Based Persistent Memory**
  Stores chat history using thread IDs, allowing the model to remember user context across turns.

* ⚡ **Tool-Aware and Extensible**
  Agents are designed to support external tools, paving the way for search, RAG, web browsing, and more.

* 🧩 **Modular Graph Architecture with LangGraph**
  Each agent is a graph node, allowing for easy customization, debugging, and branching.

* 💬 **Interactive Chat UI (Streamlit)**
  User-friendly interface with real-time streaming responses, agent tagging, and session-based chat memory.

---

## 🧠 Agents Overview

| Agent          | Role Description                                                        |
| -------------- | ----------------------------------------------------------------------- |
| **Supervisor** | Entry point of the graph. Routes user queries to the appropriate agent. |
| **Enhancer**   | Enhances vague or ambiguous queries. Can ask follow-up questions.       |
| **Researcher** | Gathers relevant background information using google search.            |
| **Coder**      | Generates and debugs code snippets based on user prompts.               |
| **Validator**  | Verifies outputs and ensures factuality, completeness, and quality.     |
| **Normal**     | Handles greetings, small talk, and informal interactions.               |

---

## 🛠 Tech Stack

* 🧠 [LangGraph](https://github.com/langchain-ai/langgraph)
* 🗃️ SQL-based Checkpointing 
* 💬 [LangChain](https://github.com/langchain-ai/langchain) agents & tools
* 🌐 [Streamlit](https://streamlit.io/) chat UI
* 🧱 Modular Python (each agent in its own module)

---

## 📦 Installation

```bash
git clone https://github.com/2003harsh/agenix.git
cd agenix
pip install -r requirements.txt
```

Make sure you have an `.env` file with your API keys, if needed.

---

## 🚀 Run the App

```bash
streamlit run streamlit_app.py
```

---

## 🧪 Example Usage

**User**: Hi, I’m Harsh
**Bot** (Normal): Hello Harsh! How can I assist you today?

**User**: What’s my name?
**Bot** (Validator): You mentioned your name is *Harsh* earlier.

**User**: Write a Python function to get the nth Fibonacci number
**Bot** (Coder → Validator): Returns an optimized Python function with explanation.

---

## 🧠 How Context Is Retained

Each chat session uses a persistent `thread_id`. All message history is saved using a **SQL-based checkpointer** and is automatically passed to agents. Even after app restarts, your chatbot remembers prior interactions within that thread.

---

## 🧩 Architecture Diagram

```
[START] → [Supervisor]
              ↓
   ┌──────────┴───────────┐
[Enhancer]  [Researcher]  [Coder]  [Normal]
               ↓               ↓        ↓
                     →→→→ [Validator] →→→→ [END]
```

---

## ✅ TODO

* [ ] Add support for RAG via LangChain Tools
* [ ] Enable agent self-reflection using LangGraph loops
* [ ] Extend to multimodal input (images, documents)
* [ ] Web deployable version with FastAPI

---

## 🤝 Contributing

Pull requests, issues, and ideas are welcome!
If you’re working on LLM orchestration, LangGraph, or custom agents — let’s collaborate.

---

## 📜 License

MIT License. Feel free to fork and build on top of it!

---

## 🌐 Connect

* 👤 Author: [Harsh Gupta](https://www.linkedin.com/in/harsh-gupta-2021/)
* 📫 Email: [harshnkgupta@gmail.com](mailto:harshnkgupta@gmail.com)

