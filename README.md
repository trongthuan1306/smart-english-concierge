# 🚀 Smart English Concierge



hi 
<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![Google Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?logo=google)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-Deployed-4285F4?logo=googlecloud)

### AI-powered Multi-Agent English Learning Assistant

**Built with FastAPI • React • Google Gemini • PostgreSQL • Google Cloud**

</div>

---

# 📖 Overview

Smart English Concierge is an AI-powered English learning assistant designed to provide users with a personalized and intelligent learning experience.

Instead of functioning as a traditional chatbot, the application adopts a **Multi-Agent Architecture** where different agent skills collaborate to understand user intent, perform specialized tasks, and securely manage personal learning data.

The project demonstrates how modern AI agents can assist language learners through intelligent conversations, vocabulary management, and secure AI interactions while remaining scalable and easily extensible.

---

# 🎯 Problem Statement

Learning English often requires learners to switch between multiple applications for chatting, translating, taking vocabulary notes, and reviewing previous learning materials.

Traditional chatbots also suffer from several limitations:

- They cannot perform structured actions.
- They have no persistent memory.
- They are difficult to extend with new capabilities.
- They are vulnerable to prompt injection attacks.
- They often expose sensitive personal information.

These limitations reduce productivity and make AI assistants less useful in daily learning.

---

# 💡 Solution

Smart English Concierge addresses these problems by introducing a modular **Multi-Agent System**.

Instead of asking one large language model to perform every task, the system separates responsibilities into specialized agent skills.

The workflow includes:

- Understanding user intent
- Selecting the appropriate skill
- Executing business logic
- Accessing PostgreSQL when necessary
- Returning structured responses

This architecture makes the application easier to maintain, more secure, and highly extensible.

---

# ✨ Features

- 🤖 AI-powered English conversation
- 📚 Save vocabulary into PostgreSQL
- 🔍 Intelligent intent recognition
- 🧠 Multi-Agent routing
- 🔒 Prompt Injection protection
- 🔐 PII masking (Email & Phone)
- ☁ Google Cloud deployment
- ⚡ RESTful FastAPI backend
- 🎨 Modern React interface
- 📖 Easily extendable Agent Skills

---

# 🏗 System Architecture

```

+-----------------------+
\|       User            |
+-----------+-----------+
|
v
+-----------------------+
\| React Frontend       |
+-----------+-----------+
|
REST API
|
v
+-----------------------+
\| FastAPI Backend      |
+-----------+-----------+
|
v
+-----------------------+
\| Security Guardrail   |
+-----------+-----------+
|
v
+-----------------------+
\| Agent Router         |
+-----------+-----------+
|
+------------+------------+
|                         |
v                         v
Google Gemini         Skill Discovery
|
v
+-----------------------+
\| Skill Handler        |
+-----------+-----------+
|
v
+-----------------------+
\| PostgreSQL Database  |
+-----------------------+

```

---

# 🔄 System Workflow

```

User Message

↓

React Frontend

↓

FastAPI API

↓

Security Guardrail

↓

Router Agent

↓

Google Gemini

↓

Select Appropriate Skill

↓

Execute Skill

↓

SQLAlchemy ORM

↓

PostgreSQL

↓

Return Response

↓

Frontend

```

---

# 🧠 Multi-Agent Design

The backend follows a modular agent architecture.

## Router Agent

Responsible for

- Intent detection
- Tool selection
- Parameter extraction
- Skill execution

---

## Skill Agents

Each skill is isolated inside its own folder.

Example:

```

agents/

skills/

vocab-saver/

SKILL.md

scripts/

handler.py

```

Adding a new capability only requires:

1. Create a new folder
2. Write SKILL.md
3. Implement handler.py

No router modification is required.

---

# 🔒 Security

The project incorporates several security mechanisms.

## Prompt Injection Detection

Prevents malicious prompts attempting to manipulate the language model.

Examples:

- Ignore previous instructions
- Reveal system prompt
- Execute unauthorized actions

---

## Personal Information Protection

Sensitive information including:

- Email addresses
- Phone numbers

is automatically masked before sending requests to Gemini.

---

## Secure Environment Variables

Secrets such as

- Gemini API Key
- Database URL

are stored securely using environment variables.

---

# 🗄 Database

The application uses PostgreSQL with SQLAlchemy ORM.

Current tables include:

Vocabulary

| Column | Description |
|----------|----------------|
| id | Primary Key |
| word | Vocabulary |
| meaning | Meaning |
| example | Example sentence |
| created_at | Timestamp |

---

# ⚙ Technologies

## Frontend

- React
- Vite
- TailwindCSS
- Axios

---

## Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic

---

## AI

- Google Gemini

---

## Database

- PostgreSQL

---

## Deployment

- Google Cloud

---

# 📂 Project Structure

```

smart-english-concierge/

├── backend/
│
├── agents/
│ ├── router.py
│ ├── security.py
│ └── skills/
│
├── database/
│ ├── database.py
│ ├── models.py
│ └── crud.py
│
├── models/
│ └── schemas.py
│
├── main.py
│
└── frontend/
├── src/
├── components/
├── services/
└── package.json

```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/smart-english-concierge.git
```

---

## Backend

```bash
cd backend

python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
uvicorn main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# 🔑 Environment Variables

Backend

```env
GEMINI_API_KEY=

DATABASE_URL=

FRONTEND_URL=
```

---

# ☁ Deployment

The application has been successfully deployed on **Google Cloud**.

Deployment includes:

- FastAPI backend
- React frontend
- PostgreSQL connection
- HTTPS access
- Environment variable configuration

---

# 📸 Screenshots

Replace these placeholders with your own screenshots.

- Home Page
- AI Chat
- Vocabulary Dashboard
- Saved Vocabulary
- PostgreSQL Database
- Google Cloud Deployment

---

# 🎥 Demo

- YouTube Demo
- Live Website
- GitHub Repository

---

# 🔮 Future Improvements

- User Authentication
- Learning Progress Dashboard
- Conversation History
- Grammar Correction
- Flashcards
- Pronunciation Assessment
- Voice Conversation
- Speech-to-Text
- Text-to-Speech
- RAG Knowledge Base

---

# 🏆 Kaggle AI Agents Capstone

This project was developed as part of the **Kaggle AI Agents: Intensive Vibe Coding Capstone Project**.

Key concepts demonstrated include:

- ✅ Multi-Agent Architecture
- ✅ Agent Skills
- ✅ Security Guardrails
- ✅ Google Gemini Integration
- ✅ Cloud Deployment
- ✅ Modular Tool Routing

---

# 👨‍💻 Author

Developed with ❤️ using FastAPI, React, Google Gemini, PostgreSQL, and Google Cloud.

---

# 📄 License

This project is intended for educational, research, and demonstration purposes.
