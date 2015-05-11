from django.contrib import admin
from holiday.models import Person, Application, Reward, ApplicationRollback
# Register your models here.


'''
在django的admin界面注册每个数据模型的显示、搜索和过滤。看django book上还可以注册处理的函数，暂时还没有实现
'''
class PersonAdmin(admin.ModelAdmin):
    list_display = ('chinese_name', 'groupname', 'holidayNum', 'holidayNumSum', 'holidayNumUsed')
    search_fields = ('chinese_name', 'groupname')
    list_filter = ('groupname', )

class RewardAdmin(admin.ModelAdmin):
    list_display = ('apply_reward', 'reward_reward', 'type', 'days_apply', 'days_approve', 'date_apply')
    search_fields = ('apply_reward__chinese_name', 'reward_reward__chinese_name',)
    list_filter = ('date_apply', 'type', 'apply_reward__groupname')

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('apply_application', 'date_start', 'date_end', 'days_apply', 'days_approve', 'date_apply')
    search_fields = ('apply_application__chinese_name', )
    list_filter = ('date_apply', 'apply_application__groupname')

class RollbackAdmin(admin.ModelAdmin):
    list_display = ('apply_rollback', 'days_apply', 'days_approve', 'date_apply')
    search_fields = ('apply_rollback__chinese_name', )
    list_filter = ('date_apply', 'apply_rollback__groupname')


admin.site.register(Person, PersonAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Reward, RewardAdmin)
admin.site.register(ApplicationRollback, RollbackAdmin)