from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("people/", include("people.urls")),
    path("events/", include("events.urls")),
    path("gifts/", include("gifts.urls")),
]

handler404 = "homepage.views.page_not_found"
