# 🚀 Project Status: Smart English Concierge

**Track:** Kaggle 5-Day AI Agents Capstone Project (Concierge Track)  
**Last Updated:** July 2026

---

## 📖 Project Overview
**Smart English Concierge** is an intelligent, fullstack AI application designed to assist users in practicing and improving their English. Utilizing a modular, multi-agent architecture powered by Google's Gemini LLM, the concierge provides personalized tutoring, vocabulary saving, grammar checking, and more, all while ensuring user privacy and data security.

---

## 🏗️ Current Architecture

The project is divided into a Python/FastAPI backend and a React/Vite frontend.

### 📂 Directory Structure
```text
smart-english-concierge/
├── backend/
│   ├── agents/
│   │   ├── router.py         # Multi-Agent Graph Router (Core Orchestrator)
│   │   ├── security.py       # PII Redaction & Prompt Injection Defense
│   │   └── skills/           # Modular Skill Definitions
│   │       ├── vocab-saver/
│   │       │   ├── SKILL.md  # LLM Tool Specification
│   │       │   └── scripts/handler.py # Executable Logic
│   │       └── ... (8 other skills)
│   ├── data/                 # Local JSON Database
│   │   ├── analytics.json
│   │   └── saved_vocabulary.json
│   ├── tests/
│   │   └── test_router_simulation.py # Offline Mock Tests
│   └── main.py               # FastAPI Entry Point (Stub)
└── frontend/                 # React + Vite + TailwindCSS
    └── src/
        ├── components/       # ChatWindow, Dashboard, Sidebar, VocabNotebook
        └── services/api.js   # Axios API Client
```

### 🧠 Core Components
1. **`router.py` (The Orchestrator):** Implements an ADK 2.0 Graph Routing pattern. It automatically discovers skills from the `skills/` directory, builds dynamic tool declarations, uses the Gemini LLM to interpret user intent, and executes the appropriate skill handler.
2. **`security.py` (The Guard):** Ensures safe interactions by filtering out prompt injection attempts and redacting sensitive PII (phone numbers, emails) before the data reaches the LLM.
3. **`skills/` Directory (The Workforce):** A highly scalable, zero-code registration system. Each subdirectory contains a `SKILL.md` (defining what the skill does and its parameters) and an optional `scripts/handler.py` (the Python logic executed when the skill is invoked).
4. **`tests/test_router_simulation.py`:** A robust test suite that uses `unittest.mock` to simulate Gemini API responses, verifying the routing logic entirely offline.

---

## ✅ Progress Checklist (Kaggle Requirements)

| Kaggle Concept | Status | Implementation Details |
|---|:---:|---|
| **Multi-agent / Agentic Workflow** | 🟢 **Done** | Implemented via `SkillRouter` and `SkillRegistry`. The router acts as the primary decision node, dynamically routing tasks to specialized skill nodes based on Gemini's tool-calling output. |
| **Custom Agent Skills** | 🟡 **In Progress** | Modular architecture is fully built. 9 skills are auto-discovered via `SKILL.md`. The `vocab-saver` skill has a fully functioning handler, but the remaining 8 skills need their `handler.py` implemented. |
| **Security Guardrails** | 🟢 **Done** | `security.py` is implemented with RegEx-based PII redaction and keyword-based prompt injection defense. |

---

## 🚧 Missing Pieces (Next Steps)

To cross the finish line, the following tasks must be completed:

- [ ] **Integrate Real Gemini API in Production:** The router currently supports the `genai.Client`, but we need to wire it up to the FastAPI endpoints in `backend/main.py` so the frontend can communicate with the live LLM.
- [ ] **Implement Remaining Skill Handlers:** Write the `scripts/handler.py` logic for essential skills like `grammar-checker`, `pii-redactor` (integrating the security module), and `voice-synthesis-trigger`.
- [ ] **Build the Frontend:** Connect the scaffolding components (`ChatWindow`, `VocabNotebook`, `Dashboard`) to the FastAPI backend using the pre-configured `axios` client. Ensure state updates dynamically as skills are triggered.
- [ ] **Deployment:** Dockerize the application or deploy the backend to a cloud provider (e.g., Google Cloud Run) and the frontend to Vercel/Netlify.

---

## 🔧 Technical Debt & Notes

- **`backend/main.py` is a stub:** Currently just a placeholder. Needs standard FastAPI boilerplate, CORS middleware, and API routes (e.g., `/api/chat`).
- **`backend/models/schemas.py` is empty:** Pydantic models should be defined here for strict API request/response validation between the React frontend and FastAPI backend.
- **Frontend State Management:** We will need a robust way to handle the chat history and real-time updates to the vocabulary notebook and analytics dashboard in React. Context API or Zustand is recommended.
