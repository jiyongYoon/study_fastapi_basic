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


class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True)
    activate = Column(EnumDB(StatusEnum), nullable=False, default=StatusEnum.STOP)
    script_file = Column(String, nullable=False)
    config_file = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)
    cron_expression = Column(String, default="0 0 * * *")


class Schedule_History(Base):
    __tablename__ = "schedule_history"

    id = Column(Integer, primary_key=True)
    act = Column(EnumDB(StatusEnum), nullable=False)
    act_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", backref="history")
    job_id = Column(Integer, ForeignKey("job.id"))
    job = relationship("Job", backref="history")