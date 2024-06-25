import graphene
from app.schemas.user import UserType
from app.handlers.user import UserHandler

class Query(graphene.ObjectType):
    user = graphene.Field(UserType, user_id=graphene.String(required=True))

    async def resolve_user(self, info, user_id):
        # user = await UserHandler.get_user_by_id(user_id)
        return {
            "first_name": "Aliaksei",
            "second_name": "Duents",
            "technical_user": True,
        }
