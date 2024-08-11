from django.db import models
from apps.accounts.models import UserModel
from apps.application.models import ItemModel


class WishlistModel(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "application"
        db_table = "wishlist"
