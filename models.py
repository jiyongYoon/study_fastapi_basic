from sqlalchemy import Column, Integer, String, DateTime, Enum as EnumDB, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from models_enum import StatusEnum


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)


class Scheduler(Base):
    __tablename__ = "scheduler"

    id = Column(Integer, primary_key=True)
    activate = Column(EnumDB(StatusEnum), nullable=False)
    target_file = Column(String, nullable=False)


class Schedule_History(Base):
    __tablename__ = "schedule_history"

    id = Column(Integer, primary_key=True)
    act = Column(EnumDB(StatusEnum), nullable=False)
    act_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", backref="history")
    scheduler_id = Column(Integer, ForeignKey("scheduler.id"))
    scheduler = relationship("Scheduler", backref="history")