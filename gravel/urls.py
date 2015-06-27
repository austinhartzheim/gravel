from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # API URLs - first for faster access
    url(r'^api/', include('api.urls')),

    # Main URLs
    url(r'^problem/', include('problems.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Home URLs
    url(r'^$', 'home.views.home'),
    url(r'^account/$', include('account.urls')),
]
