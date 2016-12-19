from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

import views

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^users/$',
        views.UserView.as_view(),
        name='user-list'),
    url(r'^users/confirm/$',
        views.UserConfirmView.as_view(),
        name='user-confirm')
])
