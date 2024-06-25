from app.models.user import UserModel, UserModifyModel
from app.db.database import MongoDB
from app.core.config import consts
from datetime import datetime

class UserHandler:    
    def __init__(self) -> None:
        self._db = MongoDB(consts.DB_COLLECTION_USERS)

    async def get_user(self, user_id: str) -> UserModel:
        data =  await self._db.find_one(user_id)
        return UserModel(**data) if data else None

    async def get_users(self) -> list[UserModel]:
        data =  await self._db.find_many()
        users = [UserModel(**user) for user in data]
        return users if users else []

    async def create_user(self, user: UserModifyModel) -> UserModel:
        user_dict = user.to_mongodb()
        created_id = await self._db.insert_one(user_dict)
        return self.get_user(created_id)

    # @staticmethod
    # async def update_user(user_id: str, user: UserModel) -> UserModel:
    #     user_dict = user.to_mongodb()
    #     user_dict["changed_at"] = datetime.utcnow()
    #     await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": user_dict})
    #     user.id = user_id
    #     return user

    # @staticmethod
    # async def delete_user(user_id: str) -> bool:
    #     result = await db["users"].delete_one({"_id": ObjectId(user_id)})
    #     return result.deleted_count > 0
