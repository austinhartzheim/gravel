from django.conf.urls import patterns, url

urlpatterns = patterns('api.views',

    # Normal API commands
    url(r'get_tokens$', 'api_get_tokens'),

    # Problem commands
    url(r'problem/highest_id$', 'problem_highest_id'),
    url(r'problem/replies/submit$', 'problem_reply'),
    url(r'problem/replies/get$', 'problem_get_replies'),

    # Tag commands
    url(r'tag/get', 'tag_get'),
    url(r'tag/problems', 'tag_problems'),
    url(r'tag/all', 'tag_all'),
)
