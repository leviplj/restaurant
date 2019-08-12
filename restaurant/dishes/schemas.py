import graphene

from restaurant.dishes.models import Dish

class DishType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()


class Query(graphene.ObjectType):
    dish = graphene.Field(DishType, id=graphene.ID(required=True))
    dishes = graphene.List(DishType)

    def resolve_dish(self, info, id):
        return Dish.objects.get(pk=id)

    def resolve_dishes(self, info, **kwargs):
        return Dish.objects.all()


class CreateDish(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    dish = graphene.Field(DishType)

    def mutate(self, info, name):
        dish = Dish.objects.create(name=name)
        ok = True
        return CreateDish(dish=dish, ok=ok)


class UpdateDish(graphene.Mutation):
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


class Mutation(graphene.ObjectType):
    create_dish = CreateDish.Field()
    update_dish = UpdateDish.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)