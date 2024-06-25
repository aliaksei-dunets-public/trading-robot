import graphene
from app.schemas.user import UserType, UserInput
from app.models.user import UserModifyModel
from app.handlers.user import UserHandler


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    user = graphene.Field(UserType)

    async def mutate(self, info, user_data):
        user_modify_mdl = UserModifyModel(**user_data)
        user_mdl = await UserHandler().create_user(user_modify_mdl)
        return CreateUser(user=user_mdl)

# class UpdateUser(graphene.Mutation):
#     class Arguments:
#         user_id = graphene.String(required=True)
#         first_name = graphene.String(required=False)
#         second_name = graphene.String(required=False)
#         technical_user = graphene.Boolean(required=False)

#     user = graphene.Field(UserType)

#     async def mutate(self, info, user_id, first_name=None, second_name=None, technical_user=None):
#         user = await UserHandler.get_user_by_id(user_id)
#         if not user:
#             raise Exception("User not found")

#         if first_name is not None:
#             user.first_name = first_name
#         if second_name is not None:
#             user.second_name = second_name
#         if technical_user is not None:
#             user.technical_user = technical_user

#         user = await UserHandler.update_user(user_id, user)
#         return UpdateUser(user=user)

# class DeleteUser(graphene.Mutation):
#     class Arguments:
#         user_id = graphene.String(required=True)

#     success = graphene.Boolean()

#     async def mutate(self, info, user_id):
#         success = await UserHandler.delete_user(user_id)
#         return DeleteUser(success=success)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    # update_user = UpdateUser.Field()
    # delete_user = DeleteUser.Field()
