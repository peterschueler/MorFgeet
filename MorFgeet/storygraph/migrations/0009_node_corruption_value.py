# Generated by Django 3.1.7 on 2021-09-06 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("storygraph", "0008_sound"),
    ]

    operations = [
        migrations.AddField(
            model_name="node",
            name="corruption_value",
            field=models.IntegerField(default=0),
        ),
    ]
