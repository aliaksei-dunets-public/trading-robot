from graphene import ObjectType, String, Boolean, DateTime

class UserType(ObjectType):
    id = String()
    first_name = String()
    second_name = String()
    technical_user = Boolean()
    created_at = DateTime()
    changed_at = DateTime()
