import graphene
import app.graphql.schemas as schema
import app.handler.handlers as handler
import app.model.models as model


class Query(graphene.ObjectType):
    user = graphene.Field(
        schema.UserComplexType, user_id=graphene.String(required=True))
    users = graphene.List(schema.UserComplexType)

    channel = graphene.Field(
        schema.ChannelComplexType, channel_id=graphene.String(required=True))
    channels = graphene.List(schema.ChannelComplexType)

    trader = graphene.Field(
        schema.TraderComplexType, trader_id=graphene.String(required=True))
    traders = graphene.List(schema.TraderComplexType)

    symbol = graphene.Field(
        schema.SymbolType, trader_id=graphene.String(required=True), symbol=graphene.String(required=True))
    symbols = graphene.List(
        schema.SymbolType,
        trader_id=graphene.String(required=True),
        symbol=graphene.String(),
        name=graphene.String(),
        status=schema.SymbolStatusGrapheneEnum(),
        type=schema.TradingTypeGrapheneEnum())

    async def resolve_user(parent, info, user_id):
        user_mdl = await handler.UserHandler().get_user(user_id=user_id)
        return model.UserComplexModel(**user_mdl.model_dump())

    async def resolve_users(parent, info):
        user_mdls = await handler.UserHandler().get_users()
        users = [model.UserComplexModel(**user_mdl.model_dump())
                 for user_mdl in user_mdls]
        return users if users else []

    async def resolve_channel(parent, info, channel_id):
        channel_mdl = await handler.ChannelHandler().get_channel(channel_id=channel_id)
        return model.ChannelComplexModel(**channel_mdl.model_dump())

    async def resolve_channels(parent, info):
        return await handler.ChannelHandler().get_channels()

    async def resolve_trader(parent, info, trader_id):
        return await handler.TraderHandler().get_trader(trader_id=trader_id)

    async def resolve_traders(parent, info):
        return await handler.TraderHandler().get_traders()

    async def resolve_symbol(parent, info, trader_id, symbol):
        return await handler.SymbolHandler(trader_id).get_symbol(symbol)

    async def resolve_symbols(parent, info, trader_id, symbol, name, status, type):
        return await handler.SymbolHandler(trader_id).get_symbol_list(symbol=symbol, name=name, status=status, type=type)
