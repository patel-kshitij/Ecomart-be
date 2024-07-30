from django.db import models


class AddressModel(models.Model):
    id = models.AutoField(primary_key=True)
    apartment = models.CharField(max_length=50)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "application"
        db_table = "address"
