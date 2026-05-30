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

async def link_client_to_against(user_id:int, against_id:int):
    await r.set(f"state:{user_id}", "in-chat")
    await r.set(f"state:{against_id}", "in-chat")

    await r.set(f"against:{user_id}", against_id) # user side
    await r.set(f"against:{against_id}", user_id) # against side

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
    await link_client_to_against(user1, user2)
    return [user1, user2]

async def get_against_id(user_id:int):
    against_id = await r.get(f"against:{user_id}")
    return against_id

async def get_user_state(user_id:int):
    state = await r.get(f"state:{user_id}")
    return state

async def end_connection(user_id:int, against_id:int):
    await r.delete(f"state:{user_id}"); await r.delete(f"state:{against_id}")
    await r.delete(f"against:{user_id}"); await r.delete(f"against:{against_id}")
