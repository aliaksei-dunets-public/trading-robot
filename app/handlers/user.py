from app.models.user import UserModel
# from app.db.database import db
from bson.objectid import ObjectId
from datetime import datetime

class UserHandler:
    pass
    
    # @staticmethod
    # async def get_user_by_id(user_id: str) -> UserModel:
    #     data = await db["users"].find_one({"_id": ObjectId(user_id)})
    #     return UserModel(**data) if data else None

    # @staticmethod
    # async def create_user(user: UserModel) -> UserModel:
    #     user_dict = user.to_mongodb()
    #     user_dict["created_at"] = datetime.utcnow()
    #     user_dict["changed_at"] = datetime.utcnow()
    #     result = await db["users"].insert_one(user_dict)
    #     user.id = str(result.inserted_id)
    #     return user

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
