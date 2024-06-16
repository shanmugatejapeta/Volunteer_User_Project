# Generated by Django 5.0.6 on 2024-06-14 02:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="volunteers",
            name="user",
        ),
        migrations.AddField(
            model_name="problems",
            name="resolved",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="VUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vols",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "vol",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="users",
                        to="app.volunteers",
                    ),
                ),
            ],
        ),
    ]