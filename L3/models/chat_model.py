from sqlalchemy import Column,Enum,Text,DateTime
from sqlalchemy.dialects.postgresql import UUID
from dependencies.session import Base
from datetime import datetime, timezone
import uuid
import enum

class MessageRole(str, enum.Enum):
    user = "user"
    assistant = "assistant"

class Chat(Base):
    __tablename__="chat"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_id = Column(UUID, nullable=False)
    role = Column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
