from django.urls import path
from . import views

app_name = "gifts"

urlpatterns = [
    path("", views.gifts, name="list"),
    path("create/", views.gift_create, name="create"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:gift_id>/edit/", views.gift_edit, name="edit"),
    path("<int:gift_id>/cancel/", views.gift_cancel, name="cancel"),
    path("<int:gift_id>/", views.gift_detail, name="detail"),
]
