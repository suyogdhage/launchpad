from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from dependencies.session import Base
import uuid

class Users(Base):
    __tablename__="users"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    name=Column(String,nullable=False)
    role_name=Column(String,ForeignKey("roles.name"),nullable=False,default="new_hire")
    assigned_to=Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())

    role=relationship("Role",back_populates="users")
    manager=relationship("Users",remote_side=[id],back_populates="team_members")
    team_members=relationship("Users",back_populates="manager")
    assigned_tasks=relationship("Task",foreign_keys="Task.assigned_to",back_populates="assignee")
    created_tasks=relationship("Task",foreign_keys="Task.assigned_by",back_populates="creator")
    uploaded_documents=relationship("Document",back_populates="uploader")
    requests=relationship("Request",back_populates="requester")