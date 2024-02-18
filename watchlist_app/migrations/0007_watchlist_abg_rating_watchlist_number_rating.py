# Generated by Django 5.0.1 on 2024-02-08 03:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("watchlist_app", "0006_review_review_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="watchlist",
            name="abg_rating",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="watchlist",
            name="number_rating",
            field=models.IntegerField(default=0),
        ),
    ]
