from django.db import migrations
from django.utils.text import slugify
from unidecode import unidecode


def fill_slugs(apps, schema_editor):
    Event = apps.get_model("events", "Event")
    for event in Event.objects.all():
        base = slugify(unidecode(event.title)) or "event"
        event.slug = f"{base}-{event.pk}"
        event.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0002_event_event_year_event_slug_alter_event_date_and_more"),
    ]

    operations = [
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
    ]
