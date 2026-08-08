from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user_routes import router as user
from routes.task_routes import router as task
from routes.document_routes import router as document
from routes.dashboard_routes import router as dashboard
from routes.request_routes import router as Request
from routes.agent_routes import router as agent
from routes.notification_routes import router as notification

app = FastAPI(title="Launchpad")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user)
app.include_router(task)
app.include_router(document)
app.include_router(dashboard)
app.include_router(Request)
app.include_router(agent)
app.include_router(notification)
