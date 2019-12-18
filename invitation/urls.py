from invitation import views
from django.conf.urls import url, include


urlpatterns = [
    url(r'^$', views.ApiHome.as_view()),
    url(r'^invitations/$', views.InvitationList.as_view()),
    url(r'^invitations/(?P<id>.+)/$', views.InvitationDetails.as_view()),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]
