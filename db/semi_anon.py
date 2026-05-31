from db.pool import fetchall

# ---- ENJOY CODING TODAY ----

async def verify_authorization(user_id, against_id):
    query = """
                SELECT EXISTS (
                    SELECT 1 FROM blocked_users WHERE
                    user_id = %s AND
                    blocked_user_id = %s)
             """
    return not(await execute(query, (user_id, against_id)))

async def get_semi_chats_id(user_id):
    """ against in known user, and the other one is anonymous """

    query = """
                SELECT id FROM sa_connections WHERE against_id = %s
            """
    return await fetchall(query, (user_id,))

async def get_current_semi_chat_id(user_id, against_id):
    query = """ SELECT id FROM sa_connections WHERE
                    user_id = %s AND
                    against_id = %s AND
                    closed_at IS NULL
            """
    return await fetchone(query, (user_id, against_id))
# به ازای هر چت یک کوری ارسال میشه . در نسخه های بعدی به گرفتن تمام پیام های ناخوانده با یک کوری بپرداز
async def store_sent_message(sender_id, conversation_id:int, message):
    query = """
                INSERT INTO semi_messaages (sender_id, conversation_id, message) VALUES (%s, %s, %s)
            """
    await execute(query, (sender_id, conversation_id, message))

async def create_sa_connections_row(user_id:int, against_id:int):
    query = """ INSERT INTO sa_connections (user_id, against_id) VALUES (%s, %s)"""
    await execute(query, (user_id, against_id))
