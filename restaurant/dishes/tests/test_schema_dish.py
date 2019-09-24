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
            query getDish($id: Int!) {
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
        
    def test_mutation_create_dish(self):
        mutation = '''
            mutation createDish($name: String!) {
                createDish(name: $name) {
                    dish {
                        name
                    }
                    ok
                }
            }'''
        result = self.client.execute(mutation, variables={'name': 'Burrata'})

        self.assertTrue(result['data']['createDish']['ok'])
        self.assertEqual(result['data']['createDish']['dish']['name'], 'Burrata')

        self.assertTrue(Dish.objects.exists())
        self.assertEqual(Dish.objects.all().first().name, 'Burrata')


    def test_mutation_update_dish(self):
        self.obj = Dish.objects.create(name='Burrata')
        self.assertTrue(Dish.objects.exists())
        self.assertEqual(Dish.objects.all().first().name, 'Burrata')

        mutation = '''
            mutation updateDish($id: Int!, $name: String!) {
                updateDish(id: $id, name: $name) {
                    dish {
                        id,
                        name
                    }
                    ok
                }
            }'''

        result = self.client.execute(mutation, variables={'id': self.obj.id, 'name': 'Burrata 2'})
        self.assertTrue(result['data']['updateDish']['ok'])
        self.assertEqual(result['data']['updateDish']['dish']['id'], self.obj.id)
        self.assertEqual(result['data']['updateDish']['dish']['name'], 'Burrata 2')

        self.assertEqual(Dish.objects.all().first().name, 'Burrata 2')

    def test_mutation_delete_dish(self):
        dishes = list((Dish.objects.create(name=f'item_{_}') for _ in range(3)))

        self.assertTrue(Dish.objects.exists())
        self.assertEqual(Dish.objects.all().count(), 3)

        mutation = '''
            mutation deleteDish($id: Int!) {
                deleteDish(id: $id) {
                    dish {
                        id,
                        name
                    }
                    ok
                }
            }'''

        result = self.client.execute(mutation, variables={'id': dishes[2].id})

        self.assertTrue(result['data']['deleteDish']['ok'])
        self.assertEqual(result['data']['deleteDish']['dish']['name'], 'item_2')

        self.assertEqual(Dish.objects.all().count(), 2)

    