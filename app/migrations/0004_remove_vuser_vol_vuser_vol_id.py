# Generated by Django 5.0.6 on 2024-06-14 03:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0003_alter_problems_resolved"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vuser",
            name="vol",
        ),
        migrations.AddField(
            model_name="vuser",
            name="vol_id",
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]