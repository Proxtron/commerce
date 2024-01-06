# Generated by Django 4.2.7 on 2023-12-29 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_user_user_listings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_listings',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='listing_owner', to='auctions.listing'),
        ),
    ]
