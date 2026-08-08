# Launchpad

A **FastAPI-based employee onboarding and task management platform** designed to serve as a "launchpad" for new hires. Employees can receive tasks, upload documents, submit requests, track their onboarding progress, and interact with an AI-powered **Onboarding Buddy** assistant. HR and Manager roles oversee the process — approving documents, assigning tasks, and managing users.

**Author:** Suyog Dhage (suyog.dhage@coditas.com)  
**Version:** 0.1.0

---

## Tech Stack

| Category              | Technology                                                                 |
| --------------------- | -------------------------------------------------------------------------- |
| **Web Framework**     | [FastAPI](https://fastapi.tiangolo.com/) 0.138.x                           |
| **ASGI Server**       | [Uvicorn](https://www.uvicorn.org/) 0.51.x                                 |
| **ORM**               | SQLAlchemy 2.x (async)                                                     |
| **Database**          | PostgreSQL (async via `asyncpg`, migrations via `psycopg2`)                |
| **Migrations**        | Alembic 1.18.x                                                             |
| **Auth**              | JWT (`python-jose` + HS256), bcrypt (`passlib`)                            |
| **Validation**        | Pydantic v2 + `pydantic-settings`, `pydantic[email]`                       |
| **AI / LLM**          | Groq SDK — model `llama-3.3-70b-versatile`                                 |
| **Cloud Storage**     | Backblaze B2 (S3-compatible API via `boto3`, no card required)             |
| **Email**             | Resend SMTP (`smtplib`)                                                    |
| **Real-time**         | WebSockets (FastAPI native)                                                |
| **Build System**      | [Poetry](https://python-poetry.org/)                                       |
| **Python**            | >= 3.12                                                                    |

---

## Architecture

Layered architecture following the **Repository Pattern** with a dedicated service layer:

```
Client  →  Routes  →  Services  →  Repository  →  Database
                  ↘              ↘
                   +→ Schemas     +→ Models
```

| Layer          | Directory         | Responsibility                              |
| -------------- | ----------------- | ------------------------------------------- |
| **Routes**     | `routes/`         | API endpoint handlers (thin controllers)    |
| **Schemas**    | `schemas/`        | Pydantic models for validation/serialization|
| **Services**   | `services/`       | Business logic                              |
| **Repository** | `repository/`     | Data access layer (raw DB queries)          |
| **Models**     | `models/`         | SQLAlchemy ORM models (database tables)     |
| **Dependencies**| `dependencies/`  | Cross-cutting: auth, DB session, B2 storage, email, logging, WebSocket |
| **Agentic**    | `agentic/`        | AI Onboarding Buddy (Groq function calling) |

---

## Entity Relationship

```
Role (1) ─────< (N) Users
Users (1) ────< (N) Task        [as assignee]
Users (1) ────< (N) Task        [as creator]
Users (1) ────< (N) Document    [as uploader]
Users (1) ────< (N) Request     [as requester]
Users (1) ────< (1) Users       [self-ref: manager / team_members]
Task   (1) ────< (N) Document
```

### Models

| Entity     | Table       | Key Fields                                                                 |
| ---------- | ----------- | -------------------------------------------------------------------------- |
| **Users**   | `users`     | `id` (UUID), `email` (unique), `password` (bcrypt), `name`, `role_name` (FK → roles), `assigned_to` (FK → users, self-ref) |
| **Role**    | `roles`     | `id` (UUID), `name` (unique, seeded: `superadmin`, `hr`, `manager`, `new_hire`) |
| **Task**    | `tasks`     | `id` (UUID), `title`, `description`, `assigned_by` (FK), `assigned_to` (FK), `deadline`, `status` (default: `"pending"`), `completed_at` |
| **Document**| `documents` | `id` (UUID), `task_id` (FK), `uploaded_by` (FK), `file_path` (B2 URL), `file_size`, `status`, `rejection_reason` |
| **Request** | `requests`  | `id` (UUID), `request_by` (FK), `description`, `status` (default: `"pending"`) |
| **Chat**    | `chat`      | `id` (UUID), `user_id`, `role` (Enum: `user` / `assistant`), `content` (Text) |

---

## Features

### User & Role Management
- Register users with role assignment (`hr` or `superadmin` only)
- JWT-based login with bcrypt password hashing
- Assign new hires to managers (self-referential FK)
- Role-based access control via `role_checker()` and `access()` dependencies

### Task Management
- Create tasks as `hr` or `manager` (managers can only assign to their team)
- List assigned tasks for the current user
- Mark tasks as complete (broadcasts real-time stats update via WebSocket)

### Document Upload & Approval
- Upload documents to Backblaze B2 for a specific task
- HR can approve or reject documents (with rejection reason)
- Email notifications sent via Resend SMTP on approval

### Request System
- New hires can submit requests to their manager
- Managers can approve or reject requests from their team members

### Dashboard & Real-time Stats
- WebSocket endpoint (`/dashboard/ws`) for live dashboard updates
- Aggregate statistics (task/document counts, status breakdowns)
- Stats broadcast automatically on task completion and document approval

### AI Onboarding Buddy
- Chat-based AI assistant powered by **Groq** (`llama-3.3-70b-versatile`)
- Function calling tools:
  - `get_pending_tasks` — fetch current user's pending tasks sorted by deadline
  - `submit_request` — create a request on behalf of the user

---

## API Endpoints

### Auth (`/auth`)

| Method | Path              | Auth               | Description                     |
| ------ | ----------------- | ------------------ | ------------------------------- |
| POST   | `/auth/register`  | `hr`, `superadmin` | Register a new user             |
| POST   | `/auth/login`     | Public             | Login, returns JWT token        |
| GET    | `/auth/user`      | `hr`               | List all users                  |
| PATCH  | `/auth/assign`    | `hr`               | Assign user to a manager        |
| GET    | `/auth/me`        | Any authenticated  | Get current user profile        |

### Tasks (`/tasks`)

| Method | Path                        | Auth                    | Description                |
| ------ | --------------------------- | ----------------------- | -------------------------- |
| POST   | `/tasks/`                   | `hr`, `manager`         | Create a task              |
| GET    | `/tasks/me`                 | Any authenticated       | List my assigned tasks     |
| PATCH  | `/tasks/{task_id}/complete` | Any authenticated       | Mark task as completed     |

### Documents (`/document`)

| Method | Path                   | Auth                    | Description                    |
| ------ | ---------------------- | ----------------------- | ------------------------------ |
| POST   | `/document/create`     | Any authenticated       | Upload file for a task (to B2, max 10 MB) |
| PATCH  | `/document/approve`    | `hr`                    | Approve a document             |
| PATCH  | `/document/reject`     | `hr`                    | Reject a document (with reason)|
| PATCH  | `/document/update`     | `hr`                    | Update document status         |

### Requests (`/requests`)

| Method | Path                              | Auth                    | Description             |
| ------ | --------------------------------- | ----------------------- | ----------------------- |
| POST   | `/requests/`                      | Any authenticated       | Create a request        |
| GET    | `/requests/my`                    | Any authenticated       | List my requests        |
| GET    | `/requests/all`                   | `manager`               | List all requests       |
| PATCH  | `/requests/{request_id}/approve`  | `manager`               | Approve a request       |
| PATCH  | `/requests/{request_id}/reject`   | `manager`               | Reject a request        |

### Dashboard (`/dashboard`)

| Method | Path               | Auth | Description                          |
| ------ | ------------------ | ---- | ------------------------------------ |
| WS     | `/dashboard/ws`    | Public | Real-time dashboard stats (WebSocket) |
| GET    | `/dashboard/stats` | `hr` | Get dashboard statistics              |

### Buddy (`/buddy`)

| Method | Path          | Auth              | Description                        |
| ------ | ------------- | ----------------- | ---------------------------------- |
| POST   | `/buddy/chat` | Any authenticated | Chat with the AI Onboarding Buddy  |

---

## Getting Started

### Prerequisites

- Python >= 3.12
- [Poetry](https://python-poetry.org/docs/#installation)
- PostgreSQL database
- Backblaze B2 bucket (private; no credit card required for the 10 GB free tier)
- Resend account (verified domain + API key)
- Groq API key

### Environment Variables (`.env`)

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/launchpad
SECRET_KEY=your-jwt-secret
ACCESS_TIME_IN_MINUTES=30
ALGORITHM=HS256
SUPERADMIN_PASSWORD=your-superadmin-password

B2_ENDPOINT_URL=https://s3.us-west-002.backblazeb2.com
B2_ACCESS_KEY_ID=your-b2-key-id
B2_SECRET_ACCESS_KEY=your-b2-application-key
B2_BUCKET_NAME=your-b2-bucket

MAX_UPLOAD_SIZE_MB=10
USER_STORAGE_QUOTA_MB=50
ALLOWED_EXTENSIONS=pdf,docx,doc,txt,png,jpg,jpeg

SMTP_HOST=smtp.resend.com
SMTP_PORT=465
SMTP_USERNAME=resend
SMTP_PASSWORD=your-resend-api-key
EMAILS_FROM_EMAIL=no-reply@your-verified-domain.com
EMAIL_ENABLED=true

GROQ_API_KEY=your-groq-api-key
```

### Installation

```bash
# Install dependencies
poetry install

# Activate the virtual environment
poetry shell

# Run database migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload
```

### Database Migrations

Migrations are managed with Alembic:

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply all pending migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1
```

The migration history includes:
1. `dc6f02d99321` — Initial: `roles` and `users` tables
2. `7904e2e8787a` — Seeds: 4 roles and a superadmin user
3. `3a329b7fbfda` — `tasks`, `documents`, `requests` tables; self-referential FK on users
4. `dec1f247088f` — `chat` table with MessageRole enum

---

## Project Structure

```
L3/
├── main.py                      # FastAPI app entry point
├── config.py                    # Pydantic settings (reads .env)
├── pyproject.toml               # Project metadata & dependencies
├── alembic.ini                  # Alembic configuration
├── .env                         # Environment variables (gitignored)
├── .gitignore
├── agentic/                     # AI Onboarding Buddy
│   ├── agent.py                 # Core agent loop (Groq function calling)
│   ├── tool_def.py              # JSON tool definitions
│   └── tools.py                 # Tool implementations
├── alembic/
│   ├── env.py                   # Alembic environment
│   └── versions/                # Migration scripts
├── dependencies/                # Cross-cutting concerns
│   ├── auth.py                  # JWT auth, role checking
│   ├── deps.py                  # Dependency injection
│   ├── session.py               # DB session
│   ├── s3.py                    # Backblaze B2 (S3-compatible) client
│   ├── email_service.py         # Resend SMTP email
│   ├── loggers.py               # Logging setup
│   └── web_sockets.py           # WebSocket connection manager
├── models/                      # SQLAlchemy ORM models
│   ├── user_model.py
│   ├── role_model.py
│   ├── task_model.py
│   ├── document_model.py
│   ├── request_model.py
│   └── chat_model.py
├── repository/                  # Data access layer
│   ├── user_repo.py
│   ├── task_repo.py
│   ├── document_repo.py
│   ├── request_repo.py
│   └── dashboard_repo.py
├── routes/                      # API route handlers
│   ├── user_routes.py
│   ├── task_routes.py
│   ├── document_routes.py
│   ├── request_routes.py
│   ├── dashboard_routes.py
│   └── agent_routes.py
├── schemas/                     # Pydantic schemas
│   ├── user_schema.py
│   ├── task_schemas.py
│   ├── document_schemas.py
│   └── request_schema.py
└── services/                    # Business logic
    ├── user_services.py
    ├── task_service.py
    ├── document_service.py
    ├── request_service.py
    └── dashboard_service.py
```
