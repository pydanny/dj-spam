from django.conf.urls import url, include

from test_app.views import DataDetailView

urlpatterns = [
    url(r'^spam/', include('spam.urls', namespace='spam')),
    url(
        regex="^(?P<pk>\d+)/$",
        view=DataDetailView.as_view(),
        name="data",
    ),

]
