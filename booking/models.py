from django.db import models


# Create your models here.
class Participant(models.Model):
    name = models.CharField(max_length=128, default = "")
    email = models.EmailField()
    spex = models.BooleanField()
    nachspex = models.BooleanField()
    diet = models.CharField(max_length=128, default = "")
    alcoholfree = models.BooleanField()
    avec = models.CharField(max_length=256, default = "")
    comment = models.TextField(default="none")
    discount_code = models.ForeignKey('DiscountCode', db_column='participants', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DiscountCode(models.Model):
    code = models.CharField(max_length=8)
    price = models.FloatField()
    used = models.BooleanField(default = False)
    
    def __str__(self):
        return self.code
