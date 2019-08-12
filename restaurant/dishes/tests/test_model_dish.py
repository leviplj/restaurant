from django.test import TestCase

from restaurant.dishes.models import Dish


class DishModelTest(TestCase):
    def setUp(self):
        self.obj = Dish.objects.create(name='Burrata')

    def test_create(self):
        self.assertTrue(Dish.objects.exists())
        