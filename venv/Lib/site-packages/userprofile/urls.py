from django.conf.urls import patterns, url

from .views import Home, Login, Logout, RequireEmail
from .views import ProfileView

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^require-email/$', RequireEmail.as_view(), name='require_email'),
)

urlpatterns += patterns(
    '',
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^profile/(?P<pk>\d+)/$', ProfileView.as_view(), name='profile-view'),
)
