from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

import views

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^$', views.UserView.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name='detail'),
    url(r'^confirm/$', views.UserConfirmView.as_view(), name='confirm'),
    url(r'^sign-in/$', views.UserSignInView.as_view(), name='sign-in'),
    url(r'^change-password/$', views.UserChangePasswordView.as_view(),
        name='change-password'),
])
