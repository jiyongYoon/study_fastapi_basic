from apscheduler.triggers.cron import CronTrigger
import subprocess
from datetime import datetime

scheduled_jobs_map = {}


def get_scheduled_job(scheduler):
    jobs = scheduler.get_jobs()
    job_ids = []
    for job in jobs:
        job_json = dict()
        job_json['id'] = job.id
        job_ids.append(job_json)
    return job_ids


def add_job_if_applicable(job, scheduler):
    job_id = str(job.id)

    import copy

    if (job_id not in scheduled_jobs_map):
        scheduled_jobs_map[job_id] = job
        copy_job = copy.deepcopy(job)
        scheduler.add_job(lambda: execute_job(copy_job), CronTrigger.from_crontab(job.cron_expression, timezone='UTC'),
                          id=job_id)
        print("added job with id: " + str(job_id))
        return job
    else:
        return "job_id is already register"


def pause_scheduled_job(job, scheduler):
    print("pause job with id : " + str(job.id))
    scheduler.pause_job(str(job.id))


def resume_scheduled_job(job, scheduler):
    print("resume job with id : " + str(job.id))
    scheduler.resume_job(str(job.id))


def execute_job(job):
    print("executing job with id: " + str(job.id))
    print(datetime.utcnow())
    shell_path = job.script_file
    subprocess.call([shell_path])