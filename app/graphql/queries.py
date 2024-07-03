import graphene
from app.schemas.complex import UserType, ChannelType, UserComplexType, ChannelComplexType
from app.handlers.handlers import UserHandler, ChannelHandler


def get_requested_models(info):
    """Recursively extract all requested field names"""
    field_names = []

    def combine_fields(field_node):
        fields = []

        if field_node.selection_set:
            fields.append(field_node.name.value)
            for field in field_node.selection_set.selections:
                fields.extend(combine_fields(field))
            return fields
        else:
            return fields

    if info.field_nodes:
        field_names = combine_fields(info.field_nodes[0])
    return field_names


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, user_id=graphene.String(required=True))
    users = graphene.List(UserType)
    channel = graphene.Field(
        ChannelType, channel_id=graphene.String(required=True))
    channels = graphene.List(ChannelType)

    complex_user = graphene.Field(
        UserComplexType, user_id=graphene.String(required=True))

    complex_channel = graphene.Field(
        ChannelComplexType, channel_id=graphene.String(required=True))

    async def resolve_user(self, info, user_id):
        # requested_models = get_requested_models(info)
        # return await UserHandler().get_complex_user(user_id=user_id, requested_models=requested_models)
        return await UserHandler().get_user(user_id=user_id)

    async def resolve_users(self, info):
        return await UserHandler().get_users()

    async def resolve_channel(self, info, channel_id):
        return await ChannelHandler().get_channel(channel_id=channel_id)

    async def resolve_channels(self, info):
        return await ChannelHandler().get_channels()

    async def resolve_complex_user(self, info, user_id):
        requested_models = get_requested_models(info)
        return await UserHandler().get_complex_user(user_id=user_id, requested_models=requested_models)
    
    async def resolve_complex_channel(self, info, channel_id):
        requested_models = get_requested_models(info)
        return await ChannelHandler().get_complex_channel(channel_id=channel_id, requested_models=requested_models)
