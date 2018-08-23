from django.conf.urls import url

from users.views import register,detail,EditUserView

app_name = 'users'
urlpatterns = [
    url(r'^register/$', register, name='register'),
    # url(r'^detail/$', detail, name='register'),
    url(r'^edit_user/(?P<pk>\d+)/$', EditUserView.as_view(), name='edit_user'),
]
