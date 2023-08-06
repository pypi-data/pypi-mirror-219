from django.urls import path

from django_aps.views.apscheduler_view import RegisteredFuncQueryView, SchedulerJobAddView, SchedulerJobQueryView, \
    SchedulerJobUpdateView, SchedulerJobPauseView, SchedulerJobResumeView, SchedulerJobRemoveView

urlpatterns = [
    path(r'func/query', RegisteredFuncQueryView.as_view()),
    path(r'scheduler-job/query', SchedulerJobQueryView.as_view()),
    path(r'scheduler-job/add', SchedulerJobAddView.as_view()),
    path(r'scheduler-job/update', SchedulerJobUpdateView.as_view()),
    path(r'scheduler-job/pause', SchedulerJobPauseView.as_view()),
    path(r'scheduler-job/resume', SchedulerJobResumeView.as_view()),
    path(r'scheduler-job/remove', SchedulerJobRemoveView.as_view()),
]
