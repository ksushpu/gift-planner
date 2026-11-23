from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.events, name="list"),
    path("create/", views.event_create, name="create"),
    path("<slug:event_slug>/edit/", views.event_edit, name="edit"),
    path("<slug:event_slug>/", views.event_detail, name="detail"),
]
