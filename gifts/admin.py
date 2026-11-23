from django.contrib import admin

from .models import Gift


@admin.action(description="Отметить выбранные подарки как вручённые")
def mark_given(modeladmin, request, queryset):
    queryset.update(status=Gift.Status.GIVEN)


@admin.action(description="Вернуть выбранные подарки в статус «Запланирован»")
def mark_planned(modeladmin, request, queryset):
    queryset.update(status=Gift.Status.PLANNED)


@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ("id", "idea", "person", "event", "status")
    list_display_links = ("idea",)
    list_filter = ("status", "person", "event")
    search_fields = ("idea", "person__name", "event__title")
    list_editable = ("status",)
    list_select_related = ("person", "event")
    ordering = ("id",)
    actions = (mark_given, mark_planned)
