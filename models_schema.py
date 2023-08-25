from pydantic import BaseModel

import datetime

class User(BaseModel):
    id: int
    name: str
    create_date: datetime.datetime

    class Config:
        orm_mode = True


class Scheduler(BaseModel):
    id: int
    activate: str
    target_file: str

    class Config:
        orm_mode = True


class Schedule_History(BaseModel):
    id: int
    act: str
    act_date: datetime.datetime
    user_id: int
    scheduler_id: int

    class Config:
        orm_mode = True