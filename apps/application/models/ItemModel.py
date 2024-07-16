from django.db import models
from apps.accounts.models import UserModel
from apps.application.models.CategoryModel import CategoryModel


class ItemModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    seller = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    price = models.FloatField(null=False, blank=False)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "application"
        db_table = "item"
