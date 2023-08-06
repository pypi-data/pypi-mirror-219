"""
APScheduler serializers
"""
from rest_framework import serializers

__all__ = [
    'RegisteredFuncQuerySerializers',
    'SchedulerJobAddSerializers',
    'SchedulerJobQuerySerializers',
    'SchedulerJobUpdateSerializers',
    'SchedulerJobPauseSerializers'
]


class RegisteredFuncQuerySerializers(serializers.Serializer):  # noqa
    func_name = serializers.CharField(max_length=256, required=False, help_text='定时任务方法名')


class TriggerParamsSerializers(serializers.Serializer):  # noqa
    start_date = serializers.CharField(help_text='开始执行时间', required=False)
    end_date = serializers.CharField(help_text='结束执行时间', required=False)
    year = serializers.CharField(help_text='年', required=False)
    month = serializers.CharField(help_text='月', required=False)
    week = serializers.CharField(help_text='周', required=False)
    day = serializers.CharField(help_text='日', required=False)
    day_of_week = serializers.CharField(help_text='周', required=False)
    hour = serializers.CharField(help_text='小时', required=False)
    minute = serializers.CharField(help_text='分钟', required=False)
    second = serializers.CharField(help_text='秒', required=False)
    timezone = serializers.CharField(help_text='时区', required=False)
    jitter = serializers.IntegerField(help_text='抖动时间', required=False)

    def validate(self, attrs):
        day_of_week = attrs.get('day_of_week')
        day = attrs.get('day')
        if day_of_week and day:
            raise serializers.ValidationError('Both "day" and "day_of_week" cannot be selected')
        return attrs


class TriggerSerializers(serializers.Serializer):  # noqa
    trigger_type = serializers.CharField(max_length=64, required=False, default='cron', help_text='触发器类型')
    trigger_params = TriggerParamsSerializers(help_text='触发器参数')


class SchedulerJobAddSerializers(serializers.Serializer):  # noqa
    name = serializers.CharField(max_length=256, help_text='定时任务名称')
    func_module = serializers.CharField(max_length=256, help_text='方法所属模块')
    func_name = serializers.CharField(max_length=256, help_text='方法名')
    func_args = serializers.ListField(required=False, default=None, help_text='方法参数')
    func_kwargs = serializers.DictField(required=False, default=None, help_text='方法关键字参数')
    trigger = TriggerSerializers(help_text='触发器')


class SchedulerJobQuerySerializers(serializers.Serializer):  # noqa
    job_id = serializers.CharField(max_length=256, required=False, help_text='定时任务id')


class SchedulerJobUpdateSerializers(serializers.Serializer):  # noqa
    job_id = serializers.CharField(max_length=256, help_text='定时任务id')
    name = serializers.CharField(max_length=256, help_text='定时任务名称')
    # func_module = serializers.CharField(max_length=256, help_text='方法所属模块')
    # func_name = serializers.CharField(max_length=256, help_text='方法名')
    func_args = serializers.ListField(required=False, default=None, help_text='方法参数')
    func_kwargs = serializers.DictField(required=False, default=None, help_text='方法关键字参数')
    trigger = TriggerSerializers(help_text='触发器')


class SchedulerJobPauseSerializers(serializers.Serializer):  # noqa
    job_id = serializers.CharField(max_length=256, help_text='定时任务id')
