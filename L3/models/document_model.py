from sqlalchemy import Column,String,DateTime,ForeignKey,func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from dependencies.session import Base
import uuid

class Document(Base):
    __tablename__="documents"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    task_id=Column(UUID(as_uuid=True),ForeignKey("tasks.id"),nullable=False)
    uploaded_by=Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    file_path=Column(String,nullable=False)
    status=Column(String,default="pending",nullable=False)
    rejection_reason=Column(String,nullable=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())

    task=relationship("Task",back_populates="documents")
    uploader=relationship("Users",back_populates="uploaded_documents")