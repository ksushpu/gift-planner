from django.db import migrations


def copy_status(apps, schema_editor):
    Gift = apps.get_model("gifts", "Gift")
    Gift.objects.filter(is_done=True).update(status="given")
    Gift.objects.filter(is_done=False).update(status="planned")


class Migration(migrations.Migration):

    dependencies = [
        ("gifts", "0002_gift_status_alter_gift_idea"),
    ]

    operations = [
        migrations.RunPython(copy_status, migrations.RunPython.noop),
    ]
