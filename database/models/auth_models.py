from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from database.database import Base


# Define SQLAlchemy models

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    status = Column(String, nullable=False, default='active')
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
