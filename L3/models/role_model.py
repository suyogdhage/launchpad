from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from dependencies.session import Base
import uuid

class Role(Base):
    __tablename__="roles"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name=Column(String,unique=True,nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now())

    users=relationship("Users",back_populates="role")