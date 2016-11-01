from django.conf.urls import url

import test_views

urlpatterns = (
    url(r'^success$', test_views.success,
        name='success'),
    url(r'^not-found$', test_views.not_found,
        name='not-found'),
    url(r'^error$', test_views.error,
        name='error'),
)
