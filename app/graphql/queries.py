import graphene
from app.schemas.user import UserType
from app.handlers.user import UserHandler


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, user_id=graphene.String(required=True))
    users = graphene.List(UserType)

    async def resolve_user(self, info, user_id):
        return await UserHandler().get_user(user_id)
    
    async def resolve_users(self, info):
        return await UserHandler().get_users()
