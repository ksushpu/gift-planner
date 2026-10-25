from django.urls import path
from . import views

app_name = "gifts"

urlpatterns = [
    path("", views.gifts, name="list"),
    path("<int:gift_id>/", views.gift_detail, name="detail"),
    path("statistics/", views.statistics, name="statistics"),
]
