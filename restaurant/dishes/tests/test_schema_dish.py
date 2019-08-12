from unittest import TestCase
from graphene.test import Client

from restaurant.dishes.models import Dish
from restaurant.dishes.schemas import schema


class DishSchemaTest(TestCase):
    def setUp(self):
        self.client = Client(schema=schema)
    
    def tearDown(self):
        Dish.objects.all().delete()

    def test_query_dish(self):
        self.obj = Dish.objects.create(name='Burrata')
        query = '''
            query getDish($id: ID!) {
                dish(id: $id) {
                    name
                }
            }
            '''

        result = self.client.execute(query, variables={'id': self.obj.pk})

        self.assertEqual(result['data']['dish']['name'], 'Burrata')

    def test_query_dishes(self):
        dishes = list((Dish.objects.create(name=f'item_{_}') for _ in range(5)))

        query =  '''
            query {
                dishes {
                    name
                }
            }'''

        result = self.client.execute('''query { dishes {name} }''')
        self.assertEqual(len(result['data']['dishes']), 5)