from models import *
from sqlalchemy.orm import Session



def get_job_list(db: Session, skip: int = 0, limit: int = 10):
    _job_list = db.query(Job).order_by(Job.id)

    total = _job_list.count()
    job_list = _job_list.offset(skip).limit(limit).all()
    return total, job_list # (전체 건수, 페이징 리스트)


def get_activate_job_list(db: Session, skip: int = 0, limit: int = 10):
    _activating_job_list = db.query(Job)\
                            .filter(Job.activate == StatusEnum.ACTIAVTE)\
                            .order_by(Job.id)
    total = _activating_job_list.count()
    activating_job_list = _activating_job_list.offset(skip).limit(limit).all()
    return total, activating_job_list

def get_job(job_id: int, db: Session):
    return db.query(Job).get(job_id)