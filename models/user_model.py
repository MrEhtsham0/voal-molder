# from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from config.database import Base


class UserModel(Base):
    __tablename__ = 'UsersData'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=False, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(128), unique=False, index=True)
    generated_voices = Column(Integer, default=0)
    join_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
