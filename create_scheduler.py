from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from utils.config_reader import config

jobstores = {
    'default': SQLAlchemyJobStore(url=f'sqlite:///{config.job_database_file}')
}
executors = {
    'default': AsyncIOExecutor()
}
job_defauts = {
    'coalesce': False,
    'max_instances': 1
}

scheduler = AsyncIOScheduler(
    jobstores = jobstores,
    executors = executors,
    job_defauts = job_defauts,
    timezone = 'Europe/Moscow'
)