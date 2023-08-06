# """
# apscheduler job model mapper
# """
# from django.db import DatabaseError
#
# from django_aps.models import ApschedulerJobInfo
#
#
# def add_apscheduler_job_info(job_info: dict):
#     try:
#         obj = ApschedulerJobInfo.objects.create(
#             **job_info
#         )
#         return obj.id
#     except DatabaseError:
#         raise
#
#
# def update_apscheduler_job_info(job_info_id: int, job_info: dict):
#     ApschedulerJobInfo.objects.filter(
#         id=job_info_id,
#         is_deleted='N'
#     ).update(**job_info)
