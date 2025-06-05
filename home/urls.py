from django.urls import path
from .views import IngestAPIView, StatusAPIView,home_view

urlpatterns = [
    path("ingest", IngestAPIView.as_view(), name="ingest"),
    path("status/<uuid:ingestion_id>", StatusAPIView.as_view(), name="status"),
    path("",home_view,name="home"),
]
