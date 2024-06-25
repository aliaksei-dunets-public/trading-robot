from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings, consts
from bson import ObjectId
from datetime import datetime

client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]


class MongoDB:
    def __init__(self, collection_name: str):
        if not collection_name:
            raise Exception(f"[DB]: Collection name is missed")
        self._collection_name = collection_name
        self._collection = db[collection_name]

    async def insert_one(self, query: dict) -> str:
        if not query:
            raise Exception(
                f"[DB]: {self._collection_name}: insert_one - Query is empty")
        else:
            query[consts.DB_FIELD_CREATED_AT] = datetime.utcnow()
            query[consts.DB_FIELD_CHANGED_AT] = datetime.utcnow()

        result = await self._collection.insert_one(query)
        return str(result.inserted_id)

    async def find_one(self, id: str) -> dict:
        result = await self._collection.find_one({consts.DB_FIELD_ID: self._convert_id(id)})
        return result

    async def find_one_by_filter(self, query: dict) -> dict:
        if not query:
            raise Exception(
                f"[DB]: {self._collection_name}: find_one_by_filter - Query is empty")
        result = await self._collection.find_one(query)
        return result

    async def find_many(self, query: dict = {}) -> list:
        cursor = self._collection.find(query)
        result = []
        async for entry in cursor:
            result.append(entry)
        return result

    def _convert_id(self, id: str) -> str:
        if not id:
            raise Exception(f"[DB]: {self._collection_name} - _id is missed")

        return ObjectId(id)
