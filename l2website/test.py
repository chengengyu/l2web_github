#
from django_excel_templates import *
from django_excel_templates.color_converter import *
from models import *
from django.http import HttpResponse


'''
保存了一些看到的模板函数
'''
def xls_simple(request):

    ## Simple ##
    testobj = Book.objects.all()

    formatter = ExcelFormatter()
    simpleStyle = ExcelStyle(vert=2,wrap=1)
    formatter.addBodyStyle(simpleStyle)
    formatter.setWidth('name,category,publish_date,bought_on',3000)
    formatter.setWidth('price',600)
    formatter.setWidth('ebook',1200)
    formatter.setWidth('about',20000)

    simple_report = ExcelReport()
    simple_report.addSheet("TestSimple")
    filter = ExcelFilter(order='name,category,publish_date,about,bought_on,price,ebook')
    simple_report.addQuerySet(testobj,REPORT_HORZ,formatter, filter)

    response = HttpResponse(simple_report.writeReport(),mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=simple_test.xls'
    return response