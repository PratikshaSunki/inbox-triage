from sqlalchemy import Column, String, Text, DateTime, Boolean
from sqlalchemy.sql import func

from db import Base


class Email(Base):
    __tablename__ = "emails"
    gmail_id = Column(String, primary_key=True)

    sender = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    snippet = Column(Text, nullable=True)
    body = Column(Text, nullable=True)

    # these fields stay null for now for future steps
    category = Column(String, nullable=True)
    urgency_score = Column(String, nullable=True)
    needs_reply = Column(Boolean, nullable=True)
    draft_reply = Column(Text, nullable=True)

    fetched_at = Column(DateTime(timezone=True), server_default=func.now())