import redis.asyncio as redis
from random import sample

from db.semi_anon import create_sa_connections_row
from db.anon import create_a_connections_row
# ---- TODAY IS GREAT ----

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# ----- General ----
async def update_user_state(user_id:int, state:str):
    """ example: (state:78123495 = 'anon-chat') """

    await r.set(f"state:{user_id}", state)

async def get_user_state(user_id:int):
    """ example: (state:17854950 = 'searching') """

    state = await r.get(f"state:{user_id}")
    return state

async def link_client_to_against(user_id:int, against_id:int, chat_type):
    """ 
        example: (against:8745316 = 12345678) and (against:12345678 = 8745316)
        it also update user state (anon-chat instead of seraching or ...)
    """

    await update_user_state(user_id, chat_type)
    await update_user_state(against_id, chat_type)

    await r.set(f"against:{user_id}", against_id) # user side
    await r.set(f"against:{against_id}", user_id) # against side

async def get_against_id(user_id:int):
    """ example: (against:12345678 = 8888822222)"""

    against_id = await r.get(f"against:{user_id}")
    return against_id

async def end_connection(user_id:int, against_id:int):
    """ 
        delete state:nnnnnnnn (since now it will return none)
        delete against:nnnnnnnn (since now it will return none)
    """

    await r.delete(f"state:{user_id}"); await r.delete(f"state:{against_id}")
    await r.delete(f"against:{user_id}"); await r.delete(f"against:{against_id}")

# ---- Anonymous chat ----
async def add_to_queue(user_id:int):
    """ add a telegram id to 'search for aponent' list from right side """

    if await get_user_state(user_id) not in ["searching", "anon-chat"]:
        await r.rpush("anon_chat_queue", user_id)
        await update_user_state(user_id, "searching")

async def remove_from_queue(user_id:int):
    """ remove a telegram id from 'search for aponent' from left side """

    await r.lrem("anon_chat_queue", 1, user_id)

async def match_users():
    """
        Is there at least 2 users in queue?
            no  ->  return None
            yes ->  1) select 2 of them 'from left side'.
                        2) remove them from queue. 
                        3) return [first_id, second_id]
    """

    user1_id = await r.lpop("anon_chat_queue")
    if not user1_id:
        return None
    user2_id = await r.lpop("anon_chat_queue")
    if not user2_id:
        await r.lpush("anon_chat_queue", user1_id)
        return None

    await create_a_connections_row(user1_id, user2_id)
    await link_client_to_against(user1_id, user2_id, "anon-chat")
    return [user1_id, user2_id]

# ---- Semi Anon ----
async def match_sa_users(user_id:int, against_id:int):
    """ 
        We know who is against, but user is anonymous
    """

    await link_client_to_against(user_id, against_id, "semi-chat")
    return await create_sa_connections_row(user_id, against_id)

async def store_chat_id_hash(mapping:dict, user_id:int):
    """
        relate a sa_connection id to user* button. example: 
        
        chatmap:12345678 = {user1:15,
                            user2:21}
    """

    await r.hset(f"chatmap:{user_id}", 
                    mapping=mapping   
                )

async def get_chat_id_by_button(user_id:int, button_text:str):
    return await r.hget(f"chatmap:{user_id}", button_text)

# Next two functions are relate to AGANIST user
async def set_current_semi_chat_id(user_id:int, button_text: str|None = None, chat_id: int|None = None):
    """ 
        example: (current_semi_chat:88888888 = 12)
        1) get sa_connection id from user* button which user clicked on that before.
        2) match this number with user telegram id.

        you can get chat_id from the value of user* which is saved by store_chat_id_hash before
        you also can give the chat id manual
    """
    if button_text:
        chat_id = await get_chat_id_by_button(user_id, button_text)
    await r.set(f"current_semi_chat:{user_id}", chat_id)

async def get_current_semi_chat_id(user_id:int):
    """ example: (current_semi_chat:88888888 = 17) """

    return int(await r.get(f"current_semi_chat:{user_id}"))
