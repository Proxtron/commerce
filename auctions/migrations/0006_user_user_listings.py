# Generated by Django 4.2.7 on 2023-12-29 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_category_alter_listing_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_listings',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='listing_owner', to='auctions.listing'),
        ),
    ]
