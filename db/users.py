from db.pool import fetchone, execute, execute_return_id
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
    user_id = await execute_return_id(build_query, (telegram_id, personal_id, name, lastname, username, phone))
    user = await fetchone("SELECT * FROM users WHERE id = %s", user_id)
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
    
async def get_secret_link(user_id:int):
    query = "SELECT personal_id FROM users WHERE telegram_id = %s"
    personal_id = await fetchone(query, (user_id,))
    link = f"https://ble.ir/DebtManagerBot?start={personal_id[0]}"
    return link

async def get_user_by_personal_id(personal_id:int):
    query = """ SELECT * FROM users WHERE personal_id = %s"""
    return await fetchone(query, (personal_id,))
