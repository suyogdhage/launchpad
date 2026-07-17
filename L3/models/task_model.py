from sqlalchemy import Column,String,Date,DateTime,ForeignKey,func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from dependencies.session import Base
import uuid

class Task(Base):
    __tablename__="tasks"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    title=Column(String,nullable=False)
    description=Column(String,nullable=True)
    assigned_by=Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    assigned_to=Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    deadline=Column(Date,nullable=True)
    status=Column(String,default="pending",nullable=False)
    completed_at=Column(DateTime(timezone=True),nullable=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())

    creator=relationship("Users",foreign_keys=[assigned_by],back_populates="created_tasks")
    assignee=relationship("Users",foreign_keys=[assigned_to],back_populates="assigned_tasks")
    documents=relationship("Document",back_populates="task",cascade="all, delete-orphan")