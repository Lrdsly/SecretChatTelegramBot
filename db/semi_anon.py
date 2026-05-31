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

async def get_sa_chats_id(user_id):
    query = """
                SELECT id FROM sa_connections WHERE user_id = %s
            """
    return await fetchall(query, (user_id,))
# به ازای هر چت یک کوری ارسال میشه . در نسخه های بعدی به گرفتن تمام پیام های ناخوانده با یک کوری بپرداز
async def get_unread_messages(chat_id):
    query = """
                SELECT * FROM sanon_messages WHERE
                conversation_id = %s
                AND is_read = FALSE
            """
    return await fetchalll(query, (chat_id))
