# Generated by Django 2.2.24 on 2021-11-09 14:46

# Django imports
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [("dalec_prime", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="content",
            name="channel_object",
            field=models.CharField(
                blank=True,
                max_length=255,
                null=True,
                verbose_name="channel app object id",
            ),
        ),
        migrations.AlterIndexTogether(
            name="content",
            index_together={("app", "content_type", "channel", "channel_object")},
        ),
    ]
