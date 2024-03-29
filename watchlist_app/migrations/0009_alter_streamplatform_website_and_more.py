# Generated by Django 5.0.1 on 2024-02-16 15:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("watchlist_app", "0008_rename_abg_rating_watchlist_avg_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="streamplatform",
            name="website",
            field=models.URLField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="watchlist",
            name="storyline",
            field=models.CharField(max_length=200),
        ),
    ]
