from django.db import models
from apps.accounts.models import UserModel
from apps.application.models import ItemModel, AddressModel


class ShippingAddressModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=False, blank=False)
    address = models.ForeignKey(AddressModel, on_delete=models.CASCADE, null=False, blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "application"
        db_table = "shipping_address"


class ContactDetailsModel(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "application"
        db_table = "contact_details"


class OrderModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAddressModel, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(AddressModel, on_delete=models.CASCADE)
    contact_details = models.ForeignKey(ContactDetailsModel, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "application"
        db_table = "order"


class OrderItemModel(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    createAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "application"
        db_table = "order_items"
        unique_together = (("order", "item"),)
