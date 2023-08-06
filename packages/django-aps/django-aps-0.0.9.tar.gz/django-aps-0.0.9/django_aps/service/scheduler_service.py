"""
APScheduler Service
"""
import logging
from typing import Union

from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.module_loading import import_string

from django_aps.model.aps_models import APSchedulerJob
from django_aps.model.trigger_models import CronTriggerModel, IntervalTriggerModel, DateTriggerModel
from django_aps.settings import aps_settings

logger = logging.getLogger(__name__)


class APSchedulerService:

    def __init__(self):
        self._scheduler_options = None
        # self._scheduler = None
        self._trigger_model = {
            'cron': CronTriggerModel,
            'interval': IntervalTriggerModel,
            'date': DateTriggerModel
        }
        self._start()

    def _start(self):
        scheduler_options = self._init_scheduler_options()
        self._scheduler = BackgroundScheduler(**scheduler_options)
        try:
            self._scheduler.start()
            logger.info('APScheduler has started')
        except Exception as e:
            logger.error(e, exc_info=True)
            self._scheduler.shutdown()

    def _init_scheduler_options(self):
        job_stores_cls = import_string(aps_settings.DEFAULT_JOB_STORES)
        jobstores = {
            'default': job_stores_cls()
        }
        default_executors = aps_settings.DEFAULT_EXECUTORS
        executors_cls = import_string(default_executors.get('executor'))
        executor = {
            'default': executors_cls(default_executors.get('max_pool_size'))
        }
        job_defaults = aps_settings.DEFAULT_JOB_DEFAULTS
        timezone = aps_settings.DEFAULT_TIMEZONE
        self._scheduler_options = {
            'jobstores': jobstores,
            'executor': executor,
            'job_defaults': job_defaults,
            'timezone': timezone
        }

        return self._scheduler_options

    def add_scheduler_job(self, name: str, func_module: str, func_name: str, func_args: list = None,
                          func_kwargs: dict = None, trigger: dict = None) -> int:
        """
        新增定时任务

        """
        func_ref = func_module + ':' + func_name
        trigger_params = trigger.get('trigger_params')
        trigger_type = str(trigger.get('trigger_type')).lower()
        trigger_params = self._trigger_params_formatting(trigger_type, trigger_params)
        job = self._scheduler.add_job(name=name, func=func_ref, args=func_args, kwargs=func_kwargs,
                                      trigger=trigger_type,
                                      **trigger_params)
        # job_info = {
        #     'name': name,
        #     'func_ref': func_ref,
        #     'func_name': func_name,
        #     'func_args': func_args,
        #     'func_kwargs': func_kwargs,
        #     'trigger_type': trigger_type,
        #     'trigger_params': trigger_params,
        #     'description': description,
        #     'job_status': JobStatus.PENDING.value,
        #     'job_id': job.id
        # }
        # job_info_id = apscheduler_job_model_mapper.add_apscheduler_job_info(job_info)

        return job.id

    def get_scheduler_job(self, job_id: str = None, job_store: str = None):
        """
        Returns the Job that matches the given ``job_id``. Returns all job if ``job_id`` is None

        :param str job_id: the identifier of the job
        :param str job_store: alias of the job store that most likely contains the job
        :return: the Job by the given ID, or ``None`` if it wasn't found, or all Job if ``job_id`` is None
        :rtype: dict | list[dict]

        """
        if job_id:
            job = self._scheduler.get_job(job_id, jobstore=job_store)
            return self._parse_job_detail_to_dict(job)

        return self.get_scheduler_jobs(job_store)

    def get_scheduler_jobs(self, job_store: str = None) -> list:
        """
        Returns a list of pending jobs

        :param str job_store: alias of the job store
        :rtype: list[dict]
        """
        parsed_jobs = []
        jobs = self._scheduler.get_jobs(jobstore=job_store)
        for job in jobs:
            parsed_jobs.append(self._parse_job_detail_to_dict(job))

        return jobs

    @staticmethod
    def _parse_job_detail_to_dict(job: Job) -> dict:
        job_model = APSchedulerJob(
            id=job.id,
            name=job.name,
            func_ref=job.func_ref,
            trigger=job.trigger,
            func_args=job.args,
            func_kwargs=job.kwargs,
            next_run_time=job.next_run_time
        )

        return job_model.model_dump()

    def remove_scheduler_job(self, job_id: str, job_store: str = None):
        """
        Removes a job, preventing it from being run anymore.

        :param str job_id: the identifier of the job
        :param str job_store: alias of the job store that contains the job
        :raises JobLookupError: if the job was not found

        """
        if job_id:
            self._scheduler.remove_job(job_id, jobstore=job_store)
        else:
            self.remove_all_scheduler_jobs(job_store)

    def remove_all_scheduler_jobs(self, job_store: str = None):
        """
        Removes all jobs from the specified job store, or all job stores if none is given.

        :param str job_store: alias of the job store

        """
        self._scheduler.remove_all_jobs(jobstore=job_store)

    def pause_scheduler_job(self, job_id: str, job_store: str = None):
        """
        Causes the given job not to be executed until it is explicitly resumed.

        :param str job_id: the identifier of the job
        :param str job_store: alias of the job store that contains the job
        :return the relevant job detail
        :rtype: dict
        """
        job = self._scheduler.pause_job(job_id, jobstore=job_store)

        return self._parse_job_detail_to_dict(job)

    def resume_scheduler_job(self, job_id: str, job_store: str = None) -> Union[dict, None]:
        """
        Resumes the schedule of the given job, or removes the job if its schedule is finished.

        :param str job_id: the identifier of the job
        :param str job_store: alias of the job store that contains the job
        :return the relevant job instance if the job was rescheduled, or ``None`` if no
            next run time could be calculated and the job was removed

        """
        job = self._scheduler.resume_job(job_id, jobstore=job_store)
        if job is None:
            return None

        return self._parse_job_detail_to_dict(job)

    def update_scheduler_job(self, job_id: str, job_store: str = None, name: str = None,
                             func_args: Union[list, tuple] = None,
                             func_kwargs: dict = None, trigger: dict = None) -> dict:
        """
        Update APScheduler job

        :param str job_id: the identifier of the job
        :param str job_store: alias of the job store that contains the job
        :param str name: textual description of the job
        :param list|tuple func_args: list of positional arguments to call func with
        :param dict func_kwargs: dict of keyword arguments to call func with
        :param dict trigger: trigger that determines when ``func`` is called
        :rtype: dict
        """
        trigger_params = trigger.get('trigger_params')
        trigger_type = str(trigger.get('trigger_type')).lower()
        trigger_params = self._trigger_params_formatting(trigger_type, trigger_params)

        self._scheduler.reschedule_job(job_id=job_id, jobstore=job_store, trigger=trigger_type,
                                       **trigger_params)
        job = self._scheduler.modify_job(
            job_id=job_id,
            jobstore=job_store,
            name=name,
            args=func_args,
            kwargs=func_kwargs
        )

        return self._parse_job_detail_to_dict(job)

    def _trigger_params_formatting(self, trigger_type: str, trigger_params: dict) -> dict:
        trigger_cls = self._trigger_model.get(trigger_type)

        return trigger_cls(**trigger_params).model_dump()
