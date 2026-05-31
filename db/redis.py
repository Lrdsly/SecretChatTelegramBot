import redis.asyncio as redis
from random import sample

from db.pool import execute

# ---- TODAY IS GREAT ----

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

async def update_user_state(user_id:int, state:str):
    await r.set(f"state:{user_id}", state)

async def get_user_state(user_id:int):
    state = await r.get(f"state:{user_id}")
    return state

async def add_to_queue(user_id:int):
    if await get_user_state(user_id) not in ["searching", "anon-chat"]:
        await r.rpush("anon_chat_queue", user_id)
        await update_user_state(user_id, "searching")

async def remove_from_queue(user_id:int):
    await r.lrem("anon_chat_queue", 1, user_id)

async def link_client_to_against(user_id:int, against_id:int, chat_type):
    await update_user_state(user_id, chat_type)
    await update_user_state(against_id, chat_type)

    await r.set(f"against:{user_id}", against_id) # user side
    await r.set(f"against:{against_id}", user_id) # against side
    
async def match_users():
    user1_id = await r.lpop("anon_chat_queue")
    if not user1_id:
        return None
    user2_id = await r.lpop("anon_chat_queue")
    if not user2_id:
        await r.lpush("anon_chat_queue", user1_id)
        return None

    query = "INSERT INTO a_connections (user1_id, user2_id) VALUES (%s, %s)"
    await execute(query, (user1_id, user2_id))
    await link_client_to_against(user1_id, user2_id, "anon-chat")
    return [user1_id, user2_id]

async def match_sa_users(user_id:int, against_id:int):
    """ We know who is against, but user is anonymous"""

    query = """ INSERT INTO sa_connections (user_id, against_id) VALUES (%s, %s)"""
    await execute(query, (user_id, against_id))
    await link_client_to_against(user_id, against_id, "semi-chat")

async def get_against_id(user_id:int):
    against_id = await r.get(f"against:{user_id}")
    return against_id

async def end_connection(user_id:int, against_id:int):
    await r.delete(f"state:{user_id}"); await r.delete(f"state:{against_id}")
    await r.delete(f"against:{user_id}"); await r.delete(f"against:{against_id}")

async def store_chat_id_hash(mapping:dict, user_id:int):
    await r.hset(f"chatmap:{user_id}", 
                    mapping=mapping   
                )

async def check_chat_id_exists(usern:str, user_id:int):
    chat_id = await r.hget(f"chatmap:{user_id}", usern)
    return True if chat_id
    
async def set_current_semi_chat(usern:str, user_id:int):
    chat_id = await r.hget(f"chatmap:{user_id}", usern)
    await r.set(f"current_semi_chat:{user_id}", chat_id)

async def get_current_chat_id(user_id:int):
    return await r.get(f"current_semi_chat:{user_id}")
