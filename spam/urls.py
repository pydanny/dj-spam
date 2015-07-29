from django.conf.urls import url
from . import views

urlpatterns = (
    url(
        regex=r'^$',
        view=views.ThankYouView.as_view(),
        name='thanks'
    ),
    url(
        r'^(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<pk>\d+)/$',
        view=views.ReportSpamCreateView.as_view(),
        name='report'
    ),
)
