from db.pool import *

# ---- ENJOY CODING TODAY ----

async def verify_authorization(user_id, against_user_id):
    query = """
                SELECT EXISTS (
                    SELECT 1 FROM blocked_users WHERE
                    user_id = %s AND
                    blocked_user_id = %s)
             """
    check = await fetchone(query, (user_id, against_user_id))
    return check[0] == 0

async def make_connection(user_id, args):
    from db.users import get_user_by_personal_id
    import db.redis as r
    from db.users import get_user_full_name

    async def final_step(against_user):
        other_text = None
        if await verify_authorization(user_id, against_user[0]):
            against_name = (await get_user_full_name(against_user[1]))[0] # It include username in the next index
            
            # configure chats
            sa_connection_id, status = await r.sa_match_users(user_id, against_user[1])
            if status == "new":
                await r.set_current_semi_chat_id(user_id=user_id, chat_id=sa_connection_id)
            
                reply_text = f"شما به کاربر {against_name} وصل شدید. لطفا پیام خود را بفرستید"
                other_text = "یک کاربر ناشناس برای شما پیامی ثبت کرد، پیام را از قسمت گفتگو های من بررسی کنید"
            elif status == "existing": reply_text = "چنین گفتگویی ای از قبل وجود دارد."
        else:
            reply_text = "امکان ساخت این گفتگو وجود ندارد\n\nموارد زیر را بررسی کنید:د\n1. کاربر گفتگو را قبلا مسدود کرده است"
        return reply_text, other_text
        
    if args:
        against_user = await get_user_by_personal_id(args[0])
        other_text = None
        if against_user:
            if against_user[1] == user_id:
                reply_text = "شما نمی توانید با خودتان گفتگو ناشناس انجام دهید\n خودت رو میشناسی مگه نه؟ :)"

            # block if user is in anon-chat
            elif await r.get_user_state(user_id) == "anon-chat":
                reply_text = "شما در حال حاضر در یک گفتگوی ناشناس هستید."

            elif current_chat_id := await r.get_current_semi_chat_id(user_id):
                chat_sides = await get_semi_chat_sides(current_chat_id)
                # check if user has already built a semi chat using secret link
                if chat_sides[0] == user_id:
                    reply_text = "شما در حال حاضر یک گفگتوی نیمه ناشناس باز دارید"
                else:
                    reply_text, other_text = await final_step(against_user)
            # user can build that chat, just check entered information
            else : 
               reply_text, other_text = await final_step(against_user)
        else: reply_text = "چنین شخصی ای وجود ندارد یا شناسه شخصی اشتباه است."

        return reply_text, other_text
   
async def get_semi_chats_id(against_id:int):
    """ against in known user, and the other one is anonymous """

    query = """
                SELECT id FROM sa_connections WHERE (against_id = %s  OR user_id = %s) AND closed_at IS NULL
            """
    return await fetchall(query, (against_id, against_id))

async def get_current_semi_chat_id(user_id, against_id):
    query = """ SELECT id FROM sa_connections WHERE
                    user_id = %s AND
                    against_id = %s AND
                    closed_at IS NULL
            """
    return await fetchone(query, (user_id, against_id))

async def get_semi_chat_sides(chat_id):
    query = """
                SELECT user_id, against_id FROM sa_connections WHERE id = %s
            """
    return await fetchone(query, (chat_id,))

async def create_sa_connections_row(user_id:int, against_id:int):
    existing = await fetchone(
        "SELECT id FROM sa_connections WHERE user_id = %s AND against_id = %s AND closed_at IS NULL",
        (user_id, against_id))

    if existing:
        return existing[0], "existing"

    query = "INSERT INTO sa_connections (user_id, against_id) VALUES (%s, %s)"
    _id = await execute_return_id(query, (user_id, against_id))
    return _id, "new"

async def end_sa_connection(user_id:int, against_id:int):
    query = """ UPDATE sa_connections SET closed_at = NOW() WHERE
                    (user_id = %s AND against_id = %s) OR
                    (user_id = %s AND against_id = %s) AND
                    closed_at IS NULL
            """
    await execute(query, (user_id, against_id, against_id, user_id))