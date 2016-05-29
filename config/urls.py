from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'jobs.views.home', name='home'),
    url(r'^', include('jobs.apps.users.urls', namespace='users')),

    url(r'^admin/', include(admin.site.urls)),
]
