# Generated by Django 5.0 on 2023-12-30 18:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_remove_user_user_listings_listing_listing_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='listing_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_listing', to=settings.AUTH_USER_MODEL),
        ),
    ]