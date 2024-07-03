from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings, consts
from bson import ObjectId
from datetime import datetime

client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]


class MongoDB:
    def __init__(self, collection_name: str):
        if not collection_name:
            raise Exception(
                f"[{self.__class__.__name__}]: Collection name is missed")
        self._collection_name = collection_name
        self._collection = db[collection_name]

    async def insert_one(self, query: dict) -> str:
        if not query:
            raise Exception(
                f"[{self.__class__.__name__}]: {self._collection_name}: insert_one - Query is empty")

        query[consts.DB_FIELD_CREATED_AT] = datetime.utcnow()
        query[consts.DB_FIELD_CHANGED_AT] = datetime.utcnow()

        result = await self._collection.insert_one(query)
        return str(result.inserted_id)

    async def insert_many(self, entries: list) -> list:
        if not entries:
            raise Exception(
                f"[{self.__class__.__name__}]: {self._collection_name}: insert_many - Entries are missed")

        for entry in entries:
            entry[consts.DB_FIELD_CREATED_AT] = datetime.utcnow()
            entry[consts.DB_FIELD_CHANGED_AT] = datetime.utcnow()

        result = await self._collection.insert_many(entries)
        return result.inserted_ids

    async def update_one(self, id: str, query: dict) -> bool:
        return await self.__update_one(id=id, query=query, upsert=True)

    async def upsert_one(self, id: str, query: dict) -> bool:
        return await self.__update_one(id=id, query=query, upsert=True)

    async def delete_one(self, id: str) -> bool:
        result = await self._collection.delete_one({consts.DB_FIELD_ID: self._convert_id(id)})
        return result.deleted_count > 0

    async def delete_many(self, query: dict) -> bool:
        if not query:
            raise Exception(
                f"[{self.__class__.__name__}]: {self._collection_name}: delete_many - Query is empty")
        result = await self._collection.delete_many(query)
        return result.deleted_count > 0

    async def find_one(self, id: str) -> dict:
        result = await self._collection.find_one({consts.DB_FIELD_ID: self._convert_id(id)})
        return result

    async def find_one_by_filter(self, query: dict) -> dict:
        if not query:
            raise Exception(
                f"[{self.__class__.__name__}]: {self._collection_name}: find_one_by_filter - Query is empty")
        result = await self._collection.find_one(query)
        return result

    async def find_many(self, query: dict = {}) -> list:
        result = []
        cursor = self._collection.find(query)
        async for entry in cursor:
            result.append(entry)
        return result

    async def get_count(self, query: dict = {}) -> int:
        return await self._collection.count_documents(query)

    async def aggregate(self, query: dict = {}) -> list:
        if not query:
            raise Exception(
                f"[{self.__class__.__name__}]: {self._collection_name}: aggregate - Query is empty")

        result = []
        cursor = self._collection.aggregate(query)
        async for entry in cursor:
            result.append(entry)
        return result

    async def __update_one(self, id: str, query: dict, upsert: bool = False) -> bool:
        if not query:
            raise Exception(
                f"[{self.__class__.__name__}]: {self._collection_name}: update_one - Query is empty")

        query[consts.DB_FIELD_CHANGED_AT] = datetime.utcnow()

        result = await self._collection.update_one(
            {consts.DB_FIELD_ID: self._convert_id(id)}, {"$set": query}, upsert
        )

        return result.modified_count == 1

    def _convert_id(self, id: str) -> str:
        if not id:
            raise Exception(f"[{self.__class__.__name__}]: {
                            self._collection_name} - _id is missed")

        return ObjectId(id)
