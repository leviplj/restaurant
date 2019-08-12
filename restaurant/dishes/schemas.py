import graphene

from restaurant.dishes.models import Dish

class DishType(graphene.ObjectType):
    '''Dish object'''
    id = graphene.Int()
    name = graphene.String()


class Query(graphene.ObjectType):
    dish = graphene.Field(DishType, id=graphene.Int(required=True), description='Return a dish according to the given id')
    dishes = graphene.List(DishType, description='Return a list of all dishes')

    def resolve_dish(self, info, id):
        '''always pass an object for `me` field'''
        return Dish.objects.get(pk=id)

    def resolve_dishes(self, info, **kwargs):
        return Dish.objects.all()


class CreateDish(graphene.Mutation):
    '''Creates and return a dish\n
     params name: String
    '''
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    dish = graphene.Field(DishType)

    def mutate(self, info, name):
        dish = Dish.objects.create(name=name)
        ok = True
        return CreateDish(dish=dish, ok=ok)


class UpdateDish(graphene.Mutation):
    '''Update a dish according to the given id and return it\n
     params id: Int, name: String
    '''
    class Arguments:
        id = graphene.Int()
        name = graphene.String()

    ok = graphene.Boolean()
    dish = graphene.Field(DishType)

    def mutate(self, info, id, name):
        dish = Dish.objects.get(pk=id)
        dish.name = name
        dish.save()
        ok = True
        return UpdateDish(dish=dish, ok=ok)

class DeleteDish(graphene.Mutation):
    '''Delete a dish according to the given id and return it\n
     params id: Int
    '''
    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()
    dish = graphene.Field(DishType)

    def mutate(self, info, id):
        dish = Dish.objects.get(pk=id)
        dish.delete()
        ok = True
        return DeleteDish(dish=dish, ok=ok)


class Mutation(graphene.ObjectType):
    create_dish = CreateDish.Field()
    update_dish = UpdateDish.Field()
    delete_dish = DeleteDish.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)