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
    await r.rpush("queue", telegram_id)

async def remove_from_queue(telegram_id:int):
    # remove the first found object from the list. start from left side.
    await r.lrem("queue", 1, telegram_id)

async def match_users():
    more_waiting_users = await r.lrange("queue", 0, 9)
    if len(more_waiting_users) < 2:
        return None
    selected = sample(more_waiting_users, k=2)
    for user in selected:
        await remove_from_queue(user)
    query = "INSERT INTO a_connections (user1_id, user2_id) VALUES (%s, %s)"
    await execute(query, tuple(selected))
    return selected

