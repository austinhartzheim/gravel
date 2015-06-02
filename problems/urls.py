from django.conf.urls import patterns, url

urlpatterns = patterns('problems.views',
    url(r'report/$', 'problem_report'),
    url(r'report/submit$', 'problem_submit'),
    url(r'view/(?P<pk>\d+)/', 'problem_view'),
)