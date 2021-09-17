import os
from pathlib import Path

import storygraph.importer as imp
from django.core.files import File
from django.db import IntegrityError, migrations, transaction

from MorFgeet.settings import MEDIA_ROOT


def create_static(apps, schema_editor):
    Sound = apps.get_model("storygraph", "Sound")
    sound_file = File(open(os.path.join(MEDIA_ROOT, "static.mp3"), "rb"))
    try:
        with transaction.atomic():
            sound = Sound.objects.create(title="__static__")
            name = sound_file.file.name.split("/")[-1]
            sound.file.save(name, sound_file)
            sound.save()
    except IntegrityError:
        Sound.objects.create(title="__static__")


def create_corruption(apps, schema_editor):
    Corruption = apps.get_model("storygraph", "Corruption")
    Corruption.objects.create()


def import_story(apps, schema_editor):
    nodes, links = imp.parse_story("MorFgeet.csv")
    imp.import_story(nodes, links)


class Migration(migrations.Migration):
    dependencies = [
        ("storygraph", "0009_node_corruption_value"),
    ]

    operations = [
        migrations.RunPython(create_static),
        migrations.RunPython(create_corruption),
        migrations.RunPython(import_story),
    ]
