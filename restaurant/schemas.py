import graphene

import restaurant.dishes.schemas


class Query(restaurant.dishes.schemas.Query, graphene.ObjectType):
    pass

class Mutation(restaurant.dishes.schemas.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)