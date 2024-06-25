from app.models.common import BaseModel, IdentifierModel, AdminModel


class UserModifyModel(BaseModel):
    first_name: str
    second_name: str
    technical_user: bool = False

    def to_mongodb(self):
        return {
            "first_name": self.first_name,
            "second_name": self.second_name,
            "technical_user": self.technical_user,
        }


class UserModel(IdentifierModel, UserModifyModel, AdminModel):
    pass
