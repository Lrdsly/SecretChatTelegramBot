from dotenv import load_dotenv
import aiomysql
import os

# ---- ENJOY CODING TODAY ----

load_dotenv()

DB_CONFIG = {
    "host": "localhost", 
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "db": os.getenv("DB_NAME")
}

pool = None
async def initialize_pool():
    global pool
    pool = await aiomysql.create_pool(
        **DB_CONFIG,
        minsize = 1,
        maxsize = 5
    )

async def fetchone(query, params):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            return await cur.fetchone()

async def fetchall(query, params=None):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            return await cur.fetchall()

async def execute(query, params=None):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            await conn.commit()

<<<<<<< HEAD
async def execute_return_id(query, params):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            await conn.commit()
            return cur.lastrowid()
=======
>>>>>>> df60fdf (add "my chats" button in semi anon .)
