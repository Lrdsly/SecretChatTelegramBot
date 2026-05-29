from dotenv import load_dotenv

import aiomysql
import asyncio
import os 

# ---- ENJOY CODING TODAY ----

load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db = os.getenv("DB_NAME")

DB_CONFIG = {
    "host": "localhost",
    "user": user,
    "password": password,
    "db": db
}

CREATE_USERS_TABLE = """
                    CREATE TABLE IF NOT EXISTS users (
                                
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                telegram_id BIGINT UNIQUE,
                                personal_id VARCHAR(20) UNIQUE,
                                joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,

                                name VARCHAR(100) NULL,
                                lastname VARCHAR(100) NULL,
                                username VARCHAR(100) NULL,
                                phone VARCHAR(13) NULL
                    );
                     """

CREATE_SEMI_ANONYMOUS_CONNECTIONS_TABLE = """
                            CREATE TABLE IF NOT EXISTS sa_connections (
                            
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                user1_id BIGINT,
                                user2_id BIGINT,
                                started_at DATETIME NULL,
                                closed_at DATETIME NULL
                             );
                           """

CREATE_ANONYMOUS_CONNECTIONS_TABLE = """
                                    CREATE TABLE IF NOT EXISTS a_connections(
                                        id INT AUTO_INCREMENT PRIMARY KEY,
                                        user1_id BIGINT NOT NULL,
                                        user2_id BIGINT NOT NULL,
                                        started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                                        closed_at DATETIME NULL
                                    );
                                     """
async def init_db():
    conn = await aiomysql.connect(**DB_CONFIG)
    async with conn.cursor() as cur:
        await cur.execute(CREATE_USERS_TABLE)
        await cur.execute(CREATE_SEMI_ANONYMOUS_CONNECTIONS_TABLE)
        await cur.execute(CREATE_ANONYMOUS_CONNECTIONS_TABLE)
        await conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())
