from django.urls import path

from . import views

urlpatterns = [
    path("", views.gifts, name="gifts"),
    path("<int:gift_id>/", views.gift_detail, name="gift_detail"),
]
