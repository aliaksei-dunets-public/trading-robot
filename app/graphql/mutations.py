import graphene
import app.graphql.schemas as schema
import app.models.models as models
import app.handler.handlers as handler


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = schema.UserCreateInput(required=True)

    user = graphene.Field(schema.UserType)

    async def mutate(parent, info, user_data):
        user_create_mdl = models.UserCreateModel(**user_data)
        user_mdl = await handler.UserHandler().create_user(user_create_mdl)
        return CreateUser(user=user_mdl)


class UpdateUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)
        user_data = schema.UserChangeInput(required=True)

    user = graphene.Field(schema.UserType)

    async def mutate(parent, info, user_id, user_data):
        user_modify_mdl = models.UserChangeModel(**user_data)
        user = await handler.UserHandler().update_user(user_id, user_modify_mdl)
        return UpdateUser(user=user)


class DeleteUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)

    success = graphene.Boolean()

    async def mutate(parent, info, user_id):
        success = await handler.UserHandler().delete_user(user_id)
        return DeleteUser(success=success)


class CreateChannel(graphene.Mutation):
    class Arguments:
        channel_data = schema.ChannelCreateInput(required=True)

    channel = graphene.Field(schema.ChannelType)

    async def mutate(parent, info, channel_data):
        create_mdl = models.ChannelCreateModel(**channel_data)
        channel_mdl = await handler.ChannelHandler().create_channel(create_mdl)
        return CreateChannel(channel_mdl)


class UpdateChannel(graphene.Mutation):
    class Arguments:
        channel_id = graphene.String(required=True)
        channel_data = schema.ChannelChangeInput(required=True)

    channel = graphene.Field(schema.ChannelType)

    async def mutate(parent, info, channel_id, channel_data):
        channel_modify_mdl = models.ChannelChangeModel(**channel_data)
        channel = await handler.ChannelHandler().update_channel(channel_id, channel_modify_mdl)
        return UpdateChannel(channel=channel)


class DeleteChannel(graphene.Mutation):
    class Arguments:
        channel_id = graphene.String(required=True)

    success = graphene.Boolean()

    async def mutate(parent, info, channel_id):
        success = await handler.ChannelHandler().delete_channel(channel_id)
        return DeleteChannel(success=success)


class CreateTrader(graphene.Mutation):
    class Arguments:
        trader_data = schema.TraderCreateInput(required=True)

    trader = graphene.Field(schema.TraderType)

    async def mutate(parent, info, trader_data):
        trader_create_mdl = models.TraderCreateModel(**trader_data)
        trader_mdl = await handler.TraderHandler().create_trader(trader_create_mdl)
        return CreateTrader(trader=trader_mdl)


class UpdateTrader(graphene.Mutation):
    class Arguments:
        trader_id = graphene.String(required=True)
        trader_data = schema.TraderChangeInput(required=True)

    trader = graphene.Field(schema.TraderType)

    async def mutate(parent, info, trader_id, trader_data):
        trader_modify_mdl = models.TraderChangeModel(**trader_data)
        trader = await handler.TraderHandler().update_trader(trader_id, trader_modify_mdl)
        return UpdateTrader(trader=trader)


class DeleteTrader(graphene.Mutation):
    class Arguments:
        trader_id = graphene.String(required=True)

    success = graphene.Boolean()

    async def mutate(parent, info, trader_id):
        success = await handler.TraderHandler().delete_trader(trader_id)
        return DeleteTrader(success=success)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

    create_channel = CreateChannel.Field()
    update_channel = UpdateChannel.Field()
    delete_channel = DeleteChannel.Field()

    create_trader = CreateTrader.Field()
    update_trader = UpdateTrader.Field()
    delete_trader = DeleteTrader.Field()
