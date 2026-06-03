from db.pool import *

# ---- ENJOY CODING TODAY ----

async def verify_authorization(user_id, against_id):
    query = """
                SELECT EXISTS (
                    SELECT 1 FROM blocked_users WHERE
                    user_id = %s AND
                    blocked_user_id = %s)
             """
    return not(await execute(query, (user_id, against_id)))

async def get_semi_chats_id(against_id:int):
    """ against in known user, and the other one is anonymous """

    query = """
                SELECT id FROM sa_connections WHERE against_id = %s
            """
    return await fetchall(query, (against_id,))

async def get_current_semi_chat_id(user_id, against_id):
    query = """ SELECT id FROM sa_connections WHERE
                    user_id = %s AND
                    against_id = %s AND
                    closed_at IS NULL
            """
    return await fetchone(query, (user_id, against_id))

async def create_sa_connections_row(user_id:int, against_id:int):
    query = """ INSERT INTO sa_connections (user_id, against_id) VALUES (%s, %s)"""
    _id = await execute_return_id(query, (user_id, against_id))
    return _id
