from django.contrib import admin

from gifts.models import Gift

from .models import Event


class GiftInline(admin.TabularInline):
    model = Gift
    extra = 0
    fields = ("id", "idea", "person", "status")
    readonly_fields = ("id",)
    show_change_link = True


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date", "event_year", "person")
    list_display_links = ("title",)
    list_filter = ("date", "person")
    search_fields = ("title", "person__name")
    list_select_related = ("person",)
    readonly_fields = ("slug", "event_year")
    ordering = ("date", "id")
    inlines = (GiftInline,)
