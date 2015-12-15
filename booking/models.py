from django.db import models


# Create your models here.
class Participant(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    nachspex = models.BooleanField()
    diet = models.CharField(max_length=128)
    alcoholfree = models.BooleanField()
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DiscountCode(models.Model):
    code = models.CharField(max_length=8)
    price = models.FloatField()

    def __str__(self):
        return self.code
