from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    type = Column(String(50), nullable=False)  # e.g., 'payout', 'revenue'
    status = Column(String(50), default="pending")
    provider = Column(String(50))  # e.g., 'payoneer', 'stripe'
    provider_transaction_id = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")
