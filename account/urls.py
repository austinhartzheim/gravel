from django.conf.urls import patterns, url

urlpatterns = patterns('account.views',
    url(r'^login/$', 'login'),
)