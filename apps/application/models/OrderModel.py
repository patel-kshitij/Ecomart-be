from django.db import models
from apps.accounts.models import UserModel
from apps.application.models import ItemModel


class OrderModel(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    shipping_address = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "application"
        db_table = "orders"
