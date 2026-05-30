from db.pool import execute

import asyncio

# ---- ENJOY CODING TODAY ----

CREATE_BLOCKED_USERS_TABEL = """
                             CREATE TABLE blocked_user IF NOT EXISTS (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                user_id BIGINT NOT NULL,
                                blocked_user_id BIGINT NOT NULL,
                                blocked_time DATETIME DEFAULT CURRENT_TIMESTAMP
                             )
                             """

CREATE_SANON_MESSAGES_TABLES = """
                               CREATE TABLE sanon_messages IF NOT EXISTS (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    conversation_id INT NOT NULL,
                                    message_text TEXT,
                                    sent_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                                    is_read BOOLEAN DEFAULT FALSE,
                                    FOREIGN KEY (conversation_id) REFERENCES sa_connections(id)
                               )
                               """

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
                                user_id BIGINT,
                                against_id BIGINT,
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
    await execute(CREATE_USERS_TABLE)
    await execute(CREATE_SEMI_ANONYMOUS_CONNECTIONS_TABLEM)
    await execute(CREATE_ANONYMOUS_CONNECTIONS_TABLE)
    await execute(CREATE_BLOCKED_USER_TABLE)
    await execute(CREATE_SANON_MESSAGES_TABLE)
    print("Database initialized successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())
