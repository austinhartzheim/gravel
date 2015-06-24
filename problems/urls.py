from django.conf.urls import patterns, url

urlpatterns = patterns('problems.views',
    url(r'report/$', 'problem_report'),
    url(r'report/submit$', 'problem_submit'),
    url(r'view/(?P<pk>\d+)/$', 'problem_view'),
    url(r'reply/(?P<pk>\d+)/submit$', 'problem_reply_submit'),
    url(r'tag/(?P<tag>[^/]+)/view', 'tag_view')
)