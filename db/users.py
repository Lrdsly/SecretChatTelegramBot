from db.pool import fetchone, execute
from random import choices
import string

# ---- ENJOY CODING TODAY ----

def generate_pid(char_count:int) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(choices(chars, k=char_count))

async def register_user(
                        telegram_id,
                        personal_id=None,
                        name=None,
                        lastname=None,
                        username=None,
                        phone=None):

    if not personal_id:
        personal_id = generate_pid(char_count=8)
    build_query = """INSERT INTO users (telegram_id, personal_id, name, lastname, username, phone) VALUES
                                      (%s, %s, %s, %s, %s, %s)"""
    fetch_query = "SELECT * FROM users WHERE id = LAST_INSERT_ID()"
    await execute(build_query, (telegram_id, personal_id, name, lastname, username, phone))
    user = await fetchone(fetch_query, None)
    return user

async def get_or_register_user(telegram_id:int,
                        personal_id=None,
                        name=None,
                        lastname=None,
                        username=None,
                        phone=None) -> tuple:
    query = "SELECT * FROM users WHERE telegram_id = %s"
    user = await fetchone(query, (telegram_id,))
    if user:
        return user
    return await register_user(telegram_id,
                        personal_id,
                        name,
                        lastname,
                        username,
                        phone)
    

