from django.db import models
from apps.accounts.models import UserModel


class ItemModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    seller = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    price = models.FloatField(null=False, blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "application"
        db_table = "item"
