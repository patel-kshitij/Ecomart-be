from django.db import models
from apps.accounts.models import UserModel
from apps.application.models.CategoryModel import CategoryModel
from django.utils.translation import gettext_lazy as _


class ItemModel(models.Model):
    class Condition(models.TextChoices):
        NEW = 'NW', _('New')
        HARDLY_USED = 'HU', _('Hardly Used')
        USED = 'US', _('Used')
        ROUGHLY_USED = 'RS', _('Roughly Used')
        WORSE = 'WR', _('Worse')

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    seller = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    price = models.FloatField(null=False, blank=False)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, null=True, blank=True)
    condition = models.CharField(choices=Condition.choices, max_length=2, null=False, blank=False,
                                 default=Condition.USED)
    is_sold = models.BooleanField(default=False)
    is_bidding_enabled = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "application"
        db_table = "item"
