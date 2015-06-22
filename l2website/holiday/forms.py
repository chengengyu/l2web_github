from django import forms
from holiday.models import Application, Person, Reward, ApplicationRollback
from django.forms import ModelForm
from django.forms.widgets import TextInput, NumberInput, DateInput, Select, RadioSelect, Textarea, CheckboxInput, SplitDateTimeWidget
from django.forms.extras.widgets import SelectDateWidget
from l2website.settings import reward_reason_choices
from django.forms.models import modelformset_factory

'''
继承module的三个form，在提交申请的三个界面使用

'''
class RewardForm(ModelForm):
    #定义除了继承外的其他字段
    applyname = forms.CharField()
    person = Person()
    #设置继承的module以及其中的字段
    class Meta:
        model = Reward
        fields = ('type', 'reason', 'days_apply')
        #定义显示的widget
        widgets = {
            'days_apply': TextInput(attrs={'type': 'number','step':'0.5', 'value':0, 'min':'0'}),
             'type': Select(choices=reward_reason_choices),
        }
    '''
    在clean 数据时，django会调用自定义的函数进行数据正确性检查
    '''
    def clean_applyname(self):
        try:
            self.cleaned_data['person'] = Person.objects.get(name=self.cleaned_data['applyname'])    
        except Person.DoesNotExist:
            raise forms.ValidationError("查不到该同事")
        return self.cleaned_data['applyname']
    
    def clean_days_apply(self):
        if (self.cleaned_data['days_apply'] <= 0) or (float(self.cleaned_data['days_apply']) % (0.5) != 0.0):
            raise forms.ValidationError("申请最小单位0.5天")
        return self.cleaned_data['days_apply']


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('holidayNum', 'holidayNumSum', 'holidayNumUsed')
        widgets = {'holidayNum': NumberInput(attrs={'name': '现有倒休'}),
                   'holidayNumSum': NumberInput(attrs={'name': '历史倒休和'}),
                   'holidayNumUsed': NumberInput(attrs={'name': '已使用的倒休'})
        }


class ApplicationForm(ModelForm):
    holidayNum = forms.NumberInput()
    class Meta:
        model = Application
        fields = ('reason', 'days_apply', 'date_start', 'date_end', 'start_meridiem', 'end_meridiem')
        widgets = {
            'days_apply': TextInput(attrs={'type': 'number','step':'0.5', 'value':0, 'min':'0'}),
            #'date_start': SelectDateWidget(attrs={'format': '%m/%d/%Y'}),
            'date_start': SelectDateWidget(),
            'date_end': SelectDateWidget(),
            'start_meridiem': Select(choices=(('上午', '上午'),('下午', '下午'))),
            'end_meridiem': Select(choices=(('下午', '下午'), ('上午', '上午'))),
        }

    def clean_days_apply(self):
        # 这里访问 holidaynum的时候并没有使用cleandata的形式，不知道是调用clean函数的顺序的问题还是其他原因，会提示字典中没有此关键字
        if self.cleaned_data['days_apply'] > self.holidayNum:
            raise forms.ValidationError("您没有那么多倒休")
        if ((self.cleaned_data['days_apply'] <= 0) or (float(self.cleaned_data['days_apply']) % (0.5) != 0.0)):
            raise forms.ValidationError("申请最小单位0.5天")
        return self.cleaned_data['days_apply']
    
    
class RollbackForm(ModelForm):        
    class Meta:
        model = ApplicationRollback
        fields = ('reason', 'days_apply')
        widgets = {
            'days_apply': TextInput(attrs={'type': 'number','step':'0.5', 'value':0, 'min':'0'}),
        }
    def clean_days_apply(self):
        if (self.cleaned_data['days_apply'] <= 0) or (float(self.cleaned_data['days_apply']) % (0.5) != 0.0):
            raise forms.ValidationError("申请最小单位0.5天")
        return self.cleaned_data['days_apply']

'''
倒休申请的formset，暂时未使用，目前添加在生成审批的界面函数中
'''

def RewardFormSet():
    return modelformset_factory(Reward, extra=0,
                                widgets={'apply_reward': TextInput(attrs={'readonly': "readonly"}),
                                         'reward_reward': TextInput(attrs={'readonly': "readonly"}),
                                         'approve_reward': TextInput(attrs={'readonly' : "readonly"}),
                                         #'date_apply': DateInput(attrs={'name': '申请日期'}),
                                         #'type': TextInput(attrs={'name': '倒休原因'}),
                                         #'reason': Textarea(attrs={'name': '备注'}),
                                         #'days_apply': NumberInput(attrs={'name': '倒休时长'}),
                                         #'days_approve': NumberInput(attrs={'name': '审批结果'}),
                                         #'approve_flag': CheckboxInput(attrs={'name': '是否审批过'}),
                                         }
                                )
