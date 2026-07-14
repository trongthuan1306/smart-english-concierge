# Smart English Concierge - Project Documentation

## 1. Overview

Smart English Concierge is an AI-powered English learning assistant built as a full-stack application with a multi-agent architecture. The system is designed to help users practice English through conversational interaction, vocabulary saving, and intelligent skill-based assistance.

The project combines:
- A FastAPI backend for API services and agent orchestration
- A React + Vite frontend for the user interface
- Google Gemini for language understanding and routing
- PostgreSQL for persistent vocabulary storage
- A modular skills system that can be extended easily

---

## 2. Project Goal

The main objective of this project is to provide a more intelligent and personalized English learning experience than a traditional chatbot. Instead of relying on a single monolithic AI response, the application uses multiple specialized agent skills to handle different user intents.

Examples of supported behavior:
- Chatting in English
- Saving vocabulary words
- Returning structured responses from specialized skills
- Protecting user data from prompt injection and privacy leaks

---

## 3. Main Features

### Core features
- AI-powered English conversation
- Vocabulary saving to database
- Intent-based routing via an agent router
- Multi-skill architecture
- Security guardrails for prompt injection and PII masking
- REST API backend
- Modern frontend interface

### Additional capabilities
- Extensible skill folders under the backend skills directory
- Database-backed learning memory
- Support for deployment on Google Cloud

---

## 4. Architecture Summary

The system is organized into two major parts:

### Backend
The backend is a Python application powered by FastAPI. Its responsibilities include:
- Receiving chat requests from the frontend
- Applying security checks to user message input
- Routing the request to the correct skill or agent
- Executing logic and interacting with the database
- Returning a structured response to the frontend

### Frontend
The frontend is a React application using Vite and Tailwind CSS. It provides:
- A chat interface
- A vocabulary dashboard or notebook view
- API calls to the backend

---

## 5. Folder Structure

```text
smart-english-concierge/
├── backend/
│   ├── agents/
│   │   ├── router.py
│   │   ├── security.py
│   │   └── skills/
│   │       ├── vocab-saver/
│   │       └── ...
│   ├── database/
│   │   ├── crud.py
│   │   ├── database.py
│   │   └── models.py
│   ├── models/
│   │   └── schemas.py
│   ├── main.py
│   ├── requirements.txt
│   └── test_real.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── README.md
└── project_overview.md
```

---

## 6. Backend Components

### 6.1 FastAPI entry point
The main application entry point is [backend/main.py](backend/main.py).

It exposes:
- POST /api/chat for chat interactions
- GET /api/vocabulary to retrieve saved vocabulary

The endpoint flow is:
1. Receive a message from the client
2. Run the security guardrail
3. Pass the sanitized message to the router
4. Return the final response

### 6.2 Security guardrail
The security layer is implemented in [backend/agents/security.py](backend/agents/security.py).

It performs:
- Prompt injection detection using a list of forbidden phrases
- PII redaction for phone numbers and emails

If suspicious content is detected, the request is rejected safely.

### 6.3 Router and skill orchestration
The router in [backend/agents/router.py](backend/agents/router.py) is the central orchestrator.

Its responsibilities include:
- Scanning the skills directory at startup
- Reading each skill definition from SKILL.md
- Building a skill catalog for the LLM
- Letting Gemini choose the best matching skill
- Dynamically importing and calling the relevant handler

This design makes the system highly extensible because new skills can be added by creating a new folder with a SKILL.md file and an optional handler script.

### 6.4 Database layer
The database layer is located in [backend/database](backend/database).

Key files:
- [backend/database/database.py](backend/database/database.py): SQLAlchemy engine and session setup
- [backend/database/models.py](backend/database/models.py): database model for vocabulary
- [backend/database/crud.py](backend/database/crud.py): database operations

The application currently stores vocabulary entries with fields such as:
- word
- meaning
- example
- created_at

### 6.5 Schemas
The request and response payloads are defined in [backend/models/schemas.py](backend/models/schemas.py).

They use Pydantic models for validation and structured JSON responses.

---

## 7. Frontend Components

The frontend is built in [frontend/src](frontend/src).

Key areas:
- [frontend/src/components](frontend/src/components): UI components such as chat view, dashboard, and vocabulary notebook
- [frontend/src/services/api.js](frontend/src/services/api.js): API service layer for communicating with the backend
- [frontend/src/App.jsx](frontend/src/App.jsx): main application page

The frontend relies on Axios to call the backend endpoints.

---

## 8. Main Data Flow

A typical request flow is:

1. User enters a message in the frontend
2. Frontend sends the message to the backend API
3. Backend runs security checks
4. The router decides which skill should handle the request
5. The selected skill executes its handler logic
6. The result is returned to the frontend
7. The UI renders the response

---

## 9. Development Stack

### Backend stack
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Google GenAI
- Python-dotenv
- PostgreSQL

### Frontend stack
- React
- Vite
- Tailwind CSS
- Axios
- Lucide React

---

## 10. How to Extend the Project

New capabilities can be added by creating a new skill directory under [backend/agents/skills](backend/agents/skills).

A new skill usually includes:
- A SKILL.md file describing the skill
- A scripts/handler.py file containing the actual logic

Because the router scans the skills directory automatically, no hard-coded router modification is required for simple additions.

---

## 11. Notes for AI/LLM Understanding

This project is a strong example of:
- Multi-agent style architecture
- Tool-based LLM routing
- Modular skill design
- Security-aware AI application development
- Full-stack integration between frontend and backend

A future AI agent reading this documentation should understand that the project is not just a simple chatbot; it is a modular system where specialized skills can be composed into a broader English-learning assistant.

---

## 12. Suggested Next Steps

Possible future improvements include:
- Adding more learning skills such as grammar correction or pronunciation help
- Improving the router with more explicit tool selection logic
- Adding authentication and user profiles
- Expanding the database schema for learning history and progress tracking
- Deploying the backend and frontend more robustly in production
