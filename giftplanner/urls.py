from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Gift Planner"
admin.site.site_title = "Gift Planner"
admin.site.index_title = "Управление подарками"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("people/", include("people.urls")),
    path("events/", include("events.urls")),
    path("gifts/", include("gifts.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "homepage.views.page_not_found"
