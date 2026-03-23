<div align="center">

<img src="https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge" alt="Version"/>

# 🏥 LLM-Based Prior Authorization Form Generator

### AI-Powered Healthcare Prior Authorization Automation System

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![Groq](https://img.shields.io/badge/Groq-Llama_3.1-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![Gemini](https://img.shields.io/badge/Gemini-1.5_Pro-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain.com)


</div>
<div align="center">
---
<img width="1206" height="401" alt="image" src="https://github.com/user-attachments/assets/ccefa1d1-5e06-440f-8038-62a99b6e4658" />
<img width="499" height="501" alt="image" src="https://github.com/user-attachments/assets/c3da3aaf-4103-4e9a-8c6f-996ae8c70c7f" />
 </div> 

## Introduction

**LLM-Based Prior Authorization Form Generator** is an AI-powered full-stack web application that automates the Prior Authorization (PA) workflow for healthcare providers. It uses Large Language Models (LLMs) to extract structured clinical data from unstructured SOAP notes, auto-populates 30+ field PA forms, manages the complete submission-review-approval lifecycle, and generates downloadable PDF reports for approved requests.

> Prior authorization affects millions of patients annually. This system reduces manual data entry, eliminates delays, and brings transparency to the entire PA process — from form creation to final decision.

---

## Table of Contents

- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Folder Structure](#folder-structure)
- [Key Files](#key-files)
- [AI / LLM Pipeline](#ai--llm-pipeline)
- [Role-Based Access Control](#role-based-access-control)
- [PA Lifecycle](#pa-lifecycle)
- [Mock Test Scenarios](#mock-test-scenarios)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Database Design](#database-design)
- [PDF Generation](#pdf-generation)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)


---

## Key Features

### 🤖 AI Auto-Fill from Clinical Notes
Paste any SOAP note or clinical summary → the LLM automatically extracts and populates all form fields including ICD-10 codes, CPT codes, medication details, patient demographics, prescriber info, clinical history, and failed treatments.

### 🔄 Dual LLM Provider with Automatic Fallback
- **Primary:** Groq (Llama-3.1-8B-Instant) — fast inference, low latency
- **Fallback:** Google Gemini 1.5 Pro — automatic switchover when Groq is unavailable
- Orchestrated via **LangChain** for seamless provider switching

### 📋 Complete Prior Authorization Lifecycle
Submit → Review → Approve / Reject → Download PDF — full workflow managed digitally with real-time status tracking.

### 👥 Role-Based Access Control (3 Roles)
| Role | Capabilities |
|------|-------------|
| **User** (Clinician) | Submit PA forms, view own forms, track status, download approved PDFs |
| **Manager** | View all PA submissions, search/filter across users |
| **Admin** | Approve/reject PAs, add reviewer comments, view analytics dashboard |

### 📄 Professional PDF Generation
ReportLab-powered PDF export for approved PA forms with color-coded status, reviewer details, two-column layout, and branded header/footer.

### 🧪 Mock Data Testing Panel
6 clinically accurate pre-built scenarios for testing — one click fills all 30+ fields.

### 📊 Analytics Dashboard
Track total submissions, approval rates, average processing time, and recent activity logs.

### 🔒 JWT Authentication & Security
Secure token-based authentication with bcrypt password hashing and role-enforced endpoint protection.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | FastAPI (Python 3.10) | REST API framework, async endpoints |
| **LLM Primary** | Groq — Llama-3.1-8B-Instant | Clinical notes analysis, field extraction |
| **LLM Fallback** | Google Gemini 1.5 Pro | Automatic fallback provider |
| **LLM Orchestration** | LangChain (`langchain-groq`, `langchain-google-genai`) | Unified LLM interface, provider switching |
| **Database** | MongoDB  | NoSQL storage for PA records and users |
| **PDF Generation** | ReportLab | Server-side professional PDF creation |
| **Authentication** | python-jose (JWT) + passlib (bcrypt) | Token auth, password hashing |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript | PA forms, dashboards, status pages |
| **ASGI Server** | Uvicorn | Production-grade async server |
| **Env Management** | python-dotenv | Secure API key management |
| **NLP Support** | nlp_services.py | Supplementary text processing |

---

## Architecture

```
User Browser (Frontend)
  auth.html | dashboard.html | pa_form.html | pa_list.html | pdf_viewer.html
       |
       |  REST API calls (fetch / JSON)
       v
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                         │
│   /api/auth  |  /api/pa  |  /api/notes  |  /api/analytics  │
│   /admin/users  |  /api/pa/{id}/download                   │
└──────┬──────────────┬────────────────┬───────────────────── ┘
       │              │                │
  MongoDB        ReportLab         LangChain LLM Service
  (pa_requests,  PDF Generation    ┌─────────────────────┐
   users)                          │  Groq (Primary)     │
                                   │  Llama-3.1-8B       │
                                   │         ↓ fallback  │
                                   │  Gemini 1.5 Pro     │
                                   └─────────────────────┘
```

### Detailed Flow

```
POST /api/notes/analyze
       │
       ├─► LangChain get_llm()
       │         ├─► Try Groq (Llama-3.1-8B-Instant)
       │         └─► Fallback: Google Gemini 1.5 Pro
       │
       └─► Returns structured JSON
               { medication, diagnosis, icd10, cpt,
                 patient_info, prescriber_info,
                 history, failed_treatments, urgency }
                       │
                       ▼
              pa_form.html auto-fills
              all 30+ fields with
              green visual feedback
```

---

## Folder Structure

```
pa-form-generator/
│
├── backend/
│   └── app/
│       ├── api/
│       │   ├── pa.py              # PA lifecycle endpoints
│       │   ├── auth.py            # Login, register, JWT
│       │   ├── notes.py           # LLM notes analysis
│       │   └── Analytics.py       # Stats & dashboard data
│       │
│       ├── auth/
│       │   ├── admin_routes.py    # Admin-only user management
│       │   ├── auth_services.py   # Auth business logic
│       │   ├── deps.py            # Role dependency injectors
│       │   ├── jwt.py             # Token encode/decode
│       │   └── schemas.py         # Pydantic auth models
│       │
│       ├── services/
│       │   ├── llm_service.py     # Groq + Gemini fallback LLM
│       │   ├── pdf_service.py     # ReportLab PDF generation
│       │   ├── nlp_services.py    # Text processing utilities
│       │   ├── pa_generator.py    # PA content generation
│       │   └── email_service.py   # Email notifications
│       │
│       ├── storage/
│       │   ├── db.py              # MongoDB connection
│       │   └── pa_repo.py         # PA CRUD operations
│       │
│       ├── main.py                # FastAPI app entry point
│       └── config.py              # Settings, env variables
│
├── frontend/
│   ├── auth.html                  # Login / Register
│   ├── dashboard.html             # Role-aware dashboard
│   ├── pa_form.html               # 30+ field PA form + AI auto-fill
│   ├── pa_list.html               # User's PA forms with status
│   ├── pa_status.html             # Single PA detail + download
│   ├── pdf_viewer.html            # In-browser PDF viewer
│   ├── style.css                  # Global styles
│   └── api.js                     # API helper functions
│
├── .env                           # Environment variables (not committed)
├── .gitignore
└── requirements.txt
```

---

## Key Files

| File | Purpose | Key Functions |
|------|---------|---------------|
| `backend/app/main.py` | FastAPI app entry, router mounting, CORS, static files | `lifespan`, `root_status`, `health` |
| `backend/app/api/pa.py` | Full PA lifecycle API | `save_pa`, `get_pa_list`, `approve_pa`, `download_pdf`, `serialize_pa` |
| `backend/app/api/notes.py` | LLM clinical notes analysis | `analyze_notes` |
| `backend/app/services/llm_service.py` | Dual LLM with fallback | `get_llm`, `get_groq_llm`, `get_gemini_llm` |
| `backend/app/services/pdf_service.py` | ReportLab PDF generation | `generate_pa_pdf` |
| `backend/app/storage/pa_repo.py` | MongoDB PA operations | `create_pa`, `get_pa`, `get_all_pa_by_user`, `update_pa_status` |
| `backend/app/auth/deps.py` | Role-based access dependencies | `get_current_user`, `require_manager`, `require_admin` |
| `frontend/pa_form.html` | 7-section collapsible PA form | AI auto-fill, radio buttons, checkboxes, signature canvas |
| `frontend/mock_data.html` | 6 pre-built clinical scenarios | One-click form population for testing |

---

## AI / LLM Pipeline

### Provider Strategy

```python
# llm_service.py — Automatic Fallback Architecture
def get_llm(temperature=0.1, max_tokens=2000):
    """Primary: Groq (Llama-3.1-8B)  |  Fallback: Gemini 1.5 Pro"""
    try:
        return ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="llama-3.1-8b-instant",
            temperature=temperature,
            max_tokens=max_tokens
        )
    except Exception as e:
        print(f"[LLM] Groq failed, switching to Gemini: {e}")
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=GEMINI_API_KEY,
            temperature=temperature,
            max_tokens=max_tokens
        )
```

### What the LLM Extracts from Clinical Notes

Given a SOAP note, the LLM returns a structured JSON with:

```json
{
  "medication": "Metformin 500mg",
  "strength": "500mg oral tablet",
  "frequency": "Twice daily (BID)",
  "diagnosis": "Type 2 Diabetes Mellitus - E11.9",
  "cpt": "99213",
  "history": "HbA1c 9.2%, fasting glucose 210 mg/dL...",
  "failed": "Dietary modification x6 months without improvement",
  "urgency": "Standard",
  "patient_first_name": "John",
  "patient_last_name": "Smith",
  "patient_dob": "1966-05-14",
  "prescriber_first": "Sarah",
  "prescriber_last": "Johnson",
  "npi": "1234567890"
}
```

---

## Role-Based Access Control

```
┌─────────────────────────────────────────────────────────────┐
│  JWT Token  →  Role Claim  →  Dependency Injector          │
│                                                             │
│  get_current_user()   →  Any authenticated user            │
│  require_manager()    →  Manager or Admin                  │
│  require_admin()      →  Admin only                        │
└─────────────────────────────────────────────────────────────┘

Role Permissions:
  User    → Submit forms, view own PA list, track status, download approved PDFs
  Manager → View ALL PA forms, search/filter, export data
  Admin   → Approve/reject PAs, reviewer comments, analytics, user management
```

---

## PA Lifecycle

```
  Clinician                   System                    Admin
     │                           │                        │
     │── Fill PA Form ──────────►│                        │
     │   (manual or AI auto-fill)│                        │
     │                           │── Save to MongoDB ──►  │
     │                           │   status: DRAFT        │
     │                           │                        │
     │                           │◄── Review PA ─────────│
     │                           │                        │── Approve / Reject
     │                           │── Update status ──────►│   + add comments
     │                           │   APPROVED / REJECTED  │
     │                           │                        │
     │◄── View Status ──────────│                        │
     │    (pa_status.html)       │                        │
     │                           │                        │
     │── Download PDF ──────────►│                        │
     │   (APPROVED only)         │── ReportLab PDF ──────►│
     │◄── PDF File ─────────────│                        │
```

---

## Mock Test Scenarios

The `mock_data.html` panel provides 6 complete clinical scenarios — one click fills all 30+ form fields for end-to-end testing:

| # | Specialty | Condition | Medication | ICD-10 | CPT | Urgency |
|---|-----------|-----------|------------|--------|-----|---------|
| 1 | Primary Care | Type 2 Diabetes | Metformin 500mg BID | E11.9 | 99213 | Standard |
| 2 | Cardiology | Atrial Fibrillation | Apixaban (Eliquis) 5mg | I48.91 | 93000 | Urgent |
| 3 | Rheumatology | Rheumatoid Arthritis | Adalimumab (Humira) 40mg | M05.79 | J0135 | Urgent |
| 4 | Neurology | Multiple Sclerosis | Ocrelizumab (Ocrevus) 300mg IV | G35 | J2350 | Urgent |
| 5 | Oncology | HER2+ Breast Cancer | Trastuzumab (Herceptin) 8mg/kg | C50.911 | J9355 | Urgent |
| 6 | Psychiatry | Treatment-Resistant MDD | Esketamine (Spravato) 56mg | F32.2 | S0013 | Standard |

---

## Getting Started

### Prerequisites

- Python 3.10+
- MongoDB 6.0+ (local or [MongoDB Atlas](https://www.mongodb.com/atlas))
- Groq API Key → [console.groq.com](https://console.groq.com) *(free tier available)*
- Gemini API Key → [ai.google.dev](https://ai.google.dev) *(free tier available)*

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/pa-form-generator.git
cd pa-form-generator
```

**2. Create and activate a virtual environment**

Windows:
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Linux / macOS:
```bash
python -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**4. Create your `.env` file**
```bash
# backend/.env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_URL=mongodb://localhost:27017
DB_NAME=pa_form_db
SECRET_KEY=your_jwt_secret_key_here_make_it_long
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=2000
```

**5. Start MongoDB** *(if running locally)*
```bash
mongod --dbpath C:\data\db        # Windows
# or
mongod --dbpath /data/db           # Linux/macOS
```

**6. Run the application**
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**7. Open in browser**
```
http://localhost:8000
```

> The app will redirect to `http://localhost:8000/frontend/auth.html`

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes* | Groq API key for Llama-3.1-8B (*at least one LLM key required) |
| `GEMINI_API_KEY` | Yes* | Google Gemini API key (fallback LLM) |
| `MONGODB_URL` | Yes | MongoDB connection string |
| `DB_NAME` | Yes | MongoDB database name |
| `SECRET_KEY` | Yes | JWT signing secret (use a long random string) |
| `LLM_TEMPERATURE` | No | LLM response randomness (default: `0.1`) |
| `LLM_MAX_TOKENS` | No | Max tokens per LLM response (default: `2000`) |

---

## API Reference

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/auth/register` | No | Register new user |
| `POST` | `/api/auth/login` | No | Login; returns JWT token |
| `GET` | `/api/auth/me` | Yes | Get current user profile |

### Prior Authorization

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/pa/save` | User | Submit PA form as DRAFT |
| `GET` | `/api/pa/list` | User | Get current user's PA forms |
| `GET` | `/api/pa/all` | Manager/Admin | Get all PA forms |
| `GET` | `/api/pa/{id}` | User (owner) or Admin | Get single PA form |
| `POST` | `/api/pa/{id}/approve` | Admin | Approve or reject PA with comments |
| `GET` | `/api/pa/{id}/download` | User (owner) | Download PDF for approved PA |

### AI & Analytics

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/notes/analyze` | User | Analyze clinical notes with LLM |
| `GET` | `/api/analytics/stats` | Manager/Admin | PA statistics and trends |
| `GET` | `/admin/users` | Admin | All registered users |

### Sample: AI Notes Analysis

```bash
curl -X POST "http://localhost:8000/api/notes/analyze" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "notes": "Patient: John Smith, DOB 05/14/1966. Dx: Type 2 DM (E11.9). Requesting Metformin 500mg BID. HbA1c 9.2%. Failed dietary modification x6mo. CPT: 99213."
  }'
```

**Expected response:**
```json
{
  "medication": "Metformin",
  "strength": "500mg",
  "frequency": "Twice daily (BID)",
  "diagnosis": "Type 2 Diabetes Mellitus - E11.9",
  "cpt": "99213",
  "patient_first_name": "John",
  "patient_last_name": "Smith",
  "patient_dob": "1966-05-14",
  "history": "HbA1c 9.2%, fasting glucose elevated",
  "failed": "Dietary modification x6 months without improvement",
  "urgency": "Standard"
}
```

---

## Database Design

### Collection: `users`

```json
{
  "_id": "ObjectId",
  "email": "user@clinic.com",
  "hashed_password": "bcrypt_hash",
  "role": "user | manager | admin",
  "created_at": "ISO timestamp"
}
```

### Collection: `pa_requests`

```json
{
  "_id": "ObjectId",
  "medication": "Metformin 500mg",
  "diagnosis": "Type 2 Diabetes - E11.9",
  "history": "Clinical history text...",
  "frequency": "Twice daily",
  "cpt": "99213",
  "urgency": "Standard",
  "status": "DRAFT | APPROVED | REJECTED",
  "created_by": "user@clinic.com",
  "created_at": "ISO timestamp",
  "reviewer": "Admin Name",
  "reviewed_at": "ISO timestamp",
  "comments": "Reviewer decision notes",
  "patient_first_name": "John",
  "patient_last_name": "Smith",
  "patient_dob": "1966-05-14",
  "patient_sex": "Male",
  "member_id": "INS123456",
  "npi": "1234567890",
  "prescriber_first": "Sarah",
  "prescriber_last": "Johnson"
}
```

---

## PDF Generation

Approved PA forms generate professional PDFs using **ReportLab**:

- 🔵 Branded blue header with form title and PA ID
- ✅ Color-coded APPROVED status badge (green)
- Two-column layout for compact field display
- Full-width sections for clinical history and failed treatments
- Reviewer decision box with timestamp and reviewer name
- Auto-generated footer with creation date

> PDF download is **restricted to APPROVED status only** — draft and rejected forms are not downloadable.

---

## Frontend Pages

| Page | Description |
|------|-------------|
| `auth.html` | Login / Register with JWT session |
| `dashboard.html` | Role-aware: Users see summaries; Managers see all PA table; Admins see review panel + analytics |
| `pa_form.html` | 7-section collapsible 30+ field form with AI auto-fill, signature canvas, and file upload |
| `pa_list.html` | Color-coded PA table: 🟢 Approved (with Download button) · 🟡 Pending · 🔴 Rejected |
| `pa_status.html` | Full detail view: green/blue/red hero banner + Download CTA for approved forms |
| `pdf_viewer.html` | In-browser PDF viewer |
| `mock_data.html` | 6 clinical scenario cards — one click fills all form fields for testing |

---

## Production Deployment

```bash
# Using gunicorn with uvicorn workers
pip install gunicorn
cd backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Docker (recommended)**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Production checklist:**
- [ ] Set `SECRET_KEY` to a cryptographically random 64-char string
- [ ] Enable HTTPS (nginx reverse proxy or cloud load balancer)
- [ ] Use MongoDB Atlas or a secured MongoDB instance
- [ ] Restrict `allow_origins` in CORS config to your domain
- [ ] Store `.env` securely — never commit to version control

---

## Troubleshooting

**LLM auto-fill not working**
```
Check GROQ_API_KEY and GEMINI_API_KEY in .env
The system will try Groq first, then auto-switch to Gemini
At least one valid API key is required
```

**MongoDB connection error**
```
Ensure MongoDB is running: mongod --dbpath /data/db
Check MONGODB_URL in .env matches your MongoDB instance
For Atlas: use the full connection string from your cluster dashboard
```

**PDF download fails (403)**
```
PDF download is only available for APPROVED PA forms
Ask your admin to approve the form first
```

**Frontend pages not loading**
```
Ensure frontend/ folder exists at the project root (pa-form-generator/frontend/)
The server mounts /frontend as a static directory from this path
```

**Port already in use**
```powershell
# Windows: find and kill the process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## Future Improvements

- [ ] **FHIR API Integration** — Connect to Epic/Cerner EHR systems for auto-import of patient data
- [ ] **Real-Time Payer Connectivity** — Integrate with insurance payer APIs (Availity, CoverMyMeds)
- [ ] **Email Notifications** — Notify clinicians when PA status changes to APPROVED/REJECTED
- [ ] **Fine-Tuned Clinical LLM** — Train a dedicated model on PA-specific documents for higher extraction accuracy
- [ ] **Cloud Deployment** — AWS EC2 + DocumentDB or Azure with Docker + CI/CD pipeline
- [ ] **Mobile App** — React Native app for on-the-go PA management
- [ ] **Multi-Payer Support** — Payer-specific form templates and submission rules
- [ ] **HIPAA Audit Logging** — Comprehensive audit trails for all PA actions
- [ ] **Redis Cache** — Replace in-memory session data with Redis for multi-worker deployments
- [ ] **Bulk PA Upload** — CSV import for submitting multiple PA requests at once

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature description"`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please ensure your code follows the existing structure and includes appropriate error handling.

---

## Author

**Meghana Kamatam**
M.S. Data Science — Sri Venkateswara University, Tirupati
Academic Year: 2024 – 2026

---

## Languages

![Python](https://img.shields.io/badge/Python-36.5%25-3776AB?style=flat-square&logo=python)
![JavaScript](https://img.shields.io/badge/JavaScript-28.0%25-F7DF1E?style=flat-square&logo=javascript)
![HTML](https://img.shields.io/badge/HTML-27.0%25-E34F26?style=flat-square&logo=html5)
![CSS](https://img.shields.io/badge/CSS-8.5%25-1572B6?style=flat-square&logo=css3)

---


<div align="center">

Made with ❤️ for Healthcare Automation

⭐ If this project helped you, please give it a star!

</div>
