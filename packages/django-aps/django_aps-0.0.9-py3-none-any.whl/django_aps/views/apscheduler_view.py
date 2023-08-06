"""
Apscheduler functions view
"""
from django.http import JsonResponse

from django_aps.base import BaseGenericAPIView
from django_aps.serializers.apscheduler_serializers import RegisteredFuncQuerySerializers, SchedulerJobAddSerializers, \
    SchedulerJobQuerySerializers, SchedulerJobUpdateSerializers, SchedulerJobPauseSerializers
from django_aps.service.discover_service import DiscoverService
from django_aps.service.scheduler_service import APSchedulerService


class RegisteredFuncQueryView(BaseGenericAPIView):
    serializer_class = RegisteredFuncQuerySerializers

    def get(self, request):
        serializer = self.serializer_class(data=request.query_params)
        self.check_validate(serializer)
        data = serializer.validated_data
        aps_funcs = DiscoverService().get_apscheduler_funcs(data.get('name'))

        return JsonResponse(
            data={
                'success': True,
                'code': 1,
                'data': aps_funcs
            }
        )


class SchedulerJobAddView(BaseGenericAPIView):
    serializer_class = SchedulerJobAddSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        self.check_validate(serializer)
        data = serializer.validated_data
        job_info_id = APSchedulerService().add_scheduler_job(**data)

        return JsonResponse(
            data={
                'success': True,
                'code': 1,
                'data': {
                    'job_info_id': job_info_id
                }
            }
        )


class SchedulerJobQueryView(BaseGenericAPIView):
    serializer_class = SchedulerJobQuerySerializers

    def get(self, request):
        serializer = self.serializer_class(data=request.query_params)
        self.check_validate(serializer)
        data = serializer.validated_data
        job_info = APSchedulerService().get_scheduler_job(job_id=data.get('job_id'))

        return JsonResponse(
            data={
                'success': True,
                'code': 1,
                'data': job_info
            }
        )


class SchedulerJobUpdateView(BaseGenericAPIView):
    serializer_class = SchedulerJobUpdateSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        self.check_validate(serializer)
        data = serializer.validated_data
        job_info = APSchedulerService().update_scheduler_job(**data)

        return JsonResponse(
            data={
                'success': True,
                'code': 1,
                'data': job_info
            }
        )


class SchedulerJobPauseView(BaseGenericAPIView):
    serializer_class = SchedulerJobPauseSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        self.check_validate(serializer)
        data = serializer.validated_data
        job_info = APSchedulerService().pause_scheduler_job(data.get('job_id'))

        return JsonResponse(
            data={
                'success': True,
                'code': 1,
                'data': job_info
            }
        )


class SchedulerJobResumeView(BaseGenericAPIView):
    serializer_class = SchedulerJobPauseSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        self.check_validate(serializer)
        data = serializer.validated_data
        job_info = APSchedulerService().resume_scheduler_job(data.get('job_id'))

        return JsonResponse(
            data={
                'success': True,
                'code': 1,
                'data': job_info
            }
        )


class SchedulerJobRemoveView(BaseGenericAPIView):
    serializer_class = SchedulerJobQuerySerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        self.check_validate(serializer)
        data = serializer.validated_data
        APSchedulerService().remove_scheduler_job(data.get('job_id'))

        return JsonResponse(
            data={
                'success': True,
                'code': 1,
                'data': None
            }
        )
