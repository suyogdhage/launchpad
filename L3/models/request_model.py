from sqlalchemy import Column,String,DateTime,ForeignKey,func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from dependencies.session import Base
import uuid

class Request(Base):
    __tablename__="requests"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    request_by=Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    description=Column(String,nullable=False)
    status=Column(String,default="pending",nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now())

    requester=relationship("Users",back_populates="requests")