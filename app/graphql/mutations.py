import graphene
from app.schemas.main import UserCreateInput, UserChangeInput, UserType, ChannelCreateInput, ChannelChangeInput, ChannelType
from app.models.main import UserChangeModel, UserCreateModel, ChannelCreateModel, ChannelChangeModel
from app.handlers.handlers import UserHandler, ChannelHandler


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = UserCreateInput(required=True)

    user = graphene.Field(UserType)

    async def mutate(parent, info, user_data):
        user_create_mdl = UserCreateModel(**user_data)
        user_mdl = await UserHandler().create_user(user_create_mdl)
        return CreateUser(user=user_mdl)


class UpdateUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)
        user_data = UserChangeInput(required=True)

    user = graphene.Field(UserType)

    async def mutate(parent, info, user_id, user_data):
        user_modify_mdl = UserChangeModel(**user_data)
        user = await UserHandler().update_user(user_id, user_modify_mdl)
        return UpdateUser(user=user)


class DeleteUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)

    success = graphene.Boolean()

    async def mutate(parent, info, user_id):
        success = await UserHandler().delete_user(user_id)
        return DeleteUser(success=success)


class CreateChannel(graphene.Mutation):
    class Arguments:
        channel_data = ChannelCreateInput(required=True)

    channel = graphene.Field(ChannelType)

    async def mutate(parent, info, channel_data):
        create_mdl = ChannelCreateModel(**channel_data)
        model = await ChannelHandler().create_channel(create_mdl)
        return CreateChannel(model)


class UpdateChannel(graphene.Mutation):
    class Arguments:
        channel_id = graphene.String(required=True)
        channel_data = ChannelChangeInput(required=True)

    channel = graphene.Field(ChannelType)

    async def mutate(parent, info, channel_id, channel_data):
        channel_modify_mdl = ChannelChangeModel(**channel_data)
        channel = await ChannelHandler().update_channel(channel_id, channel_modify_mdl)
        return UpdateChannel(channel=channel)


class DeleteChannel(graphene.Mutation):
    class Arguments:
        channel_id = graphene.String(required=True)

    success = graphene.Boolean()

    async def mutate(parent, info, channel_id):
        success = await ChannelHandler().delete_channel(channel_id)
        return DeleteChannel(success=success)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    create_channel = CreateChannel.Field()
    update_channel = UpdateChannel.Field()
    delete_channel = DeleteChannel.Field()
