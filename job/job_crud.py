from models import *
from sqlalchemy.orm import Session



def get_job_list(db: Session):
    _job_list = db.query(Job).order_by(Job.id).all()
    return _job_list


def get_activate_job_list(db: Session):
    _activating_job_list = (db.query(Job)
                            .filter(Job.activate == StatusEnum.ACTIAVTE)
                            .order_by(Job.id).all())
    return _activating_job_list

def get_job(job_id: int, db: Session):
    return db.query(Job).get(job_id)