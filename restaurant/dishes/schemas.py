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


schema = graphene.Schema(query=Query)