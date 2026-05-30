from db.pool import execute

# ---- ENJOY CODING TODAY ----

async def end_connection(user_id, against_id):
    query = """UPDATE a_connections SET closed_at=NOW() WHERE 
             user1_id = %s
             AND user2_id = %s 
             AND closed_at IS NULL"""
    await execute(query, (user_id, against_id))
    await execute(query, (against_id, user_id))
