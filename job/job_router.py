from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import *

from datetime import datetime

from starlette import status

from job.scheduler import *

router = APIRouter(
    prefix="/api/jobs",
)

from database import get_db
import models_schema
from models import *

from models_enum import StatusEnum

from typing import List

from apscheduler.schedulers.background import BackgroundScheduler

from job import job_crud

scheduler = BackgroundScheduler()


job_dic = {}


@router.get("", response_model=models_schema.JobList)
def job_list(db: Session = Depends(get_db),
             page: int = 0,
             size: int = 10):
    total, _job_list = job_crud.get_job_list(db, skip=page*size, limit=size)
    return {
        'total': total,
        'job_list': _job_list
    }


@router.get("/activating", response_model=models_schema.JobList)
def activating_job_list(db: Session = Depends(get_db),
                        page: int = 0,
                        size: int = 10):
    total, _activating_job_list = job_crud.get_activate_job_list(db, skip=page*size, limit=size)
    return {
        'total': total,
        'job_list': _activating_job_list
    }


@router.get("/{job_id}", response_model=models_schema.Job)
def get_job(job_id: int, db: Session = Depends(get_db)):
    find_job = job_crud.get_job(job_id, db)
    if not find_job:
        raise HTTPException(status_code=404, detail="id-not-exist")
    return find_job


@router.post("", status_code=status.HTTP_200_OK, response_model=models_schema.Job)
def create_job(_job_create: models_schema.JobCreate,
                     db: Session = Depends(get_db)):
    db_job = Job(activate=StatusEnum.STOP,
                 create_date=datetime.now(),
                 script_file=_job_create.script_file,
                 config_file=_job_create.config_file,
                 cron_expression=_job_create.cron_expression)

    db.add(db_job)
    db.commit()

    return db_job


@router.put("", status_code=status.HTTP_200_OK, response_model=models_schema.Job)
def update_job(_job_update: models_schema.JobUpdate,
                     db: Session = Depends(get_db)):

    if hasattr(_job_update, 'id') and _job_update.id != 0:
        db_job: Job = job_crud.get_job(_job_update.id, db)
        if not db_job:
            raise HTTPException(status_code=404, detail="id-not-exist")
        else:
            db_job.config_file = _job_update.config_file
            db_job.script_file = _job_update.script_file
            db_job.cron_expression = _job_update.cron_expression
            db.add(db_job)
            db.commit()

            return db_job
    else:
        raise HTTPException(status_code=400, detail="request-not-valid")


@router.delete("", status_code=status.HTTP_200_OK, response_model=models_schema.Job)
def delete_job(job_id: int,
                     db: Session = Depends(get_db)):

    db_job: Job = job_crud.get_job(job_id, db)
    if not db_job:
        raise HTTPException(status_code=404, detail="id-not-exist")
    else:
        db.delete(db_job)
        db.commit()

        return db_job


@router.post("/{job_id}/activate")
def activate_job(job_id: int,
                       db: Session = Depends(get_db)):

    db_job: Job = job_crud.get_job(job_id, db)
    if not db_job:
        raise HTTPException(status_code=404, detail="id-not-exist")
    job = scheduler.get_job(str(db_job.id))

    if job is None:
        add_job_if_applicable(db_job, scheduler)
        db_job.activate = StatusEnum.ACTIAVTE
        db.add(db_job)
        db_history = Schedule_History(act=StatusEnum.ACTIAVTE,
                                      act_date=datetime.now(),
                                      user_id=None,
                                      job_id=db_job.id,
                                      job=db_job)
        db.add(db_history)
        db.commit()
    else:
        if job.next_run_time is None:
            resume_scheduled_job(db_job, scheduler)
            db_job.activate=StatusEnum.ACTIAVTE
            db.add(db_job)
            db_history = Schedule_History(act=StatusEnum.ACTIAVTE,
                                          act_date=datetime.now(),
                                          user_id=None,
                                          job_id=db_job.id,
                                          job=db_job)
            db.add(db_history)
            db.commit()
        else:
            print("이미 활성화중입니다")


@router.post("/{job_id}/deactivate")
def deactivate_job(job_id: int,
                       db: Session = Depends(get_db)):
    db_job: Job = job_crud.get_job(job_id, db)
    if not db_job:
        raise HTTPException(status_code=404, detail="id-not-exist")

    job = scheduler.get_job(str(db_job.id))

    if job.next_run_time is not None:
        pause_scheduled_job(db_job, scheduler)
        # log 남기기
        db_job.activate = StatusEnum.STOP
        db.add(db_job)
        db_history = Schedule_History(act=StatusEnum.STOP,
                                      act_date=datetime.now(),
                                      user_id=None,
                                      job_id=db_job.id,
                                      job=db_job)
        db.add(db_history)
        db.commit()
    else:
        print("이미 비활성화중입니다")


@router.post("/{job_id}/run")
def run_job(job_id: int,
            db: Session = Depends(get_db)):
    db_job: Job = job_crud.get_job(job_id, db)
    if not db_job:
        raise HTTPException(status_code=404, detail="id-not-exist")

    job = scheduler.get_job(str(db_job.id))

    if job is None:
        print("등록먼저 해야됨")
    else:
        if job.next_run_time is None:
            print("활성화 해야함")
        else:
            execute_job(db_job)


@router.on_event("startup")
async def start_scheduler():
    scheduler.start()


@router.on_event("startup")
async def reboot_scheduler():
    db: Session = SessionLocal()
    try:
        total, activate_job_list = job_crud.get_activate_job_list(db)
        for activate_job in activate_job_list:
            print(f'reboot_scheduler_id: {activate_job.id}')
            add_job_if_applicable(activate_job, scheduler)
    finally:
        db.close()
