import storygraph.importer as imp
from django.db import migrations


def create_static(apps, schema_editor):
    Sound = apps.get_model("storygraph", "Sound")
    Sound.objects.create(title="__static__")


def import_story(apps, schema_editor):
    nodes, links = imp.parse_story("MorFgeet.csv")
    imp.import_story(nodes, links)


class Migration(migrations.Migration):
    dependencies = [
        ("storygraph", "0009_node_corruption_value"),
    ]

    operations = [
        migrations.RunPython(create_static),
        migrations.RunPython(import_story),
    ]
