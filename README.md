# 💼 CareerGraph AI

> **An intelligent, multi-agent career assistant built with Flask, LangChain, and LangGraph — powered by Google Gemini.**

CareerGraph AI helps users **analyze their profiles**, **build better resumes**, **get tailored course and project recommendations**, and **prepare for interviews** — all through an interactive chat interface.  
It integrates structured user data, dynamic AI reasoning, and a clean Flask UI to deliver an end-to-end personalized career guidance experience.

---

## 🚀 Features

### 🧑‍💻 Core Functionality
- **User Authentication** — Secure register, login, and logout system.
- **Profile Management** — Add, view, and update education, projects, skills, and experience.
- **AI-Powered Chat** — Natural conversation with a multi-agent AI system that understands your profile and goals.
- **Resume Upload Support** — Upload PDF/DOCX resumes to extract and analyze content.
- **Dynamic Recommendations** — Personalized course, project, and learning path suggestions.
- **Interview Coaching** — Mock interview assistance and skill gap analysis.
- **Resume Optimization** — Build and enhance resumes using AI-generated insights.

---

## 🧠 Architecture Overview

CareerGraph AI combines **Flask** for the web layer with **LangGraph** (built on LangChain) for orchestrating intelligent multi-agent reasoning.

```
Frontend
       ↓
Flask Routes
       ↓
Conversation Manager
       ↓
LangGraph Multi-Agent System
       ↓
Specialized Agents
       ↓
Google Gemini LLM
```

Each layer has a defined purpose:
- **Flask** → Handles UI, user auth, sessions, and API endpoints.
- **LangGraph** → Routes user queries through a graph of domain-specific agents.
- **Agents** → Encapsulate expertise (resume builder, project recommender, etc.).
- **Gemini** → The core reasoning engine driving AI insights.

---

## 🧩 Project Structure

```
careergraph-ai/
│
├── app.py                      # Main Flask app (routes, UI, chat)
├── models.py                   # SQLAlchemy models for user data
├── state.py                    # Shared TypedDict schema for agent state
├── graph_builder.py            # LangGraph workflow construction
├── conversation_manager.py     # Manages memory and conversation routing
│
├── utils/
│   ├── llm.py                  # Initializes Gemini (Google Generative AI)
│   ├── extract_resume.py       # Extracts text from PDF/DOCX resumes
│   └── get_profile.py          # Fetches structured profile data from DB
│
├── agents/                     # Individual agent scripts
│   ├── router_agent.py
│   ├── course_recommender_agent.py
│   ├── resume_builder_agent.py
│   ├── project_recommender_agent.py
│   ├── interview_coach_agent.py
│   └── ...
│
├── templates/                  # Frontend HTML templates (Flask)
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── add_profile.html
│   └── chat.html
│
├── static/                     # CSS, images, JS
│   └── style.css
│
├── notebook/                  # Development notebook for LangGraph testing
│   └── notebook.ipynb
│
├── config.py                   # Flask configuration and secret keys
├── requirements.txt            # Python dependencies
└── README.md                   # (You are here)
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/careergraph-ai.git
cd careergraph-ai
```

### 2️⃣ Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Environment Variables
Create a `.env` file in the project root:
```bash
GOOGLE_API_KEY=your_google_gemini_api_key
SECRET_KEY=your_flask_secret_key
```

### 5️⃣ Run the Application
```bash
python app.py
```

Then open your browser at **http://127.0.0.1:5000**

---

## 🎥 Demo / Screen Record

You can watch a quick demo of CareerGraph AI in action here:  
📺 **[Screen Record Video Link](temp/video.mp4)**  
---

## 🧠 AI & Agent Flow

CareerGraph AI’s reasoning system is powered by **LangGraph**:
- The **router agent** decides which specialized agent should handle the query.
- Agents like `course_recommender`, `resume_builder`, and `interview_coach` each handle one expertise area.
- The **conversation_manager** maintains memory and context across messages.
- The **Gemini LLM** powers language understanding and reasoning.

### Example Flow:
```
User: "Can you suggest a project based on my Python skills?"
 ↓
router_agent → project_recommender_agent → Gemini → Response generated
 ↓
Flask UI renders response in chat interface
```

---

## 🗄️ Database Schema

Each user has multiple related entities:

| Model | Description |
|--------|-------------|
| **User** | Stores basic info (name, email, password hash) |
| **Education** | Degree, university, CGPA, dates |
| **Certification** | Name, issuing organization |
| **Project** | Name, description, timeline |
| **Experience** | Company, role, duration, description |
| **Skill** | List of skills per user |

---

## 🧩 Key Integrations

| Component | Purpose |
|------------|----------|
| **Flask** | Web framework for UI & API |
| **SQLAlchemy** | ORM for database management |
| **Flask-Bcrypt** | Secure password hashing |
| **LangChain + LangGraph** | Multi-agent orchestration |
| **Google Gemini API** | Core LLM reasoning engine |
| **PyMuPDF / python-docx** | Resume text extraction |
| **Flask-CORS / Flask-Session** | API and session support |

---

## 🧑‍🏫 Development Notes

- All AI logic was **prototyped and validated** inside the `notebook/` folder.
- The Flask app is modular — LangGraph can be **enabled or disabled** easily to revert to a base web app version (auth + profile only).
- Code is structured for **production readiness** and **extendability** — new agents can be plugged into `graph_builder.py`.

---

## 🎨 Frontend Overview

- Responsive, minimal UI using Flask’s Jinja templates and custom `style.css`.
- Chat interface (`chat.html`) provides a conversational layout similar to modern assistants.
- Flash messages and clean forms for all CRUD operations on profile data.

---

## 🧠 Example Use Case

1. A user logs in and adds education, projects, and skills.  
2. They upload their resume (PDF/DOCX).  
3. In the chat, they ask:
   > “What projects can I build to strengthen my data science profile?”
4. The system routes to the **Project Recommender Agent**, which uses their skill data and Gemini LLM to respond with personalized project ideas.

---

## 🧩 Future Enhancements

- ✅ LinkedIn API integration for auto-importing profiles  
- ✅ PDF Resume Builder export from AI suggestions  
- 🔄 Real-time interview simulation mode  
- 🔐 JWT-based authentication for API expansion  
- 🌐 Deployable cloud version on Render/Google Cloud Run  

---

## 💡 Tech Stack

| Layer | Technology |
|--------|-------------|
| **Frontend** | Flask Templates, CSS |
| **Backend** | Flask, SQLAlchemy, Bcrypt |
| **AI Layer** | LangChain, LangGraph |
| **LLM Engine** | Google Gemini (via LangChain) |
| **Storage** | SQLite / PostgreSQL |
| **Dev Tools** | Python, Jupyter Notebooks, VS Code |

---

## 🤝 Contributing

Pull requests are welcome!  
If you’d like to extend CareerGraph AI (e.g., add new agents, improve UI, or integrate a different LLM), please fork the repo and submit a PR.

---

## 🛡️ License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

> “CareerGraph AI isn’t just a project — it’s a personalized AI career mentor designed to help you grow, learn, and build your dream path.”
