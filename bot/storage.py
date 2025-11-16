import asyncio
import json
import os
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings


JSON_DB = "user_settings.json"
_lock = asyncio.Lock()


class Storage:
def __init__(self):
self.mongo = None
if settings.MONGO_URI:
self.mongo = AsyncIOMotorClient(settings.MONGO_URI).watermark_bot


async def get_user(self, user_id: int) -> dict:
if self.mongo:
doc = await self.mongo.users.find_one({"_id": user_id})
return doc or {}
else:
async with _lock:
if not os.path.exists(JSON_DB):
with open(JSON_DB, "w") as f:
json.dump({}, f)
with open(JSON_DB, "r") as f:
data = json.load(f)
return data.get(str(user_id), {})


async def save_user(self, user_id: int, obj: dict):
if self.mongo:
obj_copy = obj.copy()
obj_copy['_id'] = user_id
await self.mongo.users.replace_one({'_id': user_id}, obj_copy, upsert=True)
else:
async with _lock:
with open(JSON_DB, 'r') as f:
data = json.load(f)
data[str(user_id)] = obj
with open(JSON_DB, 'w') as f:
json.dump(data, f, indent=2)


storage = Storage()
