from django.conf.urls import patterns, url

urlpatterns = patterns('api.views',

    # Normal API commands
    url(r'get_tokens$', 'api_get_tokens'),

    # Problem commands
    url(r'problem/highest_id$', 'problem_highest_id'),
)