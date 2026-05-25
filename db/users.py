from db.pool import fetchone, exucute
from random import choices
import string

# ---- ENJOY CODING TODAY ----

def generate_pid(char_count:int) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(choices(chars, k=char_count)

async def create_user(telegram_id, personal_id=None):
    if not personal_id:
        personal_id = generate_pid(char_count=8)
    build_query = "INSERT INTO users (telegram_id, personal_id) VALUES (%s, %s)"
    fetch_query = "SELECT * FROM users WHERE id = LAST_INSERT_ID()"
    await execute(build_query, (telegram_id, personal_id))
    user = await fetchone(fetch_query)
    return user

async def get_or_create_user(telegram_id:int) -> tuple:
    query = "SELECT * FROM users WHERE telegram_id = %s"
    user = await fetchone(query, (telegram_id,))
    if user:
        return user
    return await create_user(telegram_id)
    

