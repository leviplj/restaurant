from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'dish'
        verbose_name_plural = 'dishes'
