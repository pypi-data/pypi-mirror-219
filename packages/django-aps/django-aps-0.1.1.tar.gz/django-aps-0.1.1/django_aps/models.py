from django.db import models


# Create your models here.


class BaseModel(models.Model):
    class Meta:
        abstract = True
        db_table = 'base_model'
        verbose_name = '基础表'

    id = models.AutoField(primary_key=True)
    is_deleted = models.CharField(max_length=2, default='N', verbose_name='是否逻辑删除', help_text='是否逻辑删除')
    creator = models.CharField(max_length=32, null=True, blank=True, verbose_name='创建人', help_text='创建人')
    modifier = models.CharField(max_length=32, null=True, blank=True, verbose_name='更新人', help_text='更新人')
    gmt_created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    gmt_modified = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')


class ApschedulerFunc(models.Model):
    class Meta:
        db_table = 'django_apscheduler_func'
        verbose_name = '定时任务方法汇总表'
        verbose_name_plural = verbose_name

    func_module = models.CharField(max_length=256, verbose_name='函数、方法所属模块')
    func_name = models.CharField(max_length=128, verbose_name='函数、方法名')
    func_args = models.CharField(max_length=128, verbose_name='函数、方法参数')
    func_doc = models.CharField(max_length=256, null=True, verbose_name='描述信息')

# class ApschedulerJobInfo(BaseModel):
#     class Meta:
#         db_table = 'django_apscheduler_job_info'
#         verbose_name = '定时任务配置表'
#         verbose_name_plural = verbose_name
#
#     name = models.CharField(max_length=128, unique=True, db_index=True, verbose_name='定时任务名称')
#     job_id = models.CharField(max_length=128, db_index=True, null=True, blank=True, verbose_name='定时任务执行id')
#     func_ref = models.CharField(max_length=256, verbose_name='函数、方法所属模块')
#     func_name = models.CharField(max_length=128, verbose_name='函数、方法名')
#     func_args = models.CharField(max_length=128, verbose_name='函数、方法参数')
#     func_kwargs = models.CharField(max_length=256, verbose_name='函数、方法关键字参数')
#     trigger_type = models.CharField(max_length=64, verbose_name='触发器类型')
#     trigger_params = models.JSONField(null=True, blank=True, verbose_name='触发器参数')
#     job_status = models.CharField(max_length=64, null=True, blank=True, verbose_name='任务状态')
#     description = models.CharField(max_length=256, null=True, blank=True, verbose_name='描述信息')
