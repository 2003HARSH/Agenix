# 🤖 Agenix - Multi-Agent Chatbot with LangGraph, Flask, and Persistent Memory

A production-ready, modular chatbot powered by **LangGraph**, built on a **Supervisor-based multi-agent architecture**. Agenix supports user authentication, session management, and persistent chat history, making it a practical framework for deploying advanced AI agents at scale.

---

## ✨ Features

* 🔄 **Supervisor-Guided Agent Routing**
  Dynamically delegates queries to specialized agents (research, coding, validation, small talk).

* 🔐 **User Authentication**
  Sign-in, sign-up, and session management built with Flask + PostgreSQL.

* 💬 **Session-Based Chat**
  Each user gets personalized chat sessions with persistent conversation history.

* 🧠 **PostgreSQL-Backed Memory**
  Stores and retrieves chat history by session ID for long-term context retention.

* ⚡ **Tool-Aware and Extensible**
  Agents support integration with external tools like search, RAG, and web browsing.

* 🧩 **LangGraph Modular Architecture**
  Each agent is a node in the graph, enabling easy customization, branching, and debugging.

* 🌐 **Flask Web Interface**
  Interactive chat UI with user accounts, session tracking, and agent-tagged responses.

---

## 🧠 Agents Overview

| Agent          | Role Description                                                |
| -------------- | --------------------------------------------------------------- |
| **Supervisor** | Entry point of the graph. Routes queries to the right agent.    |
| **Enhancer**   | Improves vague/ambiguous queries, can ask clarifying questions. |
| **Researcher** | Gathers external knowledge (search APIs, docs, etc.).           |
| **Coder**      | Generates and debugs code snippets.                             |
| **Validator**  | Checks accuracy, factuality, and correctness of outputs.        |
| **Normal**     | Handles greetings, small talk, and informal chat.               |

---

## 🛠 Tech Stack

* 🧠 [LangGraph](https://github.com/langchain-ai/langgraph) for multi-agent orchestration
* 💬 [LangChain](https://github.com/langchain-ai/langchain) agents & tools
* 🌐 **Flask** for backend + web interface
* 🗃️ **PostgreSQL** for authentication & memory persistence
* 🧱 Modular Python (each agent as a separate module)

---

## 📦 Installation

```bash
git clone https://github.com/2003harsh/agenix.git
cd agenix
pip install -r requirements.txt
```

Set up your `.env` file with:

```
DATABASE_URL=postgresql://user:password@localhost:5432/agenix
SECRET_KEY=your_flask_secret_key
OPENAI_API_KEY=your_openai_key
```

---

## 🚀 Run the App

```bash
python app.py
```

Then open: [http://localhost:5000](http://localhost:5000)

---

## 🧪 Example Usage

**User**: Write a Python function for Fibonacci
**Bot** (Coder → Validator): Returns optimized function with explanation.

**User**: What’s my name?
**Bot** (Validator): Recalls from earlier in the same session.

**User**: Summarize a recent AI breakthrough
**Bot** (Researcher → Enhancer → Validator): Provides fact-checked summary.

---

## 🧩 Architecture Diagram

```
[User Session] → [Supervisor]
                     ↓
     ┌───────────────┴───────────────┐
 [Enhancer]   [Researcher]   [Coder]   [Normal]
                    ↓            ↓         ↓
                                           →  [Passthrough]  -> [Validator] -> [END]
```

---

## ✅ TODO

* [ ] Add RAG support with vector DBs (FAISS/Chroma/Pinecone)
* [ ] Implement agent self-reflection with LangGraph loops
* [ ] Extend to multimodal input (images, PDFs)
* [ ] Deploy Flask app with Docker + AWS/GCP

---

## 🤝 Contributing

Contributions, bug reports, and feature suggestions are welcome. Fork it, play with it, break it, and help make it better.

---

## 📜 License

MIT License — free to use, modify, and extend.

---

## 🌐 Connect

* 👤 Author: [Harsh Gupta](https://www.linkedin.com/in/harsh-gupta-2021/)
* 📫 Email: [harshnkgupta@gmail.com](mailto:harshnkgupta@gmail.com)
* 💻 GitHub: [2003HARSH](https://github.com/2003HARSH)
