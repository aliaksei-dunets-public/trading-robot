import graphene
from app.schemas.main import UserType, UserCreateInput, UserChangeInput
from app.models.main import UserChangeModel, UserCreateModel
from app.handlers.handlers import UserHandler


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = UserCreateInput(required=True)

    user = graphene.Field(UserType)

    async def mutate(self, info, user_data):
        user_modify_mdl = UserCreateModel(**user_data)
        user_mdl = await UserHandler().create_user(user_modify_mdl)
        return CreateUser(user=user_mdl)


class UpdateUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)
        user_data = UserChangeInput(required=True)

    user = graphene.Field(UserType)

    async def mutate(self, info, user_id, user_data):
        user_modify_mdl = UserChangeModel(**user_data)
        user = await UserHandler().update_user(user_id, user_modify_mdl)
        return UpdateUser(user=user)


class DeleteUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)

    success = graphene.Boolean()

    async def mutate(self, info, user_id):
        success = await UserHandler().delete_user(user_id)
        return DeleteUser(success=success)

# class CreateChannel(graphene.Mutation):
#     class Arguments:
#         user_data = UserCreateInput(required=True)

#     user = graphene.Field(UserType)

#     async def mutate(self, info, user_data):
#         user_modify_mdl = UserCreateModel(**user_data)
#         user_mdl = await UserHandler().create_user(user_modify_mdl)
#         return CreateUser(user=user_mdl)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
