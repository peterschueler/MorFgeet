# Generated by Django 3.1.7 on 2021-08-29 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("storygraph", "0006_rename_fk_on_link"),
    ]

    operations = [
        migrations.CreateModel(
            name="Corruption",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("level", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name": "Corruption",
            },
        ),
    ]
