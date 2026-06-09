import aiomysql
import os

# ---- ENJOY CODING TODAY ----


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"), 
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "db": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306))
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

async def execute_return_id(query, params):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            await conn.commit()
            return cur.lastrowid
