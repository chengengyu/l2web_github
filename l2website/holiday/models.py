from django.db import models

# Create your models here.

'''
记录每个人的数据库，这里在代码中并没有和登陆时的用户名进行绑定，但是在使用上是和name进行绑定处理
此处数据库中的数字设置为10进制实数，允许3位小数点前，1位小数点后，主要是为了满足申请半天倒休的需求
'''    
class Person(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="用户名")
    chinese_name = models.CharField(max_length=30, verbose_name="中文姓名")
    email = models.EmailField(verbose_name="邮箱")
    holidayNum = models.DecimalField(max_digits=4, decimal_places=1,default=0, verbose_name="现有倒休")
    holidayNumSum = models.DecimalField(max_digits=4, decimal_places=1,default=0, verbose_name="倒休之和")
    holidayNumUsed = models.DecimalField(max_digits=4, decimal_places=1,default=0, verbose_name="已用倒休")
    groupname = models.CharField(max_length=30, verbose_name="资源组")
    class Meta:
        permissions = (
            ("apply_reward", "申请倒休的权利"),
            ("apply_application", "申请使用倒休的权利"),
            ("approve", "审批的权利"),
        )
        
    def __str__(self):
        return u'%s' % self.chinese_name
'''
记录使用倒休的数据库，
依次为：原因，申请天数，批准天数，申请使用的起始日期，申请使用的结束日期，申请人，审批人
'''    
class Application(models.Model):
    reason = models.TextField(max_length=100, verbose_name="申请原因")
    days_apply =  models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name="申请天数")
    days_approve = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name="批准天数")
    date_apply = models.DateField(auto_now_add=True, verbose_name="申请日期")
    date_approve = models.DateField(blank=True, verbose_name="审批日期")
    date_start = models.DateField(verbose_name="开始日期")
    start_meridiem = models.CharField(max_length=30, verbose_name="开始时间")
    date_end = models.DateField(verbose_name="结束日期")
    end_meridiem = models.CharField(max_length=30, verbose_name="结束时间")
    apply_application = models.ForeignKey(Person, related_name='apply_application', verbose_name="申请人")
    approve_application = models.ForeignKey(Person, blank=True, related_name='approve_application', verbose_name="审批人")
    approve_flag = models.BooleanField(default=False, verbose_name="审批通过")
    
    def __str__(self):
        return u'%s' % self.apply_application.name
'''
记录申请倒休的数据库，
依次为：申请类别，原因，申请天数，批准天数，申请人，奖励人，审批人
'''
class Reward(models.Model):
    type = models.CharField(max_length=30, verbose_name="倒休原因")
    reason = models.TextField(max_length=100, verbose_name="备注")
    days_apply =  models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name="申请天数")
    days_approve = models.DecimalField(max_digits=4, decimal_places=1,default=0, verbose_name="批准天数")
    date_apply = models.DateField(auto_now_add=True, verbose_name="申请日期")
    date_approve = models.DateField(blank=True, null=True, verbose_name="审批日期")
    apply_reward = models.ForeignKey(Person, related_name='apply_reward', verbose_name="申请人")
    reward_reward = models.ForeignKey(Person, related_name='reward_reward', verbose_name="倒休人")
    approve_reward = models.ForeignKey(Person, blank=True, related_name='approve_reward', verbose_name="审批人")
    approve_flag = models.BooleanField(default=False, verbose_name="审批通过")
    
    def __str__(self):
        return u'%s' % self.apply_reward.name

'''
有一些申请需要取消，添加一个新的表记录取消的申请
依次为：申请原因，申请天数，申请人，审批人
'''

class ApplicationRollback(models.Model):
    reason = models.TextField(max_length=100, verbose_name="取消原因")
    apply_rollback = models.ForeignKey(Person, related_name='apply_rollback', verbose_name="申请人")
    days_apply =  models.DecimalField(max_digits=4, decimal_places=1,default=0, verbose_name="申请天数")
    days_approve = models.DecimalField(max_digits=4, decimal_places=1,default=0, verbose_name="批准天数")
    approve_rollback = models.ForeignKey(Person, blank=True, related_name='approve_rollback', verbose_name="审批人")
    date_apply = models.DateField(auto_now_add=True, verbose_name="申请日期")
    date_approve = models.DateField(blank=True, verbose_name="审批日期")
    approve_flag = models.BooleanField(default=False, verbose_name="审批通过")
    
    def __str__(self):
        return u'%s' % self.apply_rollback.name
