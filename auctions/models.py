from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField(
        "Listing",
    )

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=200, blank=True, default="")
    belongs_to_category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="category_of_listing",
        null=True,
    )
    listing_owner = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="user_listing",
        null=True,
    )
    is_open = models.BooleanField(default=True)
    winning_user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="winlist",
        null=True,
    )

class Bid(models.Model):
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=-1)

    bid_owner = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="user_bid",
        null=True,
    )
    bid_listing = models.ForeignKey(
        "Listing",
        on_delete=models.CASCADE,
        related_name="listing_bid",
        null=True,
    )


class Comment(models.Model):
    message = models.CharField(max_length=500, null=True)
    belongs_to_listing = models.ForeignKey(
        "Listing",
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
    )

    belongs_to_user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="user_comments",
        null=True,
    )

class Category(models.Model):
    category_name = models.CharField(max_length=200, blank=True, default="")