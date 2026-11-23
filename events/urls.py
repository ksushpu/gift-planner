from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.events, name="list"),
    path("<slug:event_slug>/", views.event_detail, name="detail"),
]
