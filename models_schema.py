from pydantic import BaseModel

import datetime

class User(BaseModel):
    id: int
    name: str
    create_date: datetime.datetime

    class Config:
        orm_mode = True


class Job(BaseModel):
    id: int
    activate: str
    script_file: str
    config_file: str
    cron_expression: str
    create_date: datetime.datetime

    class Config:
        orm_mode = True


class JobCreate(BaseModel):
    script_file: str
    config_file: str
    cron_expression: str


class JobUpdate(BaseModel):
    id: int
    script_file: str
    config_file: str
    cron_expression: str


class Schedule_History(BaseModel):
    id: int
    act: str
    act_date: datetime.datetime
    user_id: int
    scheduler_id: int

    class Config:
        orm_mode = True