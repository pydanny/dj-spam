from django.conf.urls import url
from . import views

urlpatterns = (
    url(
        regex=r'^$',
        view=views.ReportSpamListView.as_view(),
        name='list'
    ),
    url(
        r'^(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<pk>\d+)/$',
        view=views.ReportSpamCreateView.as_view(),
        name='report'
    ),
)
