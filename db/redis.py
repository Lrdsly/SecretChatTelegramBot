import redis.asyncio as redis
from random import sample

from db.pool import execute

# ---- TODAY IS GREAT ----

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

async def add_to_queue(telegram_id:int):
    await r.sadd("anon_chat_queue", telegram_id)

async def remove_from_anon_chat_queue(telegram_id:int):
    await r.srem("anon_chat_queue", telegram_id)

async def match_users():
    user1 = await r.spop("anon_chat_queue")
    if not user1:
        return None
    user2 = await r.spop("anon_chat_queue")
    if not user2:
        await r.sadd("anon_chat_queue", user1)
        return None
    query = "INSERT INTO a_connections (user1_id, user2_id) VALUES (%s, %s)"
    await execute(query, (user1, user2))
    return [user1, user2]

