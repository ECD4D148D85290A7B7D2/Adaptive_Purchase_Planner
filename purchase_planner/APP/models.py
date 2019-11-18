from django.db import models


# Create your models here.

class Purchases(models.Model):

    user_id = models.IntegerField(null=False)
    item = models.CharField(max_length=255, null=False)
    price = models.FloatField(null=False)
    store = models.CharField(max_length=255, null=False)
    purchase_date = models.DateField(auto_now=False, auto_now_add=False, null=False)

    def __str__(self):
        return "{} - {}".format(self.user_id, self.item, self.price, self.store, self.purchase_date)
