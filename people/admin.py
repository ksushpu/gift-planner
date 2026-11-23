from django.contrib import admin

from events.models import Event
from gifts.models import Gift

from .models import Person


class EventInline(admin.TabularInline):
    model = Event
    extra = 0
    fields = ("title", "date", "slug")
    readonly_fields = ("slug",)
    show_change_link = True


class GiftInline(admin.TabularInline):
    model = Gift
    extra = 0
    fields = ("idea", "event", "status")
    show_change_link = True


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    inlines = (EventInline, GiftInline)
