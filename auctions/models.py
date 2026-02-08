from django.contrib.auth.models import AbstractUser
from django.db import models
from sqlalchemy import true


class User(AbstractUser):
    pass

class Auction(models.Model):
    EEYLOPS_OWL_EMPORIUM = "OWL"
    FLOURISH_AND_BLOTTS = "BOK"
    MAGICAL_MENAGERIE = "CRE"
    OLLIVANDERS = "WAN"
    QUALITY_QUIDDITCH_SUPPLIES = "QUI"
    WEASLEYS_WIZARD_WHEEZES = "WWW"

    CATEGORY = [
        (EEYLOPS_OWL_EMPORIUM, "Owls"),
        (FLOURISH_AND_BLOTTS, "Books"),
        (MAGICAL_MENAGERIE, "Magical Creatures"),
        (OLLIVANDERS, "Wands"),
        (QUALITY_QUIDDITCH_SUPPLIES, "Quidditch Supplies"),
        (WEASLEYS_WIZARD_WHEEZES, "Everything a Mischief-Maker Could Possibly Want"),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=True)
    current_price = models.DecimalField(max_digits=11, decimal_places=2, default=0.0)
    category = models.CharField(max_length=3, choices=CATEGORY, default=WEASLEYS_WIZARD_WHEEZES)
    image_url = models.URLField(blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "auction"
        verbose_name_plural = "auctions"

    def __str__(self):
        return f"Auction id: {self.id}, title: {self.title}, seller: {self.seller}"

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now_add=True)
    bid_price = models.DecimalField(max_digits=11, decimal_places=2)

    class Meta:
        verbose_name = "bid"
        verbose_name_plural = "bids"

    def __str__(self):
        return f"{self.user} bid {self.bid_price} $ on {self.auction}"

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    comment_date = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self):
        return f"Comment {self.id} on auction {self.auction} made by {self.user}"

class Watchlist(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")

    class Meta:
        verbose_name = "watchlist"
        verbose_name_plural = "watchlists"
        unique_together = ["auction", "user"]

    def __str__(self):
        return f"{self.auction} on user {self.user} watchlist"