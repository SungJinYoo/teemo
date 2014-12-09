from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic.base import TemplateView
from teemo.views import LoginView, LogoutView, AddStudentView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'teemo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', TemplateView.as_view(template_name='time_table.html'), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^student/$', AddStudentView.as_view(), name='add_student'),
    url(r'^time_table/', include('time_table.urls', namespace='time_table')),
    url(r'^help/$', TemplateView.as_view(template_name='help.html'), name='help'),
    url(r'^admin/', include(admin.site.urls)),
)
