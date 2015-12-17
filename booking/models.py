from django.db import models


# Create your models here.
class Participant(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    spex = models.CharField(max_length=128)
    nachspex = models.CharField(max_length=128)
    diet = models.CharField(max_length=128)
    alcoholfree = models.CharField(max_length=128)
    avec = models.CharField(max_length=256)
    comment = models.TextField()
    discount_code = models.ForeignKey('DiscountCode', db_column='participants', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DiscountCode(models.Model):
    code = models.CharField(max_length=8)
    price = models.FloatField()

    def __str__(self):
        return self.code
