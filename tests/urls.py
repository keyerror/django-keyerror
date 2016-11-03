from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^success$', views.success,
        name='success'),
    url(r'^not-found$', views.not_found,
        name='not-found'),
    url(r'^error$', views.error,
        name='error'),
    url(r'^error-grouped$', views.error_grouped,
        name='error-grouped'),
)
